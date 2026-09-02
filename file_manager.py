def find_new_files(drive_files, sheet_rows):
    """
    Compare Google Drive files with Google Sheet
    and return only new files.
    """

    # IDs of files already stored in Google Sheet
    indexed_file_ids = set()

    for row in sheet_rows[1:]:
        if len(row) >= 2:
            file_id = row[1]
            indexed_file_ids.add(file_id)

    # Find files that are not in the Sheet
    new_files = []

    for file in drive_files:

        if file["id"] not in indexed_file_ids:
            new_files.append(file)

    return new_files



