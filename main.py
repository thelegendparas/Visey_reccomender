import asyncio

from fastapi import FastAPI, Query
from pydantic import BaseModel, conlist

from logic import generate_embedding, insert_data_milvus, search_data_milvus, transform_address
from logic import combine_embeddings_with_weights, convert_list_str


class Business(BaseModel):
    id: str
    name: str
    location: str
    category: str
    categoryTags: conlist(str)
    description: str


class Startup(BaseModel):
    id: str
    name: str
    location: str
    industry: str
    sector: str
    trllevel: int


class Vector(BaseModel):
    embedding: conlist(float, min_length=500, max_length=500)


app = FastAPI(
    title="content_based recommendation",
    version="1.0.0"
)


@app.post("/get_reccomendations/")
async def get_matches(startup: Startup, limit: int = Query(default=10, ge=0, le=100)):
    coords = transform_address(startup.location)

    embeddings = await asyncio.gather(
        generate_embedding(startup.name),
        generate_embedding(f"{coords[0]},{coords[1]}"),
        generate_embedding(f"{startup.industry} + {startup.sector}")
    )

    weights = [1, 3, 6]
    embeddings = [embeddings[0], embeddings[1], embeddings[2]]
    embedding = combine_embeddings_with_weights(embeddings, weights)

    ids = search_data_milvus(embedding, limit)

    return {
        "status_code": "OK",
        "content": ids
    }


@app.post("/data_insert/")
async def insert_data(business: Business):
    coords = transform_address(business.location)
    category_tags_string = convert_list_str(business.categoryTags)
    embeddings = await asyncio.gather(generate_embedding(business.name), generate_embedding(f"{coords[0]},{coords[1]}"),
                                      generate_embedding(business.description),
                                      generate_embedding(f"{business.category} + {category_tags_string}"))

    name_vector = embeddings[0]
    location_vector = embeddings[1]
    description_vector = embeddings[2]
    category_vector = embeddings[3]
    weights = [1, 2, 3, 4]
    embeddings = [name_vector, location_vector, description_vector, category_vector]

    embedding = combine_embeddings_with_weights(embeddings, weights)

    response = insert_data_milvus(business.id, business.location, business.category, embedding)

    return response
