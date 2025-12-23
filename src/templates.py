from typing import Dict, Any, List
from .models import Product, CategorizedQuestions, FAQPage, ProductPage, ComparisonPage
from .logic_blocks import (
    select_faq_questions,
    create_faq_answers,
    build_product_description,
    generate_fictional_product_b,
    generate_comparison_points
)


class TemplateEngine:
    """Custom template engine for content generation."""

    @staticmethod
    def get_faq_template() -> Dict[str, Any]:
        """Template for FAQ page generation."""
        return {
            "fields": ["product_name", "faqs"],
            "rules": ["select_questions", "generate_answers"],
            "formatting": "structured_qa",
            "dependencies": ["question_selector", "answer_generator"]
        }

    @staticmethod
    def get_product_template() -> Dict[str, Any]:
        """Template for product description page."""
        return {
            "fields": ["product_name", "concentration", "skin_type", "key_ingredients",
                      "benefits", "how_to_use", "side_effects", "price", "description"],
            "rules": ["build_description"],
            "formatting": "product_profile",
            "dependencies": ["description_builder"]
        }

    @staticmethod
    def get_comparison_template() -> Dict[str, Any]:
        """Template for comparison page."""
        return {
            "fields": ["product_a", "product_b", "comparison_points"],
            "rules": ["generate_fictional_b", "create_comparison"],
            "formatting": "side_by_side",
            "dependencies": ["product_generator", "comparison_analyzer"]
        }

    @staticmethod
    def apply_faq_template(product: Product, questions: CategorizedQuestions) -> FAQPage:
        """Apply FAQ template to generate FAQ page."""
        selected_questions = select_faq_questions(questions, 5)
        faqs = create_faq_answers(selected_questions, product)

        return FAQPage(
            product_name=product.name,
            faqs=faqs
        )

    @staticmethod
    def apply_product_template(product: Product) -> ProductPage:
        """Apply product template to generate product page."""
        description = build_product_description(product)

        return ProductPage(
            product_name=product.name,
            concentration=product.concentration,
            skin_type=product.skin_type,
            key_ingredients=product.key_ingredients,
            benefits=product.benefits,
            how_to_use=product.how_to_use,
            side_effects=product.side_effects,
            price=product.price,
            description=description
        )

    @staticmethod
    def apply_comparison_template(product: Product) -> ComparisonPage:
        """Apply comparison template to generate comparison page."""
        product_b = generate_fictional_product_b()
        comparison_points = generate_comparison_points(product, product_b)

        return ComparisonPage(
            product_a=product.model_dump(),
            product_b=product_b,
            comparison_points=comparison_points
        )
