import argparse
from oauth2client import client
from oauth2client import file
from oauth2client import tools
from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
import httplib2
import pandas as pd
import numpy as np
import json

TOKEN_FILE_NAME = 'credentials.dat'
CLIENT_SECRETS = 'client_secrets.json'
SCOPES = 'https://www.googleapis.com/auth/analytics.readonly'
VIEW_ID = '181430824'

def prepare_credentials():
    parser = argparse.ArgumentParser(parents=[tools.argparser])
    flow = client.flow_from_clientsecrets(
      CLIENT_SECRETS, 
      scope=SCOPES,
      message='%s is missing' % CLIENT_SECRETS
    ) 
    flags = parser.parse_args()
    storage = Storage(TOKEN_FILE_NAME)
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, storage, flags)

    return credentials
  
def initialize_service():
    with open('credentials.dat') as json_file:
      data = json.load(json_file)


    credentials = client.OAuth2Credentials(
      client_id= data['client_id'],
      client_secret= data['client_secret'],
      access_token= data['access_token'],
      refresh_token= data['refresh_token'],
      token_expiry= data['token_expiry'],
      token_uri= data['token_uri'],
      user_agent= 'null',
    )
    http = httplib2.Http()
    credentials.refresh(http)
    credentials.authorize(http)
    # credentials = prepare_credentials()
    # print(credentials)
    # http = httplib2.Http()
    # http = credentials.authorize(http)

    return build('analyticsreporting', 'v4', http=http)

def get_report(analytics):
  # body = {
  #   "reportRequests":[
  #   {
  #     "viewId": VIEW_ID,
  #     "dateRanges":[
  #       {
  #         "startDate":"2015-06-15",
  #         "endDate":"today"
  #       }],
  #     "metrics":[
  #       {
  #         "expression":"ga:users"
  #       }],
  #     "dimensions": [
  #       {
  #         "name":"ga:browser"
  #       }]
  #     }]
  # }
  body = {
        'reportRequests': [{
            'viewId': VIEW_ID,
            'user': {
              'type': 'CLIENT_ID', 
              'userId': '662523190.1580044226'
            },
            'dateRanges': {
              'startDate': '7daysago', 
              'endDate': 'today'
            }
          }
        ]
      }
  # return analytics.reports().batchGet(body=body).execute()
  return analytics.userActivity().search(body=body).execute()

def print_response(response):
  for report in response.get('reports', []):
    columnHeader = report.get('columnHeader', {})
    dimensionHeaders = columnHeader.get('dimensions', [])
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
    rows = report.get('data', {}).get('rows', [])

    for row in rows:
      dimensions = row.get('dimensions', [])
      dateRangeValues = row.get('metrics', [])
      for header, dimension in zip(dimensionHeaders, dimensions):
        print(header + ': ' + dimension)

      for i, values in enumerate(dateRangeValues):
        print('Date range (' + str(i) + ')')
        for metricHeader, value in zip(metricHeaders, values.get('values')):
          print(metricHeader.get('name') + ': ' + value)


def main():

  analytics = initialize_service()
  response = get_report(analytics)
  print_response(response)

if __name__ == '__main__':
  main()
