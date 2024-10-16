import os
import requests
import time
from creds import USERNAME, PASSWORD

UPLOAD_FOLDERS = "upload_folders.txt"
UPLOADED_CLIPS_FILE_NAME = "uploaded_clips.txt"
STREAMABLE_UPLOAD_URL = "https://api.streamable.com/upload"
FREQUENCY_SECONDS = 60 # check and upload clips every x amount of seconds

def loadUploadedClips():
    """
    return set of the file names of all previously uploaded clips
    """
    with open(UPLOADED_CLIPS_FILE_NAME, "r") as file:
        return set([line.strip() for line in file.readlines()])

def loadUploadFolders():
    """
    return array of all folder paths to upload videos from
    """
    with open(UPLOAD_FOLDERS, "r") as file:
        return [line.strip() for line in file.readlines()]

def saveClip(clipPath):
    """
    saves clip name in txt file containing uploaded clip names
    """
    with open(UPLOADED_CLIPS_FILE_NAME, "a") as file:
        file.write(clipPath + "\n")

def uploadClip(path):
    files = {"file": open(path, "rb")}
    clipTitle = path.split("\\")[-1]
    response = requests.post(STREAMABLE_UPLOAD_URL, files = files, auth = (USERNAME, PASSWORD), data = {"title": clipTitle})
    if response.status_code == 200:
        return response.json()["shortcode"]
    return None

def main():
    uploadedClips = loadUploadedClips() # each uploaded clip's file path
    while True:
        uploadFolderPaths = loadUploadFolders()
        newClips = set()
        for folderPath in uploadFolderPaths:
            if os.path.exists(folderPath):
                for fileName in os.listdir(folderPath):
                    filePath = os.path.join(folderPath,fileName)
                    if filePath not in uploadedClips:
                        newClips.add(filePath)

        for clipPath in newClips:
            shortcode = uploadClip(clipPath)
            clipFileName = os.path.basename(clipPath)
            if shortcode:
                saveClip(clipPath)
                print(f"{clipFileName} uploaded successfully")
            else:
                print(f"{clipFileName} failed to upload")
        time.sleep(FREQUENCY_SECONDS)
        uploadedClips = loadUploadedClips()



if __name__ == "__main__":
    main()
