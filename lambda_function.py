import n2n_functions as n2n
import requests
import json

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from decouple import config, Csv

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

import os

def lambda_handler(event, context):
    api_data_loader()

def api_data_loader():
    #### Read previous data from google sheets

    # Define the scope
    SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    CREDENTIALS = json.loads(config('CRED_GCP'))

    # Credentials
    # add credentials to the account
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(CREDENTIALS, SCOPE)

    # authorize the clientsheet
    client = gspread.authorize(credentials)

    # get the instance of the Spreadsheet
    sheet = client.open('Copy of N2N - Database')

    # get the first sheet of the Spreadsheet
    sheet_instance = sheet.get_worksheet(0)

    # Read google sheet
    data = sheet_instance.get_all_values()
    dfToUpdate = pd.DataFrame(data[1:], columns=data[0])

    # Read relevant variables
    # Define actual meeting number
    dfToUpdate['#'] = dfToUpdate['#'].astype(int)
    MAX_NUMBER = dfToUpdate['#'].max()


    #### Read new data -----------------------------------------------
    # Read eventbrite credentials

    #with open("gcp_api/evenbrite_credentials.json", "r") as file:
        #credentials = json.load(file)

    TOKEN_API = config("TOKEN_API")
    ID_N2N = config("ID_N2N")

    url_all_events = f'https://www.eventbriteapi.com/v3/organizations/{ID_N2N}/events/' # all events from organization

    headers = {
        'Authorization': f'Bearer {TOKEN_API}',
    }

    # extract dates
    dfToUpdate['Date'] = pd.to_datetime(dfToUpdate['Date'], format='%B %d, %Y')
    dfToUpdate['Date'] = dfToUpdate['Date'].dt.strftime('%Y-%m-%d')
    dfToUpdate['Date'] = pd.to_datetime(dfToUpdate['Date'], format='%Y-%m-%d')

    start_date = dfToUpdate['Date'].max() + timedelta(days=1)
    start_date = start_date.strftime('%Y-%m-%d')

    end_date = (datetime.today() - timedelta(days=1))
    end_date = end_date.strftime("%Y-%m-%d")

    params_all_events = {
        'start_date.range_start': start_date,
        'start_date.range_end': end_date
    }

    # Extract id of all the meeting that are not in the spreadheet
    response_events = requests.get(url_all_events, headers=headers, params=params_all_events).json()
    #number_events = len(response_events['events'])
    try:
        number_events = len(response_events['events'])
    except KeyError as error:
        raise ValueError(f'There are no new meetings from {start_date} to {end_date}') from error

    all_events = response_events['events']

    id_events = [x['id'] for x in all_events]

    ##----------------------------------

    '''total_attendees = []

    for x in id_events:
        attendees_info = join_attendees_information(x)
        total_attendees.extend(attendees_info)'''
    # join all the attendees information in one list.
    total_attendees = [attendee for x in id_events for attendee in n2n.join_attendees_information(x,headers)]


    df = n2n.list_to_df(total_attendees)

    #df.to_csv('test.csv', index=False, encoding='utf-8')
    #df.to_excel('test.xlsx', index=False)

    #### Process the data --------------------

    # City
    df['City'] = df['Event Name'].apply(n2n.extract_city)

    # Seasons

    # transform the data format
    df['Date'] = pd.to_datetime(df['Date Attending'], format='%Y-%m-%dT%H:%M:%S')
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

    # Apply the custom function to create a new 'Season' column
    df['Season'] = df.apply(n2n.season_based_on_city, axis=1)

    # Save the data according the spreadsheet
    df['Date'] = df['Date'].dt.strftime('%m/%d/%Y')

    # Industry/Event

    df['Industry / Event'] = df['Event Name'].apply(n2n.extractName)

    # Format

    df['Format'] = df['Event Name'].apply(n2n.returnFormat)

    # Create an empty list to store the counter values
    counter_values = []

    # Initialize variables to keep track of the previous date and city
    prev_date = None
    prev_city = None
    counter = 0

    # Iterate through the DataFrame rows
    for index, row in df.iterrows():
        current_date = row['Date']
        current_city = row['City']

        # Check if either the date or city has changed from the previous row
        if current_date != prev_date or current_city != prev_city:
            counter += 1
        counter_values.append(counter)

        # Update the previous date and city values for the next iteration
        prev_date = current_date
        prev_city = current_city

    df['#'] = counter_values
    df['#'] = df['#'] + MAX_NUMBER

    # Attedance
    df['Attendance'] = df['Attendee Status']

    # Add columns

    # Country of Origin
    n2n.add_cols(df,'What country are you from in Latin America? (if applicable)','¿De qué país eres en América Latina? (si aplica)','Country of Origin')

    # Define a dictionary for replacements
    replacements = {
        '': np.nan,
        '.': np.nan,
        'Canadá': 'Canada',
        'Perú': 'Peru',
        'España': 'Spain',
        'México': 'Mexico',
        'República Dominicana': 'Dominican Republic',
        '-': np.nan,
        'Not': np.nan,
        'nan': np.nan,
        'Alberta, British Columbia And Calgary.' : 'Canada',
        'Brasil': 'Brazil',
        'Amazonia' : 'Colombia',
        'Amazonia' : 'Colombia',
        'Dr': np.nan,
        'Yes': np.nan,
        'Spain/Colombia': 'Colombia',
        'Mexico/El Salvador': 'Mexico',
        'X' : np.nan,
        'Na,India': np.nan,
        'None (Spain)': np.nan,
        'India':np.nan,
        'South Africa':np.nan,
        'Puebla, México' : 'Mexico',
        'Ciudad De México' : 'Mexico',
        'Coló Me La' : np.nan,
        'Born In Canada.': np.nan,
        'Panamá': 'Panama',
        'Mex': np.nan,
        'Na':np.nan,
        'N/A':np.nan,
        'No':np.nan,
        'Np':np.nan,
        'N':np.nan,
    }

    df['Country of Origin']=df['Country of Origin'].replace(replacements)

    # Area of Expertise
    n2n.add_cols(df,'What area/subject do you specialize in? (in this industry)','¿En qué área/materia te especializas? (en esta industria)','Area of Expertise')

    # Employment Status
    n2n.add_cols(df,"What\'s your employment status?",'¿Cuál es tu situación laboral?','Employment Status')

    # Define a dictionary for replacements
    replacementsEmploymentStatus = {
        'Empleado': 'Employed',
        'Empleado en búsqueda de nuevas oportunidades': 'Employed and looking for opportunities',
        'Desempleado y buscando oportunidades': 'Unemployed and looking for opportunities',
        'Empleado y en búsqueda de oportunidades': 'Employed and looking for opportunities',
        '': np.nan
    }

    df['Employment Status']=df['Employment Status'].replace(replacementsEmploymentStatus)
    df['Employment Status'] = df['Employment Status'].str.capitalize()

    # Employer
    n2n.add_cols(df,'If employed, what company do you work for?','Si estás empleado, ¿para qué empresa trabajas?','Employer')

    # Dream job
    n2n.add_cols(df,'What is your dream job in Canada?','¿Cuál es tu trabajo soñado en Canadá?','Dream Job')

    # Linkedin
    n2n.add_cols(df,'Provide your LinkedIn if you want to connect with others in this community!',
            '¡Proporciona tu LinkedIn si quieres conectarte con otros en esta comunidad!',
            'Linkedin')

    # Select and organize fields
    df2 = df[['#','Date', 'City', 'Season', 'Industry / Event', 'Format', 'Attendance',  'Email', 'First Name', 'Last Name', 'Country of Origin', 'Area of Expertise', 'Employment Status', 'Employer', 'Dream Job', 'Linkedin']]

    set_with_dataframe(sheet_instance, df2, row=dfToUpdate.shape[0] + 2, include_column_header=False)
    print('ok v4')

#lambda_handler(1,2)