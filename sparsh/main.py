from fastapi import FastAPI
from api.routes import router
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Recommendation API",
    description="API for business recommendations using OpenAI, Google Maps, and Milvus.",
    version="1.0.0"
)

# Include routes
app.include_router(router)

# Health check endpoint
@app.get("/")
async def health_check():
    return {"status": "running", "message": "Welcome to the Recommendation API!"}
