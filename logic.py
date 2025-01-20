# To import the necessary token and url values
import os
from dotenv import load_dotenv, dotenv_values
import numpy as np

# Loading all the token values
Zilli_url = os.getenv("ZILLI_URL")
Zilli_token = os.getenv("ZILLI_TOKEN")

OpenAI_API_Key = os.getenv("OPENAI_API_KEY")

Geolocator_API_Key = os.getenv("GEOLOCATOR_API_KEY")
# Openapi embedding generation code
import requests


def generate_embedding(input: str):
    # payload
    data = {
        "input": input,
        "dimensions": 500,
        "model": "text-embedding-3-large"
    }

    # Headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OpenAI_API_Key}"
    }

    response = requests.post(url="https://api.openai.com/v1/embeddings",
                             headers=headers, json=data)

    if response.status_code != 200:
        raise Exception(f"Failed to generate embedding: {response.status_code} , {response.reason}")

    response = response.json()

    return response["data"][0]['embedding']


def insert_data_milvus(id: str, location: str, category: str, vector: list):
    url = Zilli_url + "insert"

    payload = {
        "collectionName": "content_based",
        "data": [
            {
                "primary_key": id,
                "location": location,
                "category": category,
                "vector": vector
            }
        ]
    }

    headers = {
        "Authorization": Zilli_token,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.post(url=url, json=payload, headers=headers)

    return {
        "status_code": response.status_code,
        "content": response.json()
    }


def extract_ids(data: list):
    ids = []
    for entries in data:
        vector_id = entries['id']
        ids.append(vector_id)
    return ids


def search_data_milvus(vector: list, limit: int):
    url = Zilli_url + "search"

    payload = {
        "collectionName": "content_based",
        "data": [vector],
        "limit": limit,
        "outputFields": ["primary_key"]
    }

    headers = {
        "Authorization": Zilli_token,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()['data']
    ids = extract_ids(data)
    return ids


def transform_address(address: str):
    api_key = Geolocator_API_Key
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
    response = requests.get(url=url)
    data = response.json()

    # To check if the request has been successfully made or not
    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']

        return [location['lat'], location['lng']]
    else:
        return data.json()


def combine_embeddings_with_weights(embeddings: list, weights: list):
    # Initialize an empty array for the final embedding
    final_embedding = np.zeros_like(embeddings[0])

    # Combine embeddings based on their weights
    for i in range(len(embeddings)):
        final_embedding += np.array(embeddings[i]) * weights[i]

    # Normalise by the total weight to keep the scale consistent
    total_weight = sum(weights)
    final_embedding /= total_weight

    final_embedding = final_embedding.tolist()

    return final_embedding


def convert_list_str(tags: list) -> str:
    return " ".join(tags)


if __name__ == "__main__":
    def test1_insertions():
        # writing test cases here
        response = generate_embedding("testing tesbewbting, 1 2 3")

        response = insert_data_milvus("121425234", '2124124124', '21251241', (response))
        print(response)


    def test2_searches():
        # writing test cases here
        response = generate_embedding("testing testing, 1 2 3")

        response = search_data_milvus(response)
        print(response)


    def test3_geo_locator():
        address = "Hari Nagar New Delhi, 110064"
        response = transform_address(address)
        print(response)


    def test_generate_embedding():
        response = generate_embedding("testing testing, 1 2 3")
        print(response)


    def test_tag_string():
        tags = ["pokemon", "fireshow", "pikachu"]
        x = convert_list_str(tags)
        print(x)

    test_tag_string()

