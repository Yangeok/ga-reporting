import sys, glob, itertools, json, csv, argparse, httplib2, time
from oauth2client import client
from oauth2client import file
from oauth2client import tools
from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
import pandas as pd
import numpy as np

TOKEN_FILE_NAME = './data/credentials.dat' # client_secrets.json을 가공해서 나오는 파일입니다.
CLIENT_SECRETS = './data/client_secrets.json' # google developers에서 이 파일을 다운받을 수 있습니다.
SCOPES = 'https://www.googleapis.com/auth/analytics.readonly'
VIEW_ID = '181430824' # query explorer에서 viewId를 찾아 붙여넣어주세요

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
    # with open('credentials.dat') as json_file:
    #   data = json.load(json_file)

    # credentials = client.OAuth2Credentials(
    #   client_id= data['client_id'],
    #   client_secret= data['client_secret'],
    #   access_token= data['access_token'],
    #   refresh_token= data['refresh_token'],
    #   token_expiry= data['token_expiry'],
    #   token_uri= data['token_uri'],
    #   user_agent= 'null',
    # )
    # http = httplib2.Http()
    # credentials.refresh(http)
    # credentials.authorize(http)
    credentials = prepare_credentials()
    http = httplib2.Http()
    http = credentials.authorize(http)

    return build('analyticsreporting', 'v4', http=http)

def get_report(analytics, client_id):
  print(client_id)
  body = {
          'viewId': VIEW_ID,
          'user': {
            'type': 'CLIENT_ID', 
            'userId': client_id
          },
          'dateRange': {
            'endDate': 'today',
            'startDate': '2019-01-01' 
          }
        }
  return analytics.userActivity().search(body=body).execute()

def save_response(response, client_id):
  print(f'> saving client {client_id}\n')
  with open(f'./json/{client_id}.json', 'w', encoding='utf-8') as make_file:
    json.dump(response, make_file, indent="\t")

def get_client_id():
  # with open('./csv/data.csv', newline='') as csvfile:
  #     data = list(csv.reader(csvfile))

  # arr = []
  # rows = data[7:]
  # for row in rows:
  #     row = row[0]
  #     arr.append(row)
    
  # return arr
  list_of_files = glob.glob('./csv/*.csv')
  arr = []

  for file_name in list_of_files:
    rows = list(open(file_name, 'r'))[7:]
    for row in rows:
      row = row.split(',')[0]
      arr.append(row)
  
  # print(arr)
  print(f'\n> client_id length: {len(arr)}\n')
  return arr

def main():
  analytics = initialize_service()
  client_ids = get_client_id()
  for client_id in client_ids:
    time.sleep(10)
    print('timeout...')
    response = get_report(analytics, client_id)
    save_response(response, client_id)
  

if __name__ == '__main__':
  main()
