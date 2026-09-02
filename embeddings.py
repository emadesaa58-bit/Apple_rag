from google import genai
from google.genai import types

from Config import GEMINI_API_KEY


client = genai.Client(
    api_key=GEMINI_API_KEY
)


def create_embedding(text):

    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_DOCUMENT",
            output_dimensionality=768
        )
    )

    return result.embeddings[0].values

