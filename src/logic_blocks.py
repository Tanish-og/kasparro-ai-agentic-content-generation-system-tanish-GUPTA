from .models import Product, CategorizedQuestions, FAQItem, ProductPage, ComparisonPage
import random
from typing import List, Dict, Any


def generate_benefits_description(product: Product) -> str:
    """Generate compelling benefits description from product data."""
    benefits = product.benefits
    return f"Experience the transformative power of {product.name} with {benefits.lower()}. This carefully formulated serum delivers professional-grade results in the comfort of your home."


def extract_usage_instructions(product: Product) -> str:
    """Extract and format usage instructions."""
    return product.how_to_use


def create_safety_summary(product: Product) -> str:
    """Create safety summary from side effects."""
    return f"This product is generally well-tolerated. {product.side_effects}"


def select_faq_questions(questions: CategorizedQuestions, count: int = 5) -> List[str]:
    """Intelligently select FAQ questions from categorized questions."""
    selected = []
    categories = ['usage', 'safety', 'informational', 'purchase', 'comparison']

    for category in categories:
        cat_questions = getattr(questions, category)
        if cat_questions:
            # Take up to 2 from each category
            selected.extend(cat_questions[:2])

    # Shuffle and take the required count
    random.shuffle(selected)
    return selected[:count]


def generate_fictional_product_b() -> Dict[str, Any]:
    """Generate a fictional but realistic product B for comparison."""
    return {
        "name": "Dermaclear Retinol Serum",
        "concentration": "2% Retinol",
        "skin_type": "Oily, Combination, Mature",
        "key_ingredients": "Retinol, Hyaluronic Acid, Vitamin E",
        "benefits": "Anti-aging, Reduces fine lines, Improves skin texture",
        "how_to_use": "Apply 1-2 drops in the evening after cleansing",
        "side_effects": "Possible dryness and peeling during initial use",
        "price": "₹899"
    }


def generate_comparison_points(product_a: Product, product_b: Dict[str, Any]) -> List[str]:
    """Generate comparison points between two products."""
    points = [
        f"Both {product_a.name} and {product_b['name']} contain Hyaluronic Acid for hydration",
        f"{product_a.name} focuses on {product_a.benefits.lower()} while {product_b['name']} targets {product_b['benefits'].lower()}",
        f"{product_a.name} is priced at {product_a.price} compared to {product_b['name']} at {product_b['price']}",
        f"{product_a.name} is suitable for {product_a.skin_type.lower()} skin, while {product_b['name']} works for {product_b['skin_type'].lower()} skin"
    ]
    return points


def build_product_description(product: Product) -> str:
    """Build comprehensive product description."""
    return f"{product.name} is a {product.concentration} serum designed for {product.skin_type.lower()} skin. Formulated with {product.key_ingredients.lower()}, it provides {product.benefits.lower()}. {extract_usage_instructions(product)}."


def create_faq_answers(questions: List[str], product: Product) -> List[FAQItem]:
    """Create FAQ items with answers based on product data."""
    faqs = []
    for question in questions:
        # Simple rule-based answering (in real implementation, this would use LLM)
        answer = "Based on the product information, this serum is designed to provide optimal results when used as directed."

        if "vitamin c" in question.lower():
            answer = f"{product.name} contains {product.concentration} of Vitamin C, known for its {product.benefits.lower()}."
        elif "skin type" in question.lower():
            answer = f"This serum is formulated for {product.skin_type.lower()} skin types."
        elif "use" in question.lower() or "apply" in question.lower():
            answer = product.how_to_use
        elif "side effect" in question.lower() or "safe" in question.lower():
            answer = create_safety_summary(product)
        elif "price" in question.lower():
            answer = f"The product is priced at {product.price}."

        faqs.append(FAQItem(question=question, answer=answer))
    return faqs
