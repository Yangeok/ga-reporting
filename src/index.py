import os, glob, json, argparse, httplib2, time
from apiclient.discovery import build
from oauth2client import client
from oauth2client import file
from oauth2client import tools

START_DATE = os.environ['START_DATE']
END_DATE = os.environ['END_DATE']

TOKEN_FILE_NAME = './data/credentials.dat' # client_secrets.json을 가공해서 나오는 파일입니다.
CLIENT_SECRET = './data/client_secret.json' # google developers에서 이 파일을 다운받을 수 있습니다.
SCOPE = 'https://www.googleapis.com/auth/analytics.readonly'
VIEW_ID = '194260241' # query explorer에서 viewId를 찾아 붙여넣어주세요

def initialize_analyticsreporting():
    parser = argparse.ArgumentParser(
      formatter_class=argparse.RawDescriptionHelpFormatter,
      parents=[tools.argparser]
    )
    flags = parser.parse_args()
    flow = client.flow_from_clientsecrets(
      CLIENT_SECRET, 
      scope=SCOPE,
      message=tools.message_if_missing(CLIENT_SECRET)
    ) 

    storage = file.Storage(TOKEN_FILE_NAME)
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, storage, flags)

    http = credentials.authorize(http=httplib2.Http())
    analytics = build('analyticsreporting', 'v4', http=http)

    return analytics
    
def get_report(analytics, client_id):
  print(client_id)
  body = {
          'dateRange': {
            'startDate': START_DATE, 
            'endDate': END_DATE
          },
          'viewId': VIEW_ID,
          'user': {
            'type': 'CLIENT_ID', 
            'userId': client_id
          },
          'activityTypes': ['ECOMMERCE']          
        }
  return analytics.userActivity().search(body=body).execute()

def save_response(response, client_id):
  print(f'> saving client {client_id}\n')
  with open(f'./json/{client_id}.json', 'w', encoding='utf-8') as make_file:
    json.dump(response, make_file, indent="\t")

def get_client_id():
  file_names = glob.glob('./csv/*.csv')
  arr = []

  for file_name in file_names:
    rows = list(open(file_name, 'r'))[7:]
    for row in rows:
      row = row.split(',')[0]
      arr.append(row)
  
  print(f'\n> client_id length: {len(arr)}\n')
  return arr

def main():
  analytics = initialize_analyticsreporting()
  client_ids = get_client_id()
  for client_id in client_ids:
    time.sleep(10)
    response = get_report(analytics, client_id)
    save_response(response, client_id)
  
if __name__ == '__main__':
  main()
