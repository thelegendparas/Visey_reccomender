from fastapi import FastAPI, Query
from pydantic import BaseModel, conlist

from logic import generate_embedding, insert_data_milvus, search_data_milvus, transform_address
from logic import combine_embeddings_with_weights


class Business(BaseModel):
    id: str
    name: str
    location: str
    category: str
    categoryTags: str
    description: str


class Vector(BaseModel):
    embedding: conlist(float, min_length=500, max_length=500)


app = FastAPI(
    title="content_based recommendation",
    version="1.0.0"
)


@app.post("/get_reccomendations/")
def get_matches(vector: Vector, limit: int = Query(default=10, ge=0, le=100)):
    ids = search_data_milvus(vector.embedding, limit)

    return {
        "status_code": "OK",
        "content": ids
    }


@app.post("/data_insert/")
def insert_data(business: Business):
    name_vector = generate_embedding(business.name)
    coords = transform_address(business.location)
    location_vector = generate_embedding(f"{coords[0]},{coords[1]}")
    description_vector = generate_embedding(business.description)
    category_vector = generate_embedding(f"{business.category} + {business.categoryTags}")

    weights = [1, 2, 3, 4]
    embeddings = [name_vector, location_vector, description_vector, category_vector]

    embedding = combine_embeddings_with_weights(embeddings, weights)

    response = insert_data_milvus(business.id, business.location, business.category, embedding)

    return response
