import os
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from openai import OpenAI
from .models import Product, CategorizedQuestions, FAQPage, ProductPage, ComparisonPage
from .templates import TemplateEngine


class BaseAgent(ABC):
    """Base agent class with common functionality."""

    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key) if api_key else None

    @abstractmethod
    def execute(self, input_data: Any) -> Any:
        """Execute the agent's primary function."""
        pass

    def _call_llm(self, prompt: str, max_tokens: int = 500) -> str:
        """Call OpenAI LLM with the given prompt."""
        if not self.client:
            print("No OpenAI API key provided, using fallback")
            return self._fallback_response(prompt)

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"LLM call failed: {e}")
            return self._fallback_response(prompt)

    def _fallback_response(self, prompt: str) -> str:
        """Provide fallback response when LLM is not available."""
        if "question" in prompt.lower():
            return '{"informational": ["What is this product?", "What are the main ingredients?", "What skin types is it for?"], "safety": ["Are there any side effects?", "Is it safe for sensitive skin?", "Can I use it during pregnancy?"], "usage": ["How often should I use it?", "When should I apply it?", "How much should I use?"], "purchase": ["How much does it cost?", "Where can I buy it?", "Is it available online?"], "comparison": ["How does it compare to other vitamin C serums?", "What\'s better than this product?", "Is there a cheaper alternative?"]}'
        return "Fallback content generation"


class DataParserAgent(BaseAgent):
    """Agent responsible for parsing and validating product data."""

    def __init__(self):
        super().__init__("DataParser", "Parse and validate product data into structured format")

    def execute(self, raw_data: Dict[str, str]) -> Product:
        """Parse raw product data into Product model."""
        return Product(**raw_data)


class QuestionGeneratorAgent(BaseAgent):
    """Agent responsible for generating categorized user questions."""

    def __init__(self):
        super().__init__("QuestionGenerator", "Generate categorized questions based on product data")

    def execute(self, product: Product) -> CategorizedQuestions:
        """Generate at least 15 categorized questions."""

        prompt = f"""
        Based on this skincare product, generate at least 15 user questions categorized as follows:
        - Informational (general info about the product)
        - Safety (side effects, precautions, safety concerns)
        - Usage (how to use, application, routine)
        - Purchase (pricing, availability, buying)
        - Comparison (vs other products, alternatives)

        Product: {product.name}
        Concentration: {product.concentration}
        Skin Type: {product.skin_type}
        Key Ingredients: {product.key_ingredients}
        Benefits: {product.benefits}
        How to Use: {product.how_to_use}
        Side Effects: {product.side_effects}
        Price: {product.price}

        Return the questions in JSON format with keys: informational, safety, usage, purchase, comparison.
        Each key should have an array of at least 3 questions.
        """

        response = self._call_llm(prompt, max_tokens=1000)

        # Parse the JSON response
        import json
        try:
            questions_data = json.loads(response)
            return CategorizedQuestions(**questions_data)
        except:
            # Fallback with some default questions
            return CategorizedQuestions(
                informational=["What is this product?", "What are the main ingredients?", "What skin types is it for?"],
                safety=["Are there any side effects?", "Is it safe for sensitive skin?", "Can I use it during pregnancy?"],
                usage=["How often should I use it?", "When should I apply it?", "How much should I use?"],
                purchase=["How much does it cost?", "Where can I buy it?", "Is it available online?"],
                comparison=["How does it compare to other vitamin C serums?", "What's better than this product?", "Is there a cheaper alternative?"]
            )


class ContentAssemblerAgent(BaseAgent):
    """Agent responsible for assembling content pages using templates."""

    def __init__(self):
        super().__init__("ContentAssembler", "Assemble content pages using templates and logic blocks")

    def execute(self, data: Dict[str, Any]) -> Any:
        """Assemble content based on page type."""
        page_type = data.get("page_type")
        product = data.get("product")
        questions = data.get("questions")

        if page_type == "faq":
            return TemplateEngine.apply_faq_template(product, questions)
        elif page_type == "product":
            return TemplateEngine.apply_product_template(product)
        elif page_type == "comparison":
            return TemplateEngine.apply_comparison_template(product)
        else:
            raise ValueError(f"Unknown page type: {page_type}")


class OrchestratorAgent(BaseAgent):
    """Main orchestrator that coordinates the entire pipeline."""

    def __init__(self):
        super().__init__("Orchestrator", "Coordinate the multi-agent content generation pipeline")
        self.data_parser = DataParserAgent()
        self.question_generator = QuestionGeneratorAgent()
        self.content_assembler = ContentAssemblerAgent()

    def execute(self, raw_product_data: Dict[str, str]) -> Dict[str, Any]:
        """Execute the complete content generation pipeline."""

        # Step 1: Parse data
        product = self.data_parser.execute(raw_product_data)

        # Step 2: Generate questions
        questions = self.question_generator.execute(product)

        # Step 3: Generate FAQ page
        faq_data = {"page_type": "faq", "product": product, "questions": questions}
        faq_page = self.content_assembler.execute(faq_data)

        # Step 4: Generate Product page
        product_data = {"page_type": "product", "product": product}
        product_page = self.content_assembler.execute(product_data)

        # Step 5: Generate Comparison page
        comparison_data = {"page_type": "comparison", "product": product}
        comparison_page = self.content_assembler.execute(comparison_data)

        return {
            "faq": faq_page,
            "product": product_page,
            "comparison": comparison_page
        }
