from google import genai

from Config import (
    GEMINI_API_KEY,
    GEMINI_CHAT_MODEL
)


client = genai.Client(
    api_key=GEMINI_API_KEY
)


SYSTEM_PROMPT = """
You are an AI assistant specialized in Apple's financial reports.

When the user asks a question about Apple financial information,
you MUST use the retrieved information from the Apple financial reports.

Do not answer Apple financial questions from your general knowledge.

Use the retrieved information as the source of truth.

If the retrieved information does not contain the requested information,
say that the information was not found in the provided Apple financial reports.

Answer clearly and directly.

For numerical questions, pay close attention to the reporting period and date.
"""


def generate_answer(question, context):

    prompt = f"""
{SYSTEM_PROMPT}

Retrieved information from Apple financial reports:

{context}

User question:

{question}

Answer the question using only the retrieved information.
"""

    response = client.models.generate_content(
        model=GEMINI_CHAT_MODEL,
        contents=prompt
    )

    return response.text