import re
import json
import httpx
from typing import Dict, Any
from app.config import settings
from app.services.normalization.normalizer import NormalizationEngine


class ExtractionEngine:

    def __init__(self):
        self.normalizer = NormalizationEngine()

    def deterministic_extract(
        self,
        raw_title: str,
        raw_description: str = "",
        raw_price: float = None,
        raw_seller: str = "",
        raw_specifications: str = ""
    ) -> Dict[str, Any]:

        text = f"{raw_title} {raw_description} {raw_specifications}".strip()
        uncertain = []

        # -------------------------
        # BRAND
        # -------------------------
        brand = None

        if re.search(r"\b(apple|iphone|macbook)\b", text, re.I):
            brand = "Apple"

        elif re.search(r"\b(samsung|galaxy)\b", text, re.I):
            brand = "Samsung"

        elif re.search(r"\b(sony)\b", text, re.I):
            brand = "Sony"

        else:
            uncertain.append("brand")

        # -------------------------
        # MODEL
        # -------------------------
        model = None

        model_patterns = [
            r"(iPhone\s+\d+(?:\s+Pro(?:\s+Max)?)?)",
            r"(Galaxy\s+S\d+(?:\s+Ultra)?)",
            r"(WH-\d+XM\d+)",
            r"(MacBook\s+Air(?:\s+\d+(?:-inch)?)?)"
        ]

        for pattern in model_patterns:
            match = re.search(pattern, text, re.I)

            if match:
                model = match.group(1)
                break

        if not model:
            model = raw_title

        # -------------------------
        # STORAGE
        # -------------------------
        storage = None

        storage_match = re.search(
            r"(\d+\s*(?:GB|TB))\s*(?:storage|SSD)?",
            text,
            re.I
        )

        if storage_match:
            storage = self.normalizer.normalize_storage(
                storage_match.group(1)
            )
        else:
            uncertain.append("storage")

        # -------------------------
        # RAM
        # -------------------------
        ram = None

        ram_match = re.search(
            r"(\d+\s*GB)\s*(?:RAM|Memory)",
            text,
            re.I
        )

        if ram_match:
            ram = self.normalizer.normalize_ram(
                ram_match.group(1)
            )

        # -------------------------
        # COLOR
        # -------------------------
        color = None

        color_match = re.search(
            r"\b(black|white|blue|green|midnight|starlight|silver|gold|purple|red)\b",
            text,
            re.I
        )

        if color_match:
            color = color_match.group(1).title()

        # -------------------------
        # CONDITION
        # -------------------------
        condition = self.normalizer.normalize_condition(text)

        # -------------------------
        # SELLER RATING
        # -------------------------
        seller_rating = 4.5

        rating_match = re.search(
            r"(\d+(?:\.\d+)?)\s*(?:stars?|★)",
            raw_seller,
            re.I
        )

        if rating_match:
            seller_rating = float(rating_match.group(1))

        # -------------------------
        # WARRANTY
        # -------------------------
        warranty_months = 0

        year_match = re.search(
            r"(\d+)\s*(?:year|years)",
            text,
            re.I
        )

        if year_match:
            warranty_months = int(year_match.group(1)) * 12

        else:
            month_match = re.search(
                r"(\d+)\s*(?:month|months)",
                text,
                re.I
            )

            if month_match:
                warranty_months = int(month_match.group(1))

        # -------------------------
        # DELIVERY
        # -------------------------
        delivery_fee = 0.0

        delivery_match = re.search(
            r"(?:delivery|shipping).*?(?:₹|rs\.?|inr)?\s*(\d+(?:\.\d+)?)",
            text,
            re.I
        )

        if delivery_match:
            delivery_fee = float(delivery_match.group(1))

        # -------------------------
        # FINAL RESULT
        # -------------------------
        return {
            "brand": brand,
            "model": model,
            "storage": storage,
            "ram": ram,
            "color": color,
            "condition": condition,
            "price": raw_price,
            "delivery_fee": delivery_fee,
            "seller_rating": seller_rating,
            "warranty_months": warranty_months,
            "uncertain_fields": uncertain
        }

    async def extract_structured(
        self,
        raw_title: str,
        raw_description: str = "",
        raw_price: float = None,
        raw_seller: str = "",
        raw_specifications: str = ""
    ) -> Dict[str, Any]:

        # Use deterministic extraction if LLM is not configured
        if not settings.LLM_API_KEY:

            return self.deterministic_extract(
                raw_title,
                raw_description,
                raw_price,
                raw_seller,
                raw_specifications
            )

        prompt = f"""
Extract structured e-commerce product details.

Title:
{raw_title}

Description:
{raw_description}

Seller:
{raw_seller}

Specifications:
{raw_specifications}

Return strictly JSON:

{{
    "brand": null,
    "model": null,
    "storage": null,
    "ram": null,
    "color": null,
    "condition": "New",
    "warranty_months": 0
}}
"""

        for attempt in range(2):

            try:

                async with httpx.AsyncClient(timeout=8.0) as client:

                    response = await client.post(
                        f"{settings.LLM_BASE_URL}/chat/completions",

                        headers={
                            "Authorization": f"Bearer {settings.LLM_API_KEY}",
                            "Content-Type": "application/json"
                        },

                        json={
                            "model": settings.LLM_MODEL,
                            "messages": [
                                {
                                    "role": "user",
                                    "content": prompt
                                }
                            ],
                            "temperature": 0.1,
                            "response_format": {
                                "type": "json_object"
                            }
                        }
                    )

                    if response.status_code == 200:

                        content = response.json()[
                            "choices"
                        ][0]["message"]["content"]

                        parsed = json.loads(content)

                        parsed["price"] = raw_price
                        parsed["delivery_fee"] = 0.0
                        parsed["seller_rating"] = 4.5
                        parsed["uncertain_fields"] = []

                        return parsed

            except Exception:
                pass

        # AI failed → deterministic fallback
        return self.deterministic_extract(
            raw_title,
            raw_description,
            raw_price,
            raw_seller,
            raw_specifications
        )
