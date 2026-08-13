import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_endpoints_existence():
    """Verify all standard API endpoints work."""
    # GET /health
    r_health = client.get("/health")
    assert r_health.status_code == 200
    assert r_health.json()["status"] == "ok"

    # GET /api/demo-queries
    r_demo = client.get("/api/demo-queries")
    assert r_demo.status_code == 200
    assert len(r_demo.json()) >= 4

    # POST /api/search
    r_search = client.post("/api/search?query=iPhone%2015%20128GB")
    assert r_search.status_code == 200
    assert r_search.json()["count"] > 0

    # POST /api/extract
    r_extract = client.post("/api/extract", json={"raw_title": "iPhone 15 128GB", "raw_price": 50000})
    assert r_extract.status_code == 200
    assert r_extract.json()["condition"] is not None

    # POST /api/match
    r_match = client.post("/api/match", json={
        "listing_a": {"product_name": "iPhone 15 128GB", "storage": "128GB"},
        "listing_b": {"product_name": "iPhone 15 128GB", "storage": "128GB"}
    })
    assert r_match.status_code == 200
    assert r_match.json()["same_product"] is True

def test_invalid_weights_validation():
    """Verify backend returns HTTP 400 for invalid total weight = 120."""
    payload = {
        "query": "iPhone 15 128GB",
        "weights": {
            "price": 50,
            "seller": 20,
            "warranty": 20,
            "delivery": 30
        },
        "cross_platform": False
    }
    res = client.post("/api/compare", json=payload)
    assert res.status_code == 400
    err_detail = res.json()["detail"]
    assert "Invalid weight" in err_detail or "Total weights must equal" in err_detail

@pytest.mark.parametrize("query", [
    "iPhone 15 128GB",
    "Samsung Galaxy S24",
    "Sony WH-1000XM5",
    "MacBook Air M3"
])
def test_all_products_with_three_weight_cases(query):
    cases = [
        {"name": "Case A", "weights": {"price": 70, "seller": 15, "warranty": 10, "delivery": 5}},
        {"name": "Case B", "weights": {"price": 30, "seller": 40, "warranty": 20, "delivery": 10}},
        {"name": "Case C", "weights": {"price": 20, "seller": 20, "warranty": 50, "delivery": 10}}
    ]

    last_scores = None

    for case in cases:
        weights = case["weights"]
        total = sum(weights.values())
        assert total == 100

        res = client.post("/api/compare", json={
            "query": query,
            "weights": weights,
            "cross_platform": False
        })

        assert res.status_code == 200
        data = res.json()

        # Check winner selection
        scores_map = data["scores"]
        winner_id = data["recommendation"]["winner_listing_id"]

        # Verify winner actually has highest calculated overall_score
        max_id = max(scores_map.keys(), key=lambda lid: scores_map[lid]["overall_score"])
        assert winner_id == max_id, f"Expected winner {max_id} but got {winner_id} for {query} with {case['name']}"

        # Verify scores change between weight cases
        if last_scores is not None:
            assert scores_map != last_scores, f"Scores did not change for {query} between weight cases"
        last_scores = scores_map

        # Verify recommendation text mentions winner listing ID or product name
        exp = data["recommendation"]["ai_explanation"]
        assert winner_id in exp or data["listings"][0]["product_name"] in exp or "recommended" in exp.lower()

def test_cross_platform_toggle_behavior():
    # Cross Platform OFF
    res_off = client.post("/api/compare", json={"query": "iPhone 15 128GB", "cross_platform": False})
    assert res_off.status_code == 200
    listings_off = res_off.json()["listings"]

    # Cross Platform ON
    res_on = client.post("/api/compare", json={"query": "iPhone 15 128GB", "cross_platform": True})
    assert res_on.status_code == 200
    listings_on = res_on.json()["listings"]

    # Refurbished outlet is excluded when OFF (3 listings), included when ON (4 listings)
    assert len(listings_off) == 3
    assert len(listings_on) == 4
    assert any("Refurbished" in l["platform"] or "Used" in l.get("condition", "") for l in listings_on)
    assert not any("Refurbished" in l["platform"] or "Used" in l.get("condition", "") for l in listings_off)
