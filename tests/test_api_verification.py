import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_and_demo_queries():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"

    res_demo = client.get("/api/demo-queries")
    assert res_demo.status_code == 200
    queries = res_demo.json()
    assert "iPhone 15 128GB" in queries
    assert "Samsung Galaxy S24" in queries
    assert "Sony WH-1000XM5" in queries
    assert "MacBook Air M3" in queries

def test_compare_iphone15_benchmark():
    payload = {
        "query": "iPhone 15 128GB",
        "weights": {
            "price": 0.50,
            "seller": 0.25,
            "warranty": 0.15,
            "delivery": 0.10
        },
        "cross_platform": False
    }
    response = client.post("/api/compare", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["query"] == "iPhone 15 128GB"
    assert data["matched"] is True

    listings_map = {l["id"]: l for l in data["listings"]}
    assert listings_map["listing_a"]["effective_price"] == 49999.0
    assert listings_map["listing_b"]["effective_price"] == 48098.0
    assert listings_map["listing_c"]["effective_price"] == 51499.0

    recommendation = data["recommendation"]
    assert recommendation["winner_listing_id"] == "listing_b"
    assert recommendation["ai_mode"] == "Deterministic fallback"
    assert "48,098" in recommendation["ai_explanation"] or "48098" in recommendation["ai_explanation"]

def test_cross_platform_cheapest_vs_best_deal():
    payload = {
        "query": "iPhone 15 128GB",
        "weights": {
            "price": 0.50,
            "seller": 0.25,
            "warranty": 0.15,
            "delivery": 0.10
        },
        "cross_platform": True
    }
    response = client.post("/api/compare", json=payload)
    assert response.status_code == 200
    data = response.json()

    listings = data["listings"]
    # Check that refurbished listing D exists
    refurbished = next((l for l in listings if l["id"] == "listing_d_cross"), None)
    assert refurbished is not None

    # Refurbished raw effective price (41999 + 150 = 42149) is cheapest price
    assert refurbished["effective_price"] == 42149.0

    # BUT Listing B must STILL be the winner (cheapest listing != best overall deal)
    assert data["recommendation"]["winner_listing_id"] == "listing_b"
