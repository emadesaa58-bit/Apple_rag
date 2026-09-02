from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import os
import pickle


SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly"
]


def get_drive_service():

    creds = None

    if os.path.exists("token_drive.pickle"):
        with open("token_drive.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        with open("token_drive.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build(
        "drive",
        "v3",
        credentials=creds
    )

    return service

def get_files_from_folder(service, folder_id):

    query = (
        f"'{folder_id}' in parents "
        f"and trashed = false"
    )

    results = service.files().list(
        q=query,
        fields="files(id, name, mimeType)"
    ).execute()

    files = results.get("files", [])

    return files


def download_file(service, file_id, file_name):
    """
    Download a file from Google Drive.
    """

    request = service.files().get_media(
        fileId=file_id
    )

    file_path = os.path.join(
        "downloads",
        file_name
    )

    os.makedirs(
        "downloads",
        exist_ok=True
    )

    with open(file_path, "wb") as file:
        from googleapiclient.http import MediaIoBaseDownload

        downloader = MediaIoBaseDownload(
            file,
            request
        )

        done = False

        while not done:
            status, done = downloader.next_chunk()

    return file_path




