import sys
import base64
import json
import urllib
#
import webbrowser
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
    json_file_path = os.path.join(os.getcwd(),'public/css/task1/songs.json')
    file = open(json_file_path,'r')

    songs = json.load(file)
    if(title in songs):
        return True
    else:
        return False

def saveToJson(title):
    json_file_path = os.path.join(os.getcwd(),'public/css/task1/songs.json')
    with open(json_file_path, 'r') as file:
        songs = json.load(file)
    songs.append(title)
    with open(json_file_path, 'w') as file:
        json.dump(songs, file, indent=4)

def authentiate_google_drive():
    creds = Credentials.from_service_account_info(service_account_file, scopes=scopes)
    service = build('drive', 'v3', credentials=creds)
    return service

def download_file(url):
    file_name = title+'_'+videoID
    local_file_path = os.path.join(os.getcwd(), file_name)
    # Define your proxy server
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1',  # Do Not Track request header
    'Accept-Encoding': 'gzip, deflate, br'
    }
    # Replace this URL with the ProxyScrape API endpoint for getting proxies
    proxy_url = "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&proxy_format=protocolipport&format=text"

    # Fetch the list of proxies
    response = requests.get(proxy_url)
    proxies = response.text.split('\r\n')

    # Choose a proxy from the list
    proxy = proxies[6]  # just an example, choose a valid proxy from the list
    print(proxy)
    sys.stdout.flush()
    # Use the proxy in your requests
    proxies_dict = {
        'http': proxy,
        'https': proxy,
    }

    response = requests.get(url, headers=headers, proxies=proxies_dict)
    c=10
    # while(not(response.status_code!=404 and c>0)):
    #     response = requests.get(url,proxies=proxy)
    #     c=c-1
    with open(local_file_path,"wb") as file:
        file.write(response.content)
    return local_file_path, file_name
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    # req = urllib.request.Request(url, headers=headers)
    # try:
    #     with urllib.request.urlopen(req) as response:
    #         with open(local_file_path + '.mp3', 'wb') as file:
    #             file.write(response.read())
    #     print(f"File downloaded successfully to {local_file_path}.mp3")
    # except urllib.error.HTTPError as e:
    #     print(f"HTTP Error: {e.code} - {e.reason}")
    # except Exception as e:
    #     print(f"Error: {e}")
    return local_file_path, file_name

def download_file1(url):
    try:
        webbrowser.open(url)
    except Exception as e:
        print(e)
        sys.stdout.flush()
    print(os.path.join(os.getcwd(),title+'_'+videoID))

def upload_to_google_drive(service, file_path, file_name, folder_id=None):
    file_metadata = {'name' : file_name}
    if folder_id:
        file_metadata['parents'] = [folder_id]
    media = MediaFileUpload(file_path, mimetype="audio/mpeg") #application/octet-stream
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
    # Get the base64-encoded environment variable
    # base64_encoded_credentials = os.getenv('GOOGLE_DRIVE_JSON')

    # # Decode the base64 string
    # decoded_bytes = base64.b64decode(base64_encoded_credentials)
    # json_credentials = decoded_bytes.decode('utf-8')

    # # Load the JSON data
    # service_account_file = json.loads(json_credentials)
    # # service_account_file = "F:\Programs\Task01a\GOOGLE_DRIVE_JSON.json"
    try:
        base64_encoded_credentials = os.getenv('GOOGLE_DRIVE_JSON')
        if not base64_encoded_credentials:
            raise ValueError("GOOGLE_DRIVE_JSON environment variable is not set.")
        decoded_bytes = base64.b64decode(base64_encoded_credentials)
        json_credentials = decoded_bytes.decode('utf-8')
        service_account_file = json.loads(json_credentials)
    except Exception as e:
        print(f"Error processing Google Drive credentials: {e}")
        sys.exit(1)
    scopes = ['https://www.googleapis.com/auth/drive.file']

    print(1)
    sys.stdout.flush()

    service = authentiate_google_drive()
    url = link
    sys.stdout.flush()
    #file_path, file_name = 
    download_file1(url)
    upload_to_google_drive(service, os.path.join(os.getcwd(),title+'_'+videoID), title+'_'+videoID, folder_id='1Y_3XGo2z6miI-O9j_U9H0vEN_ea9uQ_k')

    print(2)
    sys.stdout.flush()

    import MelSpec
    MelSpec.save(title+'_'+videoID)
    saveToJson(title+'_'+videoID)
    os.remove(os.join(os.getcwd(),title+'_'+videoID))

    # print(title+'_'+videoID)
    # time.sleep(7)
    # import MelSpec
    # MelSpec.save(title+'_'+videoID)
    # saveToJson(title+'_'+videoID)
    # print(title+'_'+videoID)

sys.stdout.flush()
