import sys
import webbrowser
import time
import json
#
import os
import json
import requests
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def change(title):
    title_new=""
    length = len(title)
    for i in range(0,length):
        if(title[i]!='|'):
            title_new=title_new+title[i]
        else:
            title_new=title_new+'_'
    return title_new

def isPresent(title):
    json_file_path = 'public\\css\\task1\\songs.json'
    file = open(json_file_path,'r')

    songs = json.load(file)
    if(title in songs):
        return True
    else:
        return False

def saveToJson(title):
    json_file_path = 'public\\css\\task1\\songs.json'
    with open(json_file_path, 'r') as file:
        songs = json.load(file)
    songs.extend(title)
    with open(json_file_path, 'w') as file:
        json.dump(songs, file, indent=4)

def authentiate_google_drive():
    creds = Credentials.from_service_account_file(service_account_file, scopes=scopes)
    service = build('drive', 'v3', credentials=creds)
    return service

def download_file(url):
    response = requests.get(url)
    file_name = title+'_'+videoID
    local_file_path = os.path.join(os.getcwd(), file_name)
    with open(local_file_path,"wb") as file:
        file.write(response.content)
    return local_file_path, file_name, response.content

def upload_to_google_drive(service, file_path, file_name, folder_id=None):
    file_metadata = {'name' : file_name}
    if folder_id:
        file_metadata['parents'] = [folder_id]
    media = MediaFileUpload(file_path, mimetype="application/octet-stream")
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    
data_back = "Yes"

link = sys.argv[1] 
title = sys.argv[2]
title = change(title) 
videoID = sys.argv[3]

if(isPresent(title+'_'+videoID)):
    print("Song already taken try another one")
else:
    #webbrowser.open_new_tab(link)                    #remember to remove .env folders from ur task01a directory as those things will be given to 
    #third party server via environment variables
    service_account_file = json.loads(os.getenv("GOOGLE_DRIVE_JSON"))
    scopes = ['https://www.googleapis.com/auth/drive.file']

    service = authentiate_google_drive()
    url = link
    file_path, file_name, response_content = download_file(url)
    upload_to_google_drive(service, file_path, file_name, folder_id='1Y_3XGo2z6miI-O9j_U9H0vEN_ea9uQ_k')
    os.remove(file_path)


    import MelSpec
    MelSpec.save(response_content,title+'_'+videoID)
    saveToJson(title+'_'+videoID)
    # time.sleep(7)
    # import MelSpec
    # MelSpec.save(title+'_'+videoID)
    # saveToJson(title+'_'+videoID)
    # print(title+'_'+videoID)

sys.stdout.flush()
