from langchain.tools import BaseTool
from typing import Dict, Any, Optional
import json

class CompetitorLookupTool(BaseTool):
    name: str = "Competitor Lookup Tool"
    description: str = "Retrieves information about a real competitor product for comparison. Input should be the product category (e.g., 'Vitamin C Serum')."

    def _run(self, query: str = "Vitamin C Serum") -> str:
        """
        Mock database lookup for competitor products.
        In a production environment, this would query a real PIM or market intelligence API.
        """
        # Mock Database
        competitors_db = {
            "vitamin c serum": {
                "name": "LuminaGlow C+ Serum",
                "concentration": "15% Vitamin C",
                "skin_type": "All Skin Types",
                "key_ingredients": "Vitamin C, Ferulic Acid, Vitamin E",
                "benefits": "Anti-aging, Radiance, Protection",
                "how_to_use": "Apply 4-5 drops daily after cleansing",
                "side_effects": "Rare sensitivity",
                "price": "₹799"
            },
            "retinol": {
                "name": "RetinAze Night Cream",
                "concentration": "0.5% Retinol",
                "skin_type": "Mature, Acne-prone",
                "key_ingredients": "Retinol, Niacinamide",
                "benefits": "Anti-wrinkle, texture smoothing",
                "how_to_use": "Apply at night only",
                "side_effects": "Dryness, purging",
                "price": "₹899"
            }
        }
        
        # Normalize query
        key = query.lower().strip()
        
        # Search logic
        result = competitors_db.get(key)
        
        # Fallback for fuzzy matching
        if not result:
            for k, v in competitors_db.items():
                if k in key or key in k:
                    result = v
                    break
        
        if result:
            return json.dumps(result)
        else:
            return "No specific competitor found for this category. Suggest using a generic localized competitor."

