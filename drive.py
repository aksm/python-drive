# import python libraries
from decouple import config
from google.oauth2 import service_account
import googleapiclient.discovery

# define the scope for access level
SCOPES = ['https://www.googleapis.com/auth/drive']

# import the credentials from the .data folder in the root of this project
SERVICE_ACCOUNT_FILE_NAME = config('SERVICE_ACCOUNT_FILE_NAME')
SERVICE_ACCOUNT_FILE = './.data/' + SERVICE_ACCOUNT_FILE_NAME

DELEGATE = config('DELEGATE')  # Service account will impersonate this user. Must have proper admin privileges in G Suite. Check .env file for email address.

credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
credentials_delegated = credentials.with_subject(DELEGATE)

service = googleapiclient.discovery.build('drive', 'v3', credentials=credentials_delegated)

page_token = None
while True:
    response = service.files().list(q="mimeType='application/vnd.google-apps.folder'",
                                          spaces='drive',
                                          fields='nextPageToken, files(id, name)',
                                          pageToken=page_token).execute()
    for file in response.get('files', []):
        # Process change
        print ('Found file: %s (%s)' % (file.get('name'), file.get('id')))
    page_token = response.get('nextPageToken', None)
    if page_token is None:
        break
