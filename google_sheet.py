from googleapiclient.discovery import build


def get_sheets_service(drive_service):
    """
    Create Google Sheets service using the same Google credentials
    used for Google Drive.
    """

    credentials = drive_service._http.credentials

    service = build(
        "sheets",
        "v4",
        credentials=credentials
    )

    return service


def get_sheet_files(service, spreadsheet_id):
    """
    Get all rows from the Google Sheet.
    """

    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range="A:Z"
    ).execute()

    rows = result.get("values", [])

    return rows



