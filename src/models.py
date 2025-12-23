from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class Product(BaseModel):
    name: str
    concentration: str
    skin_type: str
    key_ingredients: str
    benefits: str
    how_to_use: str
    side_effects: str
    price: str


class QuestionCategory(BaseModel):
    category: str
    questions: List[str]


class CategorizedQuestions(BaseModel):
    informational: List[str]
    safety: List[str]
    usage: List[str]
    purchase: List[str]
    comparison: List[str]


class FAQItem(BaseModel):
    question: str
    answer: str


class FAQPage(BaseModel):
    product_name: str
    faqs: List[FAQItem]


class ProductPage(BaseModel):
    product_name: str
    concentration: str
    skin_type: str
    key_ingredients: str
    benefits: str
    how_to_use: str
    side_effects: str
    price: str
    description: str


class ComparisonPage(BaseModel):
    product_a: Dict[str, Any]
    product_b: Dict[str, Any]
    comparison_points: List[str]
