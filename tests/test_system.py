import pytest
from src.models import CategorizedQuestions, FAQPage, FAQItem

def test_categorized_questions_validation():
    # Valid case
    valid_data = {
        "informational": ["q1", "q2", "q3"],
        "safety": ["q1", "q2", "q3"],
        "usage": ["q1", "q2", "q3"],
        "purchase": ["q1", "q2", "q3"],
        "comparison": ["q1", "q2", "q3"]
    }
    # 5 * 3 = 15 questions
    model = CategorizedQuestions(**valid_data)
    assert model.total_questions() == 15

    # Invalid empty list
    invalid_data = {
        "informational": [],
        "safety": ["q1"],
        "usage": ["q1"],
        "purchase": ["q1"],
        "comparison": ["q1"]
    }
    with pytest.raises(ValueError):
        CategorizedQuestions(**invalid_data)

def test_faq_page_validation():
    # Valid case
    valid_faqs = [FAQItem(question=f"q{i}", answer=f"a{i}") for i in range(5)]
    model = FAQPage(product_name="Test", faqs=valid_faqs)
    assert len(model.faqs) == 5

    # Invalid case (< 5)
    invalid_faqs = [FAQItem(question=f"q{i}", answer=f"a{i}") for i in range(4)]
    with pytest.raises(ValueError):
        FAQPage(product_name="Test", faqs=invalid_faqs)
