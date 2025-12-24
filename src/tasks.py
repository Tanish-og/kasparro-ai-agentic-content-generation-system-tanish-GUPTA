from crewai import Task
from textwrap import dedent
import json
from .models import Product, FAQPage, ProductPage, ComparisonPage, CategorizedQuestions

def create_tasks(agents, product_data):
    """Create CrewAI tasks with structured outputs and validation."""
    
    data_parser, question_generator, faq_generator, product_generator, comparison_generator = agents

    # Task 1: Parse and Validate Product Data
    parse_data_task = Task(
        description=dedent(f"""
            Parse and validate the following product data. Ensure all required fields are present and properly formatted.

            Product Data: {json.dumps(product_data, indent=2)}

            Required fields: name, concentration, skin_type, key_ingredients, benefits, how_to_use, side_effects, price
        """),
        agent=data_parser,
        expected_output="Clean JSON object with validated product data",
        output_pydantic=Product # Strict Pydantic Output
    )

    # Task 2: Generate Categorized Questions
    generate_questions_task = Task(
        description=dedent(f"""
            Generate EXACTLY 5 questions for EACH of the following categories (Total 25 questions):

            Categories:
            - informational: General product information questions
            - safety: Safety concerns, side effects, precautions
            - usage: How to use, application, routine questions
            - purchase: Pricing, availability, buying questions
            - comparison: Product comparison and alternative questions

            Product: {product_data.get('name', 'Product')}
            
            Ensure you generate enough questions to meet the strict requirement of 5 per category.
        """),
        agent=question_generator,
        expected_output="JSON object with exactly 25 categorized questions",
        context=[parse_data_task],
        output_pydantic=CategorizedQuestions # Strict Pydantic Output with validator
    )

    # Task 3: Generate FAQ Page
    generate_faq_task = Task(
        description=dedent("""
            Using the validated product data and generated questions, create a comprehensive FAQ section.

            Select the 5 most relevant questions (one from each category) and provide detailed, accurate answers based ONLY on the verified product data.

            Each answer must:
            - Be specific to this product's actual features
            - Reference real product specifications
            - Be helpful and informative
            - Be based on verified data only
        """),
        agent=faq_generator,
        expected_output="JSON object with product name and 5 FAQ items",
        context=[parse_data_task, generate_questions_task],
        output_pydantic=FAQPage # Strict Pydantic Output with validator
    )

    # Task 4: Generate Product Page
    generate_product_task = Task(
        description=dedent("""
            Create a comprehensive product description page using the validated product data.

            Include all product specifications and create a compelling description paragraph.
        """),
        agent=product_generator,
        expected_output="Complete product page JSON with all fields",
        context=[parse_data_task],
        output_pydantic=ProductPage # Strict Pydantic Output
    )

    # Task 5: Generate Comparison Page
    generate_comparison_task = Task(
        description=dedent("""
            Create a structured comparison between the original product and a realistic competitor.
            
            Use the 'Competitor Lookup Tool' to fetch real details about a competitor product. DO NOT invent one.

            Original Product:
            Name: {original_name}
            Price: {original_price}
            
            Compare them point by point.
        """).format(
            original_name=product_data.get('name'),
            original_price=product_data.get('price')
        ),
        agent=comparison_generator,
        expected_output="Structured comparison JSON with both products and comparison points",
        context=[parse_data_task],
        output_pydantic=ComparisonPage # Strict Pydantic Output
    )

    return [parse_data_task, generate_questions_task, generate_faq_task, generate_product_task, generate_comparison_task]
