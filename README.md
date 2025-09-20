# Visey Recommender Microservice

## 🚀 Overview

**Visey Recommender** is a production-deployed, content-based microservice that leverages vector similarity search to intelligently match startups with relevant businesses and funding opportunities. Designed for seamless integration into larger platforms, this stateless service processes multi-dimensional startup profiles to deliver ranked recommendations via high-performance vector database queries.

## 🎯 Core Features

- **Microservice Architecture**: Stateless, container-friendly design for easy integration and horizontal scaling
- **Content-Based Recommendations**: Semantic matching based on startup characteristics, industry focus, and location
- **Vector Similarity Search**: Utilizes high-dimensional embeddings for precise recommendation ranking
- **Dual Recommendation Domains**: Business partnerships and funding opportunity discovery
- **Production API**: RESTful endpoints with configurable result limits (1-100 matches)
- **Real-time Processing**: Asynchronous processing for high-throughput environments

## 🏗️ Technology Stack

- **Backend**: FastAPI with Python 3.x
- **AI/ML**: OpenAI text-embedding-3-large (500-dimensional vectors)
- **Vector Database**: Milvus for scalable similarity search
- **Geolocation**: Google Maps Geocoding API
- **Deployment**: Heroku & Docker with Gunicorn WSGI server
- **Data Validation**: Pydantic models for strict input checking

## 📊 API Endpoints

### Business Recommendations
- `POST /business/get_recommendations/` - Returns ranked list of matching businesses
- `POST /business/data_insert/` - Add new business profiles to the system

### Opportunity Matching
- `POST /opportunity/get_recommendations/` - Discover relevant funding opportunities
- `POST /opportunity/data_insert/` - Register new opportunities

## 🔧 Input & Configuration

### Startup Profile JSON
```json
{
  "id": "string",
  "name": "string", 
  "location": "string",
  "industry": "string",
  "sector": "string",
  "trllevel":  integer
}
```

### Query Parameters
- **limit**: Number of recommendations (default: 10, max: 100)

### Environment Variables
- `OPENAI_API_KEY`
- `ZILLI_URL`, `ZILLI_TOKEN`
- `GEOLOCATOR_API_KEY`

## ⚡ System Capabilities

- **Multi-Modal Analysis**: Combines textual, geographic, and categorical data
- **Weighted Scoring**: Configurable importance factors for each data dimension
- **Scalable Deployment**: Docker-ready and cloud-native for rapid scaling
- **Geospatial Intelligence**: Address-to-coordinate conversion for proximity matching

## 📦 Deployment Guide

```bash
# Build Docker image
docker build -t visey-recommender:latest .

# Run microservice
docker run -d -p 8000:8000 \
  -e OPENAI_API_KEY=your_key \
  -e ZILLI_URL=your_endpoint \
  -e ZILLI_TOKEN=your_token \
  -e GEOLOCATOR_API_KEY=your_key \
  visey-recommender:latest
```

## 📈 Use Cases

- **Startup Ecosystems**
- **Investment Platforms**
- **Enterprise Solutions**

---

**Status**: Production Deployed Microservice  
**Version**: 1.3.1  
**API**: RESTful with OpenAPI embedding support