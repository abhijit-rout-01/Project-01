#Mel Spectrogram of audio data

import librosa
import numpy as np
import matplotlib.pyplot as plt
import json

def save(title):

    source = "C:\\Users\\Victus\\Downloads\\" + title + ".mp3"
    #print(title)
    y, sr = librosa.load(source)

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

        fig.savefig('public\\images\\'+title+str(i)+'.jpeg')

        if(i==k-1):
            editJson(str(title),k)
        

#save("KALKI 2898 A.D - Shree Krishna (OST Kalki Theme)_ZFSUYviUY_M")
def editJson(title,k):
    # Path to the JSON file
    json_file_path = 'public\\css\\task2\\images.json'

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