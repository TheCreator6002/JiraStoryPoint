from google.oauth2 import service_account
from Library.jira_data_download import JiraDataDownload
from autorization_data import autorization_data, project_list, fields, jira_options, forecasting_accuracy
from Library.period_value import PeriodValue

import pandas
import pandas_gbq

final = []
final = pandas.DataFrame(data=final)

for project in project_list:
    # Retrieving data from Jira
    data = JiraDataDownload(login=autorization_data['login'],
                            api_key=autorization_data['api_key'],
                            jira_options=jira_options,
                            project_list=project,
                            fields=fields,
                            check_logged_time=True)

    result_list = data.get_data()

    columns = ['IssueName',
               'IssueStatus',
               'Start',
               'SumTimeSpent',
               'SumTimeSpentHours',
               'StoryPoints']

    result_dataframe = pandas.DataFrame(data=result_list, columns=columns)
    result_dataframe['Start'] = pandas.to_datetime(result_dataframe['Start'], utc=True)
    result_dataframe['SPHours'] = result_dataframe['SumTimeSpent'] / (result_dataframe['StoryPoints'] * 3600)

    for value in forecasting_accuracy:
        # Periods by years
        result_year = PeriodValue(value, 'years', result_dataframe, project[0]).get_value()

        # Periods by quarts
        result_quart = PeriodValue(value, 'quarts', result_dataframe, project[0]).get_value()

        iteration_result = result_year.append(result_quart, ignore_index=True)
        final = final.append(iteration_result, ignore_index=True)


pandas.set_option('display.max_columns', 48)

KEY_FILE_LOCATION = 'bigquery_sandbox.json'

credentials = service_account.Credentials.from_service_account_file(KEY_FILE_LOCATION)

pandas_gbq.to_gbq(dataframe=final,
                  destination_table='Sandbox.JiraIssuesTest',
                  project_id='glassy-sky-241405',
                  if_exists='replace',
                  credentials=credentials)
