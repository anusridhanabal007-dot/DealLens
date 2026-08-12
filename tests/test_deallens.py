import pytest
from app.services.normalization.normalizer import NormalizationEngine
from app.services.matching.matcher import ProductMatcherEngine
from app.services.scoring.scorer import ValueScoringEngine
from app.services.recommendation.recommender import RecommendationEngine
from app.data.demo_products import get_demo_listings_for_query

normalizer = NormalizationEngine()
matcher = ProductMatcherEngine()
scorer = ValueScoringEngine()
recommender = RecommendationEngine()

def test_normalization():
    # Storage
    assert normalizer.normalize_storage("128 GB") == "128GB"
    assert normalizer.normalize_storage("128GB") == "128GB"
    assert normalizer.normalize_storage("128-Gigabyte") == "128GB"
    assert normalizer.normalize_storage("128 G") == "128GB"
    
    # Warranty
    assert normalizer.normalize_warranty("1 Year")[0] == "12 months"
    assert normalizer.normalize_warranty("12 months")[0] == "12 months"
    assert normalizer.normalize_warranty("1 yr")[0] == "12 months"
    
    # Delivery fee
    assert normalizer.normalize_delivery_fee("Free delivery") == 0.0
    assert normalizer.normalize_delivery_fee("₹0") == 0.0
    assert normalizer.normalize_delivery_fee("No delivery fee") == 0.0
    assert normalizer.normalize_delivery_fee(0) == 0.0
    assert normalizer.normalize_delivery_fee(99) == 99.0

def test_product_matching():
    # 128GB vs 256GB = false
    l1 = {"product_name": "iPhone 15 128GB", "storage": "128GB", "model": "iPhone 15"}
    l2 = {"product_name": "iPhone 15 256GB", "storage": "256GB", "model": "iPhone 15"}
    res1 = matcher.match(l1, l2)
    assert res1["same_product"] is False
    
    # iPhone 15 vs iPhone 15 Pro = false
    l3 = {"product_name": "iPhone 15", "model": "iPhone 15"}
    l4 = {"product_name": "iPhone 15 Pro", "model": "iPhone 15 Pro"}
    res2 = matcher.match(l3, l4)
    assert res2["same_product"] is False

    # Apple iPhone 15 128GB Black vs iPhone 15 - 128 GB - Black = true
    l5 = {"product_name": "Apple iPhone 15 128GB Black", "brand": "Apple", "model": "iPhone 15", "storage": "128GB"}
    l6 = {"product_name": "iPhone 15 - 128 GB - Black", "brand": "Apple", "model": "iPhone 15", "storage": "128GB"}
    res3 = matcher.match(l5, l6)
    assert res3["same_product"] is True

def test_effective_price_and_recommendation():
    listings = get_demo_listings_for_query("iPhone 15 128GB", cross_marketplace=False)
    normalized = [normalizer.normalize_listing(l) for l in listings]
    
    listing_map = {l["id"]: l for l in normalized}
    
    # Verify exact deterministic effective prices
    assert listing_map["listing_a"]["effective_price"] == 49999.0
    assert listing_map["listing_b"]["effective_price"] == 48098.0
    assert listing_map["listing_c"]["effective_price"] == 51499.0
    
    # Calculate scores with default weights
    scores_map = scorer.calculate_scores(normalized)
    
    # Determine winner
    winner_info = recommender.determine_winner(normalized, scores_map)
    assert winner_info["winner_listing_id"] == "listing_b"

def test_missing_data_resilience():
    # Ensure missing warranty, seller rating, or delivery fee does not crash
    incomplete_listing = [
        {
            "id": "missing_1",
            "product_name": "Test Phone",
            "price": 10000.0,
            # seller_rating is missing
            # warranty is missing
            # delivery_fee is missing
        },
        {
            "id": "missing_2",
            "product_name": "Test Phone 2",
            "price": 11000.0,
            "seller_rating": 4.5,
            "warranty": "6 months",
            "delivery_fee": 100.0
        }
    ]
    norm = [normalizer.normalize_listing(l) for l in incomplete_listing]
    scores = scorer.calculate_scores(norm)
    assert "missing_1" in scores
    assert scores["missing_1"]["seller_score"] == 70.0  # fallback
    assert scores["missing_1"]["warranty_score"] == 0.0
    
    winner = recommender.determine_winner(norm, scores)
    assert winner["winner_listing_id"] in ["missing_1", "missing_2"]
