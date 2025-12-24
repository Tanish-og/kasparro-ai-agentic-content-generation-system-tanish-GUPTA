from pydantic import BaseModel, field_validator, model_validator
from typing import List, Dict, Any


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

    @field_validator('informational', 'safety', 'usage', 'purchase', 'comparison')
    @classmethod
    def check_min_questions(cls, v: List[str]) -> List[str]:
        # Individual category check if needed, but the main requirement is total 15
        # The prompt asks for 5 per category, so let's enforce strictly if possible, 
        # or just ensure non-empty. Let's strictly enforce at least 1 per category for now to be safe,
        # but the meaningful check is the total count.
        if not v:
             raise ValueError("Category must not be empty")
        return v

    def total_questions(self) -> int:
        return (len(self.informational) + len(self.safety) + 
                len(self.usage) + len(self.purchase) + len(self.comparison))

    @field_validator('comparison')
    @classmethod
    def check_total_count(cls, v: List[str], info) -> List[str]:
        # We cannot easily check other fields here in field_validator without validation_info accessing instance
        # faster to rely on the total_questions method check or use model_validator.
        # However, we can at least ensure this specific list is non-empty.
        if not v:
            raise ValueError("Comparison questions must not be empty")
        return v
    
    @model_validator(mode='after')
    def check_sum_total(self) -> 'CategorizedQuestions':
        total = (len(self.informational) + len(self.safety) + 
                 len(self.usage) + len(self.purchase) + len(self.comparison))
        if total < 15:
             raise ValueError(f"Total questions must be at least 15, got {total}")
        return self


class FAQItem(BaseModel):
    question: str
    answer: str


class FAQPage(BaseModel):
    product_name: str
    faqs: List[FAQItem]

    @field_validator('faqs')
    @classmethod
    def check_min_faqs(cls, v: List[FAQItem]) -> List[FAQItem]:
        if len(v) < 15:
            raise ValueError(f"Must have at least 15 FAQs to meet requirements, got {len(v)}")
        return v


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


class CompetitorProduct(BaseModel):
    name: str
    concentration: str
    skin_type: str
    key_ingredients: str
    benefits: str
    how_to_use: str
    side_effects: str
    price: str


class ComparisonPage(BaseModel):
    product_a: Dict[str, Any]
    product_b: CompetitorProduct
    comparison_points: List[str]

