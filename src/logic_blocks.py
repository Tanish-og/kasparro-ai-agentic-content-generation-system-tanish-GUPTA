"""
Logic blocks for content transformation.

Note: Most content generation logic has been moved to CrewAI agents
to ensure real AI-powered generation without hardcoded fallbacks.
This file now contains only minimal utility functions.
"""

from .models import Product
from typing import Dict, Any


def validate_product_data(data: Dict[str, Any]) -> bool:
    """Validate that product data contains all required fields."""
    required_fields = [
        'name', 'concentration', 'skin_type', 'key_ingredients',
        'benefits', 'how_to_use', 'side_effects', 'price'
    ]
    return all(field in data for field in required_fields)


def format_product_summary(product: Product) -> str:
    """Create a basic product summary string."""
    return f"{product.name} - {product.concentration} serum for {product.skin_type} skin"
