from google.oauth2 import service_account
from Library.jira_data_download import JiraDataDownload
from autorization_data import autorization_data, \
    project_list, fields, jira_options, forecasting_accuracy, projects, project_keys
from Library.period_value import PeriodValue

import pandas
import pandas_gbq

# In[Get Jira data]
final = []
final = pandas.DataFrame(data=final)

for project in project_list:
    # Retrieving data from Jira
    data = JiraDataDownload(login=autorization_data['login'],
                            api_key=autorization_data['api_key'],
                            jira_options=jira_options,
                            project_list=project,
                            fields=fields,
                            check_logged_time=False)

    result_list = data.get_data()

    columns = ['IssueName',
               'IssueStatus',
               'Start',
               'StoryPoints']

    result_dataframe = pandas.DataFrame(data=result_list, columns=columns)
    result_dataframe['Start'] = pandas.to_datetime(result_dataframe['Start'], utc=True)

    # Group by month
    grouper_result = result_dataframe.groupby(pandas.Grouper(key='Start', freq='M')).agg({'StoryPoints': 'sum'})

    grouper_result['Date'] = grouper_result.index

    grouper_result['Project'] = str(project[0])

    final = final.append(grouper_result, ignore_index=True)

# In[Get dev payroll]
KEY_FILE_LOCATION = 'bigquery_sandbox.json'

credentials = service_account.Credentials.from_service_account_file(KEY_FILE_LOCATION)

sql = '''SELECT 
            Name, 
            MVZ_MAIN,
            end_of_month,
            Total_Payroll
         FROM 
            `F_DATASET.Dev_Payroll`'''

df = pandas_gbq.read_gbq(sql, project_id='glassy-sky-241405')

dev_payroll = []
dev_payroll = pandas.DataFrame(data=dev_payroll)

for project in projects:
    iteration_frame = df.loc[df['MVZ_MAIN'] == project]
    iteration_frame = iteration_frame.groupby([pandas.Grouper(key='end_of_month', freq='M')]).agg({'Total_Payroll': 'sum'})
    iteration_frame['Date'] = iteration_frame.index
    iteration_frame['Project'] = str(project)
    dev_payroll = dev_payroll.append(iteration_frame, ignore_index=True)

pandas.set_option('display.max_columns', 48)

dev_payroll['Project'] = dev_payroll['Project'].map(project_keys)


# In[Merge and upload]

final = pandas.merge(final, dev_payroll, how="left", on=["Date", "Project"])

pandas_gbq.to_gbq(dataframe=final,
                  destination_table='Sandbox.JiraIssues853',
                  project_id='glassy-sky-241405',
                  if_exists='replace',
                  credentials=credentials)
