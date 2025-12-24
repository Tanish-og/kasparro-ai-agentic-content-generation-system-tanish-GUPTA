"""
Unit tests for logic_blocks.py

Tests validation and utility functions used in the content generation system.
"""

import pytest
from src.logic_blocks import validate_product_data, format_product_summary
from src.models import Product


class TestProductDataValidation:
    """Test cases for product data validation."""

    def test_valid_product_data(self):
        """Test validation of complete product data."""
        valid_data = {
            "name": "Test Serum",
            "concentration": "10% Vitamin C",
            "skin_type": "Oily",
            "key_ingredients": "Vitamin C, Hyaluronic Acid",
            "benefits": "Brightening",
            "how_to_use": "Apply morning",
            "side_effects": "Mild tingling",
            "price": "₹500"
        }
        assert validate_product_data(valid_data) == True

    def test_invalid_product_data_missing_fields(self):
        """Test validation fails with missing required fields."""
        invalid_data = {
            "name": "Test Serum",
            "skin_type": "Oily"
            # Missing other required fields
        }
        assert validate_product_data(invalid_data) == False

    def test_invalid_product_data_empty_dict(self):
        """Test validation fails with empty dictionary."""
        assert validate_product_data({}) == False

    def test_invalid_product_data_none(self):
        """Test validation fails with None input."""
        assert validate_product_data(None) == False


class TestProductSummaryFormatting:
    """Test cases for product summary formatting."""

    def test_format_product_summary(self):
        """Test formatting of product summary string."""
        product = Product(
            name="GlowBoost Vitamin C Serum",
            concentration="10% Vitamin C",
            skin_type="Oily, Combination",
            key_ingredients="Vitamin C, Hyaluronic Acid",
            benefits="Brightening, Fades dark spots",
            how_to_use="Apply 2–3 drops in the morning before sunscreen",
            side_effects="Mild tingling for sensitive skin",
            price="₹699"
        )

        summary = format_product_summary(product)
        expected = "GlowBoost Vitamin C Serum - 10% Vitamin C serum for Oily, Combination skin"

        assert summary == expected

    def test_format_product_summary_minimal(self):
        """Test formatting with minimal product data."""
        product = Product(
            name="Test Product",
            concentration="5% Active",
            skin_type="All",
            key_ingredients="Water",
            benefits="Hydration",
            how_to_use="Apply daily",
            side_effects="None",
            price="₹100"
        )

        summary = format_product_summary(product)
        expected = "Test Product - 5% Active serum for All skin"

        assert summary == expected


class TestDataStructures:
    """Test data structure integrity."""

    def test_product_model_creation(self):
        """Test that Product model can be created with valid data."""
        data = {
            "name": "Test Serum",
            "concentration": "10% Vitamin C",
            "skin_type": "Oily",
            "key_ingredients": "Vitamin C, Hyaluronic Acid",
            "benefits": "Brightening",
            "how_to_use": "Apply morning",
            "side_effects": "Mild tingling",
            "price": "₹500"
        }

        product = Product(**data)

        assert product.name == "Test Serum"
        assert product.concentration == "10% Vitamin C"
        assert product.skin_type == "Oily"
        assert product.price == "₹500"

    def test_product_model_validation(self):
        """Test that Product model validates required fields."""
        # This should work with complete data
        data = {
            "name": "Test Serum",
            "concentration": "10% Vitamin C",
            "skin_type": "Oily",
            "key_ingredients": "Vitamin C",
            "benefits": "Brightening",
            "how_to_use": "Apply morning",
            "side_effects": "None",
            "price": "₹500"
        }

        product = Product(**data)
        assert product is not None

        # Missing required field should raise validation error
        incomplete_data = {
            "name": "Test Serum",
            "skin_type": "Oily"
        }

        with pytest.raises(Exception):  # Pydantic validation error
            Product(**incomplete_data)


if __name__ == "__main__":
    # Run basic tests without pytest if needed
    print("Running basic validation tests...")

    # Test validation function
    valid_data = {
        "name": "Test Serum",
        "concentration": "10% Vitamin C",
        "skin_type": "Oily",
        "key_ingredients": "Vitamin C, Hyaluronic Acid",
        "benefits": "Brightening",
        "how_to_use": "Apply morning",
        "side_effects": "Mild tingling",
        "price": "₹500"
    }

    assert validate_product_data(valid_data), "Valid data should pass validation"
    assert not validate_product_data({}), "Empty data should fail validation"

    # Test product creation
    product = Product(**valid_data)
    summary = format_product_summary(product)
    assert "Test Serum" in summary, "Summary should contain product name"

    print("✅ All basic tests passed!")
