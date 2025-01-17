import openai
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from services.geolocation import get_lat_lon

# OpenAI API Key
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

def generate_combined_embeddings(business_name: str, business_industry: str, business_description: str, business_location: str):
    """
    Generate embeddings for a business using multiple fields.

    Args:
        business_name (str): The name of the business.
        business_industry (str): The industry of the business.
        business_description (str): The description of the business.
        business_location (str): The location of the business.

    Returns:
        list: A list of floats representing the combined embedding, or None if an error occurs.
    """
    try:
        # Convert business_location to latitude and longitude
        lat, lon = get_lat_lon(business_location)
        if lat is None or lon is None:
            print("Error: Unable to fetch latitude and longitude for the location.")
            return None
        
        # Combine all fields into a single string
        combined_input = f"{business_name}, {business_industry}, {business_description}, located at latitude {lat} and longitude {lon}"
        
        # Generate embeddings using OpenAI API
        response = openai.Embedding.create(
            input=combined_input,
            model="text-embedding-ada-002"
        )
        embedding = response['data'][0]['embedding']
        return embedding
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return None

# Test the function
if __name__ == "__main__":
    # Example business data
    test_name = "Test Business"
    test_industry = "Technology"
    test_description = "A startup focused on AI-driven solutions."
    test_location = "Delhi Technological University, Rohini, New Delhi"

    embedding = generate_combined_embeddings(test_name, test_industry, test_description, test_location)
    if embedding:
        print(f"Embedding length: {len(embedding)}")
        print(f"Sample embedding values: {embedding[:5]}")
