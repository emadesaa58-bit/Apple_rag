import redis
import numpy as np

from redis.commands.search.field import (
    TextField,
    NumericField,
    VectorField
)

from redis.commands.search.index_definition import (
    IndexDefinition,
    IndexType
)

from Config import (
    REDIS_URL,
    REDIS_INDEX,
    REDIS_KEY_PREFIX
)


VECTOR_DIMENSION = 768


def get_redis_connection():

    r = redis.from_url(
        REDIS_URL,
        decode_responses=False
    )

    return r


def create_index(redis_client):

    try:
        redis_client.ft(REDIS_INDEX).info()

        print("Redis index already exists.")

    except Exception:

        schema = (

            TextField("text"),

            TextField("file_name"),

            NumericField("chunk_id"),

            VectorField(
                "embedding",
                "HNSW",
                {
                    "TYPE": "FLOAT32",
                    "DIM": VECTOR_DIMENSION,
                    "DISTANCE_METRIC": "COSINE"
                }
            )
        )

        definition = IndexDefinition(
            prefix=[f"{REDIS_KEY_PREFIX}:"],
            index_type=IndexType.HASH
        )

        redis_client.ft(
            REDIS_INDEX
        ).create_index(
            schema,
            definition=definition
        )

        print("Redis index created.")


def store_vector(
    redis_client,
    embedding,
    text,
    file_name,
    chunk_id
):

    key = f"{REDIS_KEY_PREFIX}:{file_name}:{chunk_id}"

    vector = np.array(
        embedding,
        dtype=np.float32
    ).tobytes()

    redis_client.hset(
        key,
        mapping={
            "text": text,
            "file_name": file_name,
            "chunk_id": chunk_id,
            "embedding": vector
        }
    )

    return key


