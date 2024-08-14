#Mel Spectrogram of audio data

import librosa
import numpy as np
import matplotlib.pyplot as plt
import os
import json
import requests
import base64
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def save(title):

    #source = response_content
    #print(title)
    y, sr = librosa.load(os.join(os.getcwd(),title))

    partLen = 10
    k = int(len(y)/(partLen*sr))

    c=0
    j=0
    for i in range(0,k):
        #print(c+sr*partLen+1)
        z = np.array(y[c])
        #print(c/sr)
        for j in range(c+1,c+sr*partLen+1):
            #print(j)
            z = np.append(z,y[j])
        c = j
        #print(2)
        D = librosa.stft(z)
        S_db = librosa.amplitude_to_db(np.abs(D),ref=np.max)

        fig, ax = plt.subplots(figsize = (10,5))
        img = librosa.display.specshow(S_db, x_axis='time', y_axis='log', ax=ax)
        ax.set_title('Spectogram', fontsize=20)
        #plt.show()
        
        base64_encoded_credentials = os.getenv('GOOGLE_DRIVE_JSON')

        # Decode the base64 string
        decoded_bytes = base64.b64decode(base64_encoded_credentials)
        json_credentials = decoded_bytes.decode('utf-8')

        # Load the JSON data
        service_account_file = json.loads(json_credentials)
        # service_account_file = "F:\Programs\Task01a\GOOGLE_DRIVE_JSON.json"
        scopes = ['https://www.googleapis.com/auth/drive.file']
        
        service = authentiate_google_drive(service_account_file, scopes)
        
        local_file_path = os.path.join(os.getcwd(), title+str(i))
        fig.savefig(local_file_path)
        upload_to_google_drive(service, local_file_path, title+str(i), folder_id='1zD4Zh5yWHQyA4TgGSSDpdMf78FDu-jF1')
        #fig.clear()
        os.remove(local_file_path+'.png')

        print(1)
        if(i==k-1):
            editJson(str(title),k)
        

#save("KALKI 2898 A.D - Shree Krishna (OST Kalki Theme)_ZFSUYviUY_M")
def editJson(title,k):
    # Path to the JSON file
    json_file_path = os.path.join(os.getcwd(),'public/css/task2/images.json')

    for i in range(0,k):
        # New images to be added
        new_images = [
            "/images/"+title+str(i)+".jpeg",
        ]

        # Step 1: Load the existing JSON data
        try:
            with open(json_file_path, 'r') as file:
                images = json.load(file)
        except FileNotFoundError:
            images = []  # If the file doesn't exist, start with an empty list

        # Step 2: Add new images to the list
        images.extend(new_images)

        # Step 3: Save the updated list back to the JSON file
        with open(json_file_path, 'w') as file:
            json.dump(images, file, indent=4)

def authentiate_google_drive(service_account_file, scopes):
    creds = Credentials.from_service_account_info(service_account_file, scopes=scopes)
    service = build('drive', 'v3', credentials=creds)
    return service

def upload_to_google_drive(service, file_path, file_name, folder_id=None):
    file_metadata = {'name' : file_name}
    if folder_id:
        file_metadata['parents'] = [folder_id]
    media = MediaFileUpload(file_path+'.png', mimetype="application/octet-stream")
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()