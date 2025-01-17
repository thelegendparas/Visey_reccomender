from fastapi import FastAPI
from pydantic import BaseModel

from logic import Zilli_url,Zilli_token
from logic import generate_embedding, insert_data_milvus, search_data_milvus, transform_address
from logic import combine_embeddings_with_weights

class Business(BaseModel):
    id: str
    name: str
    location: str
    category: str
    categoryTags: str
    description: str

app = FastAPI(
    title="content_based recommendation",
    version="1.0.0"
)



@app.post("/data_insert/")
async def insert_data(business: Business):
    coords = transform_address(business.location)
    name_vector = await generate_embedding(business.name)
    location_vector = await generate_embedding(coords)
    description_vector = await generate_embedding(business.description)
    category_vector = await generate_embedding(business.category + business.categoryTags)

    weights = [1,2,3,4]
    embeddings = [name_vector,location_vector, description_vector,category_vector]

    embedding = combine_embeddings_with_weights(embeddings,weights)

    response = insert_data_milvus(business.id,business.location,business.category,embedding)

    return response
