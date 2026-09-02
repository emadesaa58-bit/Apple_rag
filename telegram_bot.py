from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters
)

from Config import TELEGRAM_BOT_TOKEN

from vector_search import search_vectors
from ai_agent import generate_answer

from vector_store import get_redis_connection


# الاتصال بـ Redis
redis_client = get_redis_connection()


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    question = update.message.text

    print("\nUser question:")
    print(question)

    # =========================
    # Vector Search
    # =========================

    results = search_vectors(
        redis_client,
        question,
        top_k=5
    )

    # =========================
    # Build Context
    # =========================

    retrieved_context = ""

    for result in results:

        retrieved_context += f"""
File: {result['file_name']}
Chunk: {result['chunk_id']}

{result['text']}

-------------------------
"""

    # =========================
    # Gemini Answer
    # =========================

    answer = generate_answer(
        question,
        retrieved_context
    )

    print("\nGemini answer:")
    print(answer)

    # =========================
    # Send Answer to Telegram
    # =========================

    await update.message.reply_text(
        answer
    )


def start_telegram_bot():

    app = Application.builder().token(
        TELEGRAM_BOT_TOKEN
    ).build()

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    print("\n===== Telegram Bot =====")
    print("Bot is running...")

    app.run_polling()