import pandas as pd
import requests
from datetime import datetime, timedelta

def join_attendees_information(event_id: str, headers) -> list:
    """
    Arrange in a list of dictionaries all the information of the attendees

    Args:
        event_id (str): the event id from a meeting

    Returns:
        list: list made up of dictionaries with the information of each attendant by event
    """

    url_individual_event = f'https://www.eventbriteapi.com/v3/events/{event_id}/'
    response_individual_event = requests.get(url_individual_event, headers=headers).json()

    event_name =  response_individual_event['name']['text']
    date_attending = response_individual_event['start']['local']
    #date_attending = datetime.strptime(date_attending, "%Y-%m-%dT%H:%M:%S")
    #date_attending = date_attending.strftime("%Y-%m-%d")

    url_first_page = f'https://www.eventbriteapi.com/v3/events/{event_id}/attendees/' # url individual event
    response_first_page = requests.get(url_first_page, headers=headers).json()

    pages = response_first_page['pagination']
    page_count = pages['page_count']


    attendees = []
    for i in range(1,page_count+1):
        if i == 1:
            attendees = response_first_page['attendees']
        else:
            url_new_page = f'https://www.eventbriteapi.com/v3/events/{event_id}/attendees/?page={i}'
            new_page = requests.get(url_new_page,headers=headers).json()
            page_ateendees = new_page['attendees']
            attendees.extend(page_ateendees)
        #print(i)

    for attendee in attendees:
        attendee["event_name"] = event_name
        attendee["date_attending"] = date_attending

    return attendees


def list_to_df(total_attendees: list) -> pd.DataFrame:
        """
        Transform the json list of each attendee in a pandas data frame

        Args:
            total_attendees (list): json list with the information of each attendant

        Returns:
            df (dataframe): data frame with the information of each attendant
        """

        general_questions = ['Event Name',
                            'Date Attending',
                            'Attendee Status',
                            'Email',
                            'First Name',
                            'Last Name']

        question_list = ["What country are you from in Latin America? (if applicable)",
                                '¿De qué país eres en América Latina? (si aplica)',

                                'What area/subject do you specialize in? (in this industry)',
                                '¿En qué área/materia te especializas? (en esta industria)',

                                "What\'s your employment status?",
                                '¿Cuál es tu situación laboral?',

                                'If employed, what company do you work for?',
                                'Si estás empleado, ¿para qué empresa trabajas?',

                                'What is your dream job in Canada?',
                                '¿Cuál es tu trabajo soñado en Canadá?',

                                'Provide your LinkedIn if you want to connect with others in this community!',
                                '¡Proporciona tu LinkedIn si quieres conectarte con otros en esta comunidad!']

        columns = general_questions + question_list

        attendees_list = []
        for attendee in total_attendees:
            export_list = []
            export_list.append(attendee["event_name"]) # 'Event Name'
            export_list.append(attendee["date_attending"]) # 'Date Attending'
            export_list.append(attendee["status"]) # 'Attendee Status'

            export_list.append(attendee['profile']['email']) # email
            export_list.append(attendee['profile']['first_name']) # First name
            export_list.append(attendee['profile']['last_name']) # Last name

            for question in question_list:
                exist = False
                for answer in attendee['answers']:
                    if question == answer['question']:
                        exist = True

                        #dictionary, key
                        #dictionary.get(key, None)

                        export_list.append(answer.get('answer',None))
                        #export_list.append(get_value_or_none(answer,'answer'))

                if not exist:
                    export_list.append(None)

            attendees_list.append(export_list)

            df = pd.DataFrame(attendees_list, columns=columns)

            #print(question_list)
        return df

#### Process the data ---------------

# City
def extract_city(event_name:str) -> str:
    """
    Extract the name of the city using the event_name

    Args:
        event_name (str): field event_name from the evenbrite page

    Returns:
        str: The name of the city, can be Montreal or Toronto
    """
    if "Montreal" in event_name:
        return "Montreal"
    else:
        return "Toronto"

# Seasons
def return_season_toronto(meeting_date: str) -> int:
    """
    Return the seasson according to the meeting day
    Args:
        meeting_date (str): date of the meeting
    Returns:
        int: Number of the Toronto season
    """

    if meeting_date <= datetime(2021,3,4): return 1
    elif meeting_date <= datetime(2021,6,10): return 2
    elif meeting_date <= datetime(2021,12,9): return 3
    elif meeting_date <= datetime(2022,4,14): return 4
    elif meeting_date <= datetime(2022,7,28): return 5
    elif meeting_date <= datetime(2022,11,7): return 6
    elif meeting_date <= datetime(2023,4,6): return 7
    elif meeting_date <= datetime(2023,6,29): return 8
    elif meeting_date <= datetime(2023,12,31): return 9
    elif meeting_date <= datetime(2024,4,30): return 10
    elif meeting_date <= datetime(2024,8,10): return 11
    else: return 12

def return_season_montreal(meeting_date: str) -> int:
    """
    Return the seasson according to the meeting day
    Args:
        meeting_date (str): date of the meeting
    Returns:
        int: Number of the Montreal season
    """
    if meeting_date <= datetime(2023,12,31): return 1
    elif meeting_date <= datetime(2024,4,30): return 2
    else: return 3

# Apply the function according to hte city

def season_based_on_city(df: pd.DataFrame) -> int:
    """
    Return the season according the city of the meeting

    Args:
        df (dataframe): a dataframe to add the season

    Returns:
        int: Number of the season according to the city
    """

    if df['City'] == 'Toronto':
        return return_season_toronto(df['Date'])
    elif df['City'] == 'Montreal':
        return return_season_montreal(df['Date'])
    else:
        # Handle other cities or cases if needed
        return None

# Industry/Event
def extractName(eventName: str) -> str:
    """
    Extract the Industry or event from event Name

    Args:
        eventName (str): Full event name

    Returns:
        str: Name of the industry
    """
    if "|" in(eventName):
        split_result = eventName.split('|')

        eventNameBefore = split_result[0]
        eventNameAfter = split_result[1]

        if "NotWorking to Networking" in(eventNameBefore) or "NotWorking2Networking" in(eventNameBefore):
            eventName = eventNameAfter
        elif "NotWorking to Networking" in(eventNameAfter) or "NotWorking2Networking" in(eventNameAfter) or "N2N Montreal" in(eventNameAfter) or "N2N" in(eventNameAfter) or 'Not working to Networking Montreal' in(eventNameAfter) :
            eventName = eventNameBefore

        if 'Latinos in ' in eventName:
            split_result = eventName.split('Latinos in ')
            return split_result[1].strip()
        else:
            return eventName.strip()
    else:
        return eventName.strip()

# Format
def returnFormat(eventName: str) -> str:
    """_summary_

    Args:
        eventName (str): Full description of event

    Returns:
        str: Format of the meeting
    """

    #return "In Person" if "In Person" or "En persona" in eventName else "Online"
    return "In Person" if "In Person" in eventName or "En persona" in eventName else "Online"

# Function add columns
def add_cols (df:pd.DataFrame,field1:str, field2:str,result_field:str) -> str:
    """
    Add the information of two fields evaluating if one of both exist

    Args:
        df (pd.DataFrame): dataframe where the function will be applied
        field1 (str): first field to be added
        field2 (str): second field to be added
        result_field (str): name of the result field.

    Returns:
        str: dataframe with the new field
    """
    # Check if the columns exist in the DataFrame
    if field1 in df.columns and field2 in df.columns:
        # If both columns exist, perform the operations
        #df[field1] = df[field1].astype(str)
        #df[field2] = df[field2].astype(str)

        #df[field1].replace('nan','', inplace=True)
        #df[field2].replace('nan','', inplace=True)

        df[field1].fillna('', inplace=True)
        df[field2].fillna('', inplace=True)

        # Concatenate and strip
        df[result_field] = (df[field1] +
                                    df[field2]).str.strip()

        df[result_field] = df[result_field].str.title()

    elif field1 in df.columns:
        df[result_field] = df[field1].astype(str)
        df[result_field] = df[result_field].str.title()

    elif field2 in df.columns:
        df[result_field] = df[field2].astype(str)
        df[result_field] = df[result_field].str.title()
    else:
        # Handle the case where one or both columns are missing
        pass