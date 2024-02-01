# Notworking2Networking Project

This project is about the impact and evolution of the industry-specific meet-ups for Latinos hosted by notworking2networking. (extraction of valuable insights, patterns identification, organazing the data, creation of visualizations and interpretation of results)
The project was divided in two organization the ETL process from the Eventbrite API, data analysis, creation of a power bi dashboard and an application deployed using AWS services.

### Tools used
* Google sheets
* Python
* Python libraries: gspread, numpy, pandas, datetime, ploty, matplotlib, seaborn
* Docker
* AWS services: EC2,lambda, CloudWatch, S3, ECR

## Specific
# Check!!
• Utilized Eventbrite API to extract relevant information and data related to 184 events, ensuring accurate and up-to-date details for organizational purposes.
• Employed Python and AWS tools to automate and streamline the database update process, enhancing efficiency by reducing the manual workload by 90%
• Designed and developed interactive dashboards to visualize and analyze attendance data for organizational meetings.
• Utilized visualization tools and techniques to present insights effectively, aiding decision-making processes within the organization, resulting in a 20% increase in meeting attendance rates.

<> (### Part 1)
<> # EDA Notworking2Networking attendance

<> ### Part 2


// ## Dataset information

## Project Steps

1. Understand the project: Have meetings to understand the business logic, set objectives and deliverables.

2. Select data source: Determine the specific API that provides the data needed for tha analysis. And understand the data gathered by the organization.

3. Understand the API: Study the documentation of the evenbrite API to understand its endpoinds, query parameters, and how to retrieve data.

4. Retrieve and preprocess Data: Develop an ETL using the Eventbrite API to fetch the required data based on the analysis goals, and host the data of the organization in a database. This is done using different python libraries and multiple free AWS servicess (lambda, CloudWatch, S3, ECR), to update the data after each meeting.

5. Analyze the Data: Utilize data science techniques and libraries such as pandas, stats to perform exploratory data analysis [(EDA)](https://github.com/DavidAndres6870/n2n/blob/main/EDA.ipynb), statistical analysis and visualizations. Extract meaningful insights and identify patterns or correlations in the data. Select the appropriate visualization tool like Matplotlib, Seaborn, Plotly and Power BI to create interactive and informative visualizations.

6. Design the applications/Dashboards: Design the user interface and layout of the dashboard using Dash library and Power BI. Create Create an intuitive and user-friendly dashboard that allows users to interact with the visualizations, apply filters, and explore the data dynamically. Iterate on the design and make improvements based on user input and additional data analysis requirements

7. Deploy dashboard: : Host the dashboard on a web server or a cloud platform to make it accessible online. This involves deploying it as a web application utilizing AWS cloud hosting services. Test and Iterate: Test the functionality and usability of the dashboard, seeking feedback from potential users.


## Application description
After connecting with Eventbrite API with the selected database and update the data after each meeting, the exploration derived in the building of the dasboard. The dashboards display important information about attendance meetings of the organizations through the time, by country,employment status, event mode, and industry. This dashboars allow to the company to organize and planify the number and industries for future meetings.

[Power BI dashboard](http://3.99.181.155:8050/)
[Access the dashboard here](http://3.99.181.155:8050/)

## Project structure
The project was divided in two repositories.
[ETL repository](https://github.com/DavidAndres6870/ETL-n2n) (actual)
[EDA repository](https://github.com/DavidAndres6870/n2n)


## Contact information
    Author: David Blanco
    Email: davidandres687@gmail.com
    Linkedln: https://www.linkedin.com/in/david-blanco-aponte/

## Acknoledgments
* Amazon Web Services (AWS) to develop ETL to the dataset after each meeting automaticaly.
* Dash Python User Guide: Dash is the original low-code framework for rapidly biulding data apps in Python.
* Dash Bootstrap Components: dash-bootstrap-components is a library of Bootstrap components for Plotly Dash, that makes it easier to build consistently styled apps with complex, responsive layouts.
