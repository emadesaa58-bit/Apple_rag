import numpy as np

from redis.commands.search.query import Query

from embeddings import create_embedding

from Config import REDIS_INDEX


def search_vectors(redis_client, question, top_k=5):

    # Create embedding for the question
    query_embedding = create_embedding(question)

    # Convert embedding to FLOAT32 bytes
    query_vector = np.array(
        query_embedding,
        dtype=np.float32
    ).tobytes()

    # KNN search
    query = (
        Query(
            f"*=>[KNN {top_k} @embedding $vector AS score]"
        )
        .sort_by("score")
        .return_fields(
            "text",
            "file_name",
            "chunk_id",
            "score"
        )
        .paging(0, top_k)
        .dialect(2)
    )

    results = redis_client.ft(
        REDIS_INDEX
    ).search(
        query,
        query_params={
            "vector": query_vector
        }
    )

    documents = []

    for doc in results.docs:

        documents.append({
            "text": doc.text,
            "file_name": doc.file_name,
            "chunk_id": doc.chunk_id,
            "score": doc.score
        })

    return documents