import sys
import webbrowser
import time
import json


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

data_back = "Yes"

link = sys.argv[1]
title = sys.argv[2]
title = change(title)
videoID = sys.argv[3]

if(isPresent(title+'_'+videoID)):
    print("Song already taken try another one")
else:
    webbrowser.open_new_tab(link)

    time.sleep(7)
    import MelSpec
    MelSpec.save(title+'_'+videoID)
    saveToJson(title+'_'+videoID)
    print(title+'_'+videoID)

sys.stdout.flush()
