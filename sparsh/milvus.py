from pymilvus import Collection

def query_milvus(embedding):
    """
    Query Milvus for similar embeddings.
    """
    # Connect to the collection
    collection = Collection("Shark_tank_india")

    # Perform the search
    results = collection.search(
        data=[embedding],
        anns_field="embedding",
        param={"metric_type": "IP", "params": {"nprobe": 10}},
        limit=5,
        output_fields=["name", "description", "location"],
    )

    # Format the results
    recommendations = [
        {"name": hit.entity.get("name"),
         "description": hit.entity.get("description"),
         "location": hit.entity.get("location")}
        for hit in results[0]
    ]

    return recommendations
