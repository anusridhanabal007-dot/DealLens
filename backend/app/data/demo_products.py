from typing import Dict, List, Any

DEMO_DATASETS: Dict[str, List[Dict[str, Any]]] = {
    "iphone 15 128gb": [
        {
            "id": "listing_a",
            "platform": "Demo Marketplace A",
            "product_name": "Apple iPhone 15 128GB Black",
            "brand": "Apple",
            "model": "iPhone 15",
            "variant": "Standard",
            "storage": "128GB",
            "ram": "6GB",
            "color": "Black",
            "condition": "New",
            "price": 49999.0,
            "currency": "INR",
            "delivery_fee": 0.0,
            "seller_name": "TechWorld Premier",
            "seller_rating": 4.5,
            "seller_review_count": 1240,
            "warranty": "1 Year Official Apple Warranty",
            "warranty_months": 12,
            "return_policy": "7-day replacement",
            "delivery_days": 2,
            "availability": "In Stock",
            "important_specifications": {
                "Display": "6.1-inch Super Retina XDR",
                "Chipset": "A16 Bionic",
                "Camera": "48MP Main + 12MP Ultra Wide"
            },
            "product_url": "https://example-marketplace-a.com/item/iphone15-128gb",
            "image_url": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=600&auto=format&fit=crop",
            "source_type": "demo"
        },
        {
            "id": "listing_b",
            "platform": "Demo Marketplace B",
            "product_name": "Apple iPhone 15 128 GB Black",
            "brand": "Apple",
            "model": "iPhone 15",
            "variant": "Standard",
            "storage": "128GB",
            "ram": "6GB",
            "color": "Black",
            "condition": "New",
            "price": 47999.0,
            "currency": "INR",
            "delivery_fee": 99.0,
            "seller_name": "iStore Direct Verified",
            "seller_rating": 4.8,
            "seller_review_count": 3450,
            "warranty": "12 months Manufacturer Warranty",
            "warranty_months": 12,
            "return_policy": "10-day return policy",
            "delivery_days": 1,
            "availability": "In Stock",
            "important_specifications": {
                "Display": "6.1-inch Super Retina XDR",
                "Chipset": "A16 Bionic",
                "Camera": "48MP Main + 12MP Ultra Wide"
            },
            "product_url": "https://example-marketplace-b.com/item/iphone15-black-128gb",
            "image_url": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=600&auto=format&fit=crop",
            "source_type": "demo"
        },
        {
            "id": "listing_c",
            "platform": "Demo Marketplace C",
            "product_name": "Apple iPhone 15 128GB Black",
            "brand": "Apple",
            "model": "iPhone 15",
            "variant": "Standard",
            "storage": "128GB",
            "ram": "6GB",
            "color": "Black",
            "condition": "New",
            "price": 51499.0,
            "currency": "INR",
            "delivery_fee": 0.0,
            "seller_name": "GadgetHub Official",
            "seller_rating": 4.2,
            "seller_review_count": 890,
            "warranty": "1 Year Warranty",
            "warranty_months": 12,
            "return_policy": "7-day return",
            "delivery_days": 3,
            "availability": "In Stock",
            "important_specifications": {
                "Display": "6.1-inch Super Retina XDR",
                "Chipset": "A16 Bionic",
                "Camera": "48MP Main + 12MP Ultra Wide"
            },
            "product_url": "https://example-marketplace-c.com/item/apple-iphone-15-128gb",
            "image_url": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=600&auto=format&fit=crop",
            "source_type": "demo"
        },
        {
            "id": "listing_d_cross",
            "platform": "Refurbished Outlet X",
            "product_name": "Apple iPhone 15 128GB Black (Pre-owned Like New)",
            "brand": "Apple",
            "model": "iPhone 15",
            "variant": "Standard",
            "storage": "128GB",
            "ram": "6GB",
            "color": "Black",
            "condition": "Used - Like New",
            "price": 41999.0,
            "currency": "INR",
            "delivery_fee": 150.0,
            "seller_name": "BargainBazaar Seller",
            "seller_rating": 3.9,
            "seller_review_count": 140,
            "warranty": "3 Months Seller Warranty",
            "warranty_months": 3,
            "return_policy": "3-day replacement only",
            "delivery_days": 5,
            "availability": "In Stock",
            "important_specifications": {
                "Display": "6.1-inch Super Retina XDR",
                "Chipset": "A16 Bionic",
                "Camera": "48MP Main + 12MP Ultra Wide"
            },
            "product_url": "https://example-refurbished.com/item/iphone15-used",
            "image_url": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=600&auto=format&fit=crop",
            "source_type": "demo"
        }
    ],
    
    "samsung galaxy s24": [
        {
            "id": "s24_a",
            "platform": "Marketplace Alpha",
            "product_name": "Samsung Galaxy S24 5G 256GB Onyx Black",
            "brand": "Samsung",
            "model": "Galaxy S24",
            "variant": "5G",
            "storage": "256GB",
            "ram": "8GB",
            "color": "Onyx Black",
            "condition": "New",
            "price": 64999.0,
            "currency": "INR",
            "delivery_fee": 0.0,
            "seller_name": "Samsung Official Store",
            "seller_rating": 4.9,
            "seller_review_count": 5200,
            "warranty": "1 Year Brand Warranty",
            "warranty_months": 12,
            "return_policy": "14-day return",
            "delivery_days": 1,
            "availability": "In Stock",
            "important_specifications": {
                "Display": "6.2-inch Dynamic AMOLED 2X",
                "Processor": "Exynos 2400",
                "Battery": "4000 mAh"
            },
            "product_url": "https://example-alpha.com/s24-256gb",
            "image_url": "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=600&auto=format&fit=crop",
            "source_type": "demo"
        },
        {
            "id": "s24_b",
            "platform": "Marketplace Beta",
            "product_name": "Samsung Galaxy S24 256 GB Onyx Black",
            "brand": "Samsung",
            "model": "Galaxy S24",
            "variant": "5G",
            "storage": "256GB",
            "ram": "8GB",
            "color": "Onyx Black",
            "condition": "New",
            "price": 62999.0,
            "currency": "INR",
            "delivery_fee": 250.0,
            "seller_name": "Express Electronics",
            "seller_rating": 4.6,
            "seller_review_count": 1890,
            "warranty": "12 months Warranty",
            "warranty_months": 12,
            "return_policy": "7-day replacement",
            "delivery_days": 2,
            "availability": "In Stock",
            "important_specifications": {
                "Display": "6.2-inch Dynamic AMOLED 2X",
                "Processor": "Exynos 2400",
                "Battery": "4000 mAh"
            },
            "product_url": "https://example-beta.com/galaxy-s24",
            "image_url": "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=600&auto=format&fit=crop",
            "source_type": "demo"
        },
        {
            "id": "s24_c",
            "platform": "Marketplace Gamma",
            "product_name": "Samsung Galaxy S24 5G (Onyx Black, 256 GB)",
            "brand": "Samsung",
            "model": "Galaxy S24",
            "variant": "5G",
            "storage": "256GB",
            "ram": "8GB",
            "color": "Onyx Black",
            "condition": "New",
            "price": 63499.0,
            "currency": "INR",
            "delivery_fee": 0.0,
            "seller_name": "MobileZone Super",
            "seller_rating": 4.4,
            "seller_review_count": 670,
            "warranty": "1 Year Brand Warranty",
            "warranty_months": 12,
            "return_policy": "7-day return",
            "delivery_days": 3,
            "availability": "In Stock",
            "important_specifications": {
                "Display": "6.2-inch Dynamic AMOLED 2X",
                "Processor": "Exynos 2400",
                "Battery": "4000 mAh"
            },
            "product_url": "https://example-gamma.com/s24-onyx-black",
            "image_url": "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=600&auto=format&fit=crop",
            "source_type": "demo"
        }
    ],

    "sony wh-1000xm5": [
        {
            "id": "sony_a",
            "platform": "AudioWorld Direct",
            "product_name": "Sony WH-1000XM5 Wireless Noise-Canceling Headphones - Black",
            "brand": "Sony",
            "model": "WH-1000XM5",
            "variant": "Wireless",
            "storage": None,
            "ram": None,
            "color": "Black",
            "condition": "New",
            "price": 26990.0,
            "currency": "INR",
            "delivery_fee": 0.0,
            "seller_name": "Sony Authorized Dealer",
            "seller_rating": 4.9,
            "seller_review_count": 4100,
            "warranty": "1 Year Official Brand Warranty",
            "warranty_months": 12,
            "return_policy": "10-day return",
            "delivery_days": 1,
            "availability": "In Stock",
            "important_specifications": {
                "ANC": "Industry Leading Auto NC Optimizer",
                "Battery Life": "Up to 30 hours",
                "Microphones": "8 microphones for crisp calls"
            },
            "product_url": "https://example-audio.com/sony-xm5",
            "image_url": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=600&auto=format&fit=crop",
            "source_type": "demo"
        },
        {
            "id": "sony_b",
            "platform": "ElectroHub",
            "product_name": "Sony WH1000XM5 Noise Cancelling Headphones Black",
            "brand": "Sony",
            "model": "WH-1000XM5",
            "variant": "Wireless",
            "storage": None,
            "ram": None,
            "color": "Black",
            "condition": "New",
            "price": 24990.0,
            "currency": "INR",
            "delivery_fee": 199.0,
            "seller_name": "SoundWave India",
            "seller_rating": 4.7,
            "seller_review_count": 1420,
            "warranty": "1 Year Warranty",
            "warranty_months": 12,
            "return_policy": "7-day replacement",
            "delivery_days": 2,
            "availability": "In Stock",
            "important_specifications": {
                "ANC": "Industry Leading Auto NC Optimizer",
                "Battery Life": "Up to 30 hours",
                "Microphones": "8 microphones for crisp calls"
            },
            "product_url": "https://example-electro.com/sony-xm5-headphone",
            "image_url": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=600&auto=format&fit=crop",
            "source_type": "demo"
        },
        {
            "id": "sony_c",
            "platform": "QuickAudio Mart",
            "product_name": "Sony WH-1000XM5 Over-Ear Headphones (Black)",
            "brand": "Sony",
            "model": "WH-1000XM5",
            "variant": "Wireless",
            "storage": None,
            "ram": None,
            "color": "Black",
            "condition": "New",
            "price": 27490.0,
            "currency": "INR",
            "delivery_fee": 0.0,
            "seller_name": "Sonic Retail",
            "seller_rating": 4.3,
            "seller_review_count": 310,
            "warranty": "1 Year Warranty",
            "warranty_months": 12,
            "return_policy": "7-day return",
            "delivery_days": 3,
            "availability": "In Stock",
            "important_specifications": {
                "ANC": "Industry Leading Auto NC Optimizer",
                "Battery Life": "Up to 30 hours",
                "Microphones": "8 microphones for crisp calls"
            },
            "product_url": "https://example-sonic.com/sony-xm5-black",
            "image_url": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=600&auto=format&fit=crop",
            "source_type": "demo"
        }
    ],

    "macbook air m3": [
        {
            "id": "mac_a",
            "platform": "Apple Premium Reseller",
            "product_name": "Apple MacBook Air 13-inch M3 Chip 8GB RAM 256GB SSD - Midnight",
            "brand": "Apple",
            "model": "MacBook Air M3",
            "variant": "13-inch",
            "storage": "256GB",
            "ram": "8GB",
            "color": "Midnight",
            "condition": "New",
            "price": 114900.0,
            "currency": "INR",
            "delivery_fee": 0.0,
            "seller_name": "Imagine Apple Reseller",
            "seller_rating": 4.9,
            "seller_review_count": 3800,
            "warranty": "1 Year AppleCare Warranty",
            "warranty_months": 12,
            "return_policy": "14-day return",
            "delivery_days": 1,
            "availability": "In Stock",
            "important_specifications": {
                "Display": "13.6-inch Liquid Retina",
                "Chip": "Apple M3 8-core CPU / 8-core GPU",
                "Weight": "1.24 kg"
            },
            "product_url": "https://example-imagine.com/macbook-air-m3",
            "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=600&auto=format&fit=crop",
            "source_type": "demo"
        },
        {
            "id": "mac_b",
            "platform": "CyberTech Store",
            "product_name": "Apple MacBook Air M3 13.6\" 8GB / 256GB Midnight",
            "brand": "Apple",
            "model": "MacBook Air M3",
            "variant": "13-inch",
            "storage": "256GB",
            "ram": "8GB",
            "color": "Midnight",
            "condition": "New",
            "price": 109900.0,
            "currency": "INR",
            "delivery_fee": 499.0,
            "seller_name": "CyberTech Verified Partner",
            "seller_rating": 4.7,
            "seller_review_count": 2100,
            "warranty": "1 Year Apple Warranty",
            "warranty_months": 12,
            "return_policy": "7-day replacement",
            "delivery_days": 2,
            "availability": "In Stock",
            "important_specifications": {
                "Display": "13.6-inch Liquid Retina",
                "Chip": "Apple M3 8-core CPU / 8-core GPU",
                "Weight": "1.24 kg"
            },
            "product_url": "https://example-cybertech.com/macbook-air-m3-midnight",
            "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=600&auto=format&fit=crop",
            "source_type": "demo"
        },
        {
            "id": "mac_c",
            "platform": "MegaComputers",
            "product_name": "Apple MacBook Air 13.6 M3 (8GB, 256GB SSD, Midnight)",
            "brand": "Apple",
            "model": "MacBook Air M3",
            "variant": "13-inch",
            "storage": "256GB",
            "ram": "8GB",
            "color": "Midnight",
            "condition": "New",
            "price": 112900.0,
            "currency": "INR",
            "delivery_fee": 0.0,
            "seller_name": "MegaComputers Hub",
            "seller_rating": 4.4,
            "seller_review_count": 750,
            "warranty": "1 Year Warranty",
            "warranty_months": 12,
            "return_policy": "7-day return",
            "delivery_days": 3,
            "availability": "In Stock",
            "important_specifications": {
                "Display": "13.6-inch Liquid Retina",
                "Chip": "Apple M3 8-core CPU / 8-core GPU",
                "Weight": "1.24 kg"
            },
            "product_url": "https://example-megacomputers.com/macbook-m3-256gb",
            "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=600&auto=format&fit=crop",
            "source_type": "demo"
        }
    ]
}

DEMO_QUERIES = [
    "iPhone 15 128GB",
    "Samsung Galaxy S24",
    "Sony WH-1000XM5",
    "MacBook Air M3"
]

def get_demo_listings_for_query(query: str, cross_marketplace: bool = True) -> List[Dict[str, Any]]:
    clean_query = query.lower().strip()
    
    # Try exact match or partial match
    matched_key = None
    for key in DEMO_DATASETS.keys():
        if key in clean_query or clean_query in key:
            matched_key = key
            break
            
    if not matched_key:
        # Default fallback to iPhone 15 128GB
        matched_key = "iphone 15 128gb"
        
    listings = DEMO_DATASETS[matched_key].copy()
    
    if not cross_marketplace:
        # Filter out refurbished/used outlet listings when cross_marketplace is False
        listings = [l for l in listings if "Refurbished" not in l["platform"] and "Used" not in l.get("condition", "")]
        
    return listings
