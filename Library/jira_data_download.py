from jira import JIRA
import pandas
from dateutil.parser import parse
import math


class JiraDataDownload:
    def __init__(self, login, api_key, project_list, jira_options, fields):
        self.__fields = fields
        self.__project_list = project_list
        self.__connect = JIRA(options=jira_options, basic_auth=(login, api_key))
        self.__result = []
        self.__issues = 0

    def get_data(self):
        for project in self.__project_list:

            JiraDataDownload.__log_project(project)

            jql = 'project=' + str(project)
            size = 100
            initial = 0

            JiraDataDownload.__request(self, jql, size, initial)

        return self.__result

    def __request(self, jql, size, initial):
        while True:
            start = initial * size
            self.__issues = self.__connect.search_issues(jql_str=jql,
                                                         startAt=start,
                                                         maxResults=size,
                                                         fields=self.__fields)

            if JiraDataDownload.__issues_len_checked(self.__issues):
                break

            initial += 1

            JiraDataDownload.__log_page_number(initial)

            JiraDataDownload.__processing_request(self, self.__issues)

    def __processing_request(self, issues):
        for issue in issues:
            if JiraDataDownload.__field_checked(issue, 'customfield_10163'):
                if JiraDataDownload.__issues_fields_value_checked(issue):
                    if JiraDataDownload.__story_point_value_checked(issue.fields.customfield_10163):
                        iteration_result = JiraDataDownload.__iteration_result(issue)
                        self.__result.append(iteration_result)

    @staticmethod
    def __iteration_result(issue):
        iteration_result = [str(issue),
                            str(issue.fields.status),
                            parse(str(issue.fields.created)),
                            (int(issue.fields.aggregatetimespent)),
                            (math.ceil(int(issue.fields.aggregatetimespent) / 3600)),
                            float(issue.fields.customfield_10163)]
        return iteration_result

    @staticmethod
    def __issues_len_checked(issues):
        if len(issues) == 0:
            return True
        else:
            return False

    @staticmethod
    def __field_checked(issue, field_name: str):
        if hasattr(issue.fields, field_name):
            return True
        else:
            return False

    @staticmethod
    def __issues_fields_value_checked(issue):
        if issue.fields.created is not None and \
                str(issue.fields.status) == 'Closed' and \
                issue.fields.customfield_10163 is not None and \
                issue.fields.aggregatetimespent is not None:
            return True
        else:
            return False

    @staticmethod
    def __story_point_value_checked(field):
        if float(field) >= 1.0:
            return True
        else:
            return False

    @staticmethod
    def __log_project(project):
        print('Request data ' + str(project))

    @staticmethod
    def __log_page_number(page_number):
        print('Pagination is in progress. Page number: ' + str(page_number))
