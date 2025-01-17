from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import List
from services.openai_embeddings import generate_embeddings
from services.milvus import query_milvus
from services.geolocation import get_geolocation

router = APIRouter()

# Define the input schema for the endpoint
class QueryRequest(BaseModel):
    query: str # i am this and this and i want this 

# Define the output schema for recommendations
class Recommendation(BaseModel):
    name: str
    description: str
    location: str

@router.post("/recommendations", response_model=List[Recommendation])
async def get_recommendations(payload: QueryRequest):
    """
    Get service provider recommendations for a startup query.
    """
    # Step 1: Generate embeddings using OpenAI
    embedding = generate_embeddings(payload.query) # query leta hai and generate_embeddings function jo ki openaiembeedings.py mein defined hai, use use karta hai and embeddings banata hai, then milvus se recommendation leta haio and returns a list of recommendations

    # Step 2: Query Milvus for similar embeddings
    recommendations = query_milvus(embedding)# this is defined in milvus.py

    # Step 3: Return the recommendations
    return recommendations

@router.get("/geolocation")
async def get_location(ip: str = Query(..., description="IP address to fetch geolocation for")):
    """
    Get geolocation details for a given IP address.
    """
    # Fetch geolocation data using the API
    location = get_geolocation(ip)
    
    # Return the location details
    return {"ip": ip, "location": location}
