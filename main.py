from Config import (
    GOOGLE_DRIVE_FOLDER_ID,
    GOOGLE_SHEET_ID
)

from google_drive import (
    get_drive_service,
    get_files_from_folder,
    download_file
)

from google_sheet import (
    get_sheets_service,
    get_sheet_files
)

from file_manager import (
    find_new_files
)

from document_processor import (
    extract_text_from_pdf,
    split_text
)

from embeddings import (
    create_embedding
)

from vector_store import (
    get_redis_connection,
    create_index,
    store_vector
)


from vector_search import search_vectors
from ai_agent import generate_answer
from telegram_bot import start_telegram_bot

def main():

    # =========================
    # Google Drive
    # =========================

    drive_service = get_drive_service()

    drive_files = get_files_from_folder(
        drive_service,
        GOOGLE_DRIVE_FOLDER_ID
    )

    print("\n===== Google Drive Files =====")

    for file in drive_files:
        print(
            file["name"],
            file["id"]
        )


    # =========================
    # Google Sheets
    # =========================

    sheets_service = get_sheets_service(
        drive_service
    )

    sheet_files = get_sheet_files(
        sheets_service,
        GOOGLE_SHEET_ID
    )

    print("\n===== Google Sheet =====")

    for row in sheet_files:
        print(row)


    # =========================
    # Find New Files
    # =========================

    new_files = find_new_files(
        drive_files,
        sheet_files
    )

    print("\n===== New Files =====")

    for file in new_files:
        print(
            file["name"],
            file["id"]
        )


    # =========================
    # Redis Connection
    # =========================

    redis_client = get_redis_connection()

    print("\n===== Redis Test =====")
    print(redis_client.ping())

    create_index(redis_client)


    # =========================
    # Download + Extract
    # + Split + Embeddings
    # + Redis
    # =========================

    for file in new_files:

        # -------------------------
        # Download
        # -------------------------

        file_path = download_file(
            drive_service,
            file["id"],
            file["name"]
        )

        print(
            "\nDownloaded:",
            file_path
        )


        # -------------------------
        # Extract Text
        # -------------------------

        text = extract_text_from_pdf(
            file_path
        )

        print(
            "\n===== Extracted Text ====="
        )

        print(
            text[:500]
        )


        # -------------------------
        # Split Text
        # -------------------------

        chunks = split_text(
            text
        )

        print(
            "\n===== Chunks ====="
        )

        print(
            "Number of chunks:",
            len(chunks)
        )


        # -------------------------
        # Create Embeddings
        # + Store in Redis
        # -------------------------

        for i, chunk in enumerate(chunks):

            print(
                f"\nCreating embedding "
                f"{i + 1}/{len(chunks)}"
            )

            embedding = create_embedding(
                chunk
            )


            key = store_vector(
                redis_client,
                embedding,
                chunk,
                file["name"],
                i
            )

            print(
                "Stored:",
                key
            )
        print("\n===== Vector Search Test =====")

        question = "What was Apple's total net sales?"

        results = search_vectors(
        redis_client,
        question,
        top_k=5
        )

        for result in results:

            print("\n-------------------------")

            print("File:", result["file_name"])

            print("Chunk:", result["chunk_id"])

            print("Score:", result["score"])

            print("Text:")

            print(result["text"][:500])   

    context = ""

    for result in results:

        context += f"""
    File: {result['file_name']}
    Chunk: {result['chunk_id']}

    {result['text']}

-------------------------
"""


    answer = generate_answer(
    question,
    context
        )

    print("\n===== Gemini Answer =====")

    print(answer) 
    print("\nStarting Telegram Bot...")

    start_telegram_bot()       


# =========================
# Start Program
# =========================

if __name__ == "__main__":
    main()




    