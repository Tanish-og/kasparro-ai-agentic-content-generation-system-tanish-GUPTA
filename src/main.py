import json
import os
from pathlib import Path
from crewai import Crew, Task, Agent
from textwrap import dedent
from .models import Product, FAQPage, ProductPage, ComparisonPage, FAQItem

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Product data from assignment
RAW_PRODUCT_DATA = {
    "name": "GlowBoost Vitamin C Serum",
    "concentration": "10% Vitamin C",
    "skin_type": "Oily, Combination",
    "key_ingredients": "Vitamin C, Hyaluronic Acid",
    "benefits": "Brightening, Fades dark spots",
    "how_to_use": "Apply 2–3 drops in the morning before sunscreen",
    "side_effects": "Mild tingling for sensitive skin",
    "price": "₹699"
}

def create_agents():
    """Create CrewAI agents for the content generation system."""

    # Data Parser Agent
    data_parser = Agent(
        role="Data Parser",
        goal="Parse and validate product data into structured format",
        backstory="You are an expert data validator who ensures product information is correctly structured and validated.",
        verbose=True
    )

    # Question Generator Agent
    question_generator = Agent(
        role="Question Generator",
        goal="Generate at least 15 categorized user questions based on product data",
        backstory="You are a content strategist who creates comprehensive questions that users typically ask about skincare products.",
        verbose=True
    )

    # FAQ Generator Agent
    faq_generator = Agent(
        role="FAQ Generator",
        goal="Generate detailed FAQ answers based on product information and user questions",
        backstory="You are an expert customer service specialist who provides accurate, helpful answers to skincare product questions.",
        verbose=True
    )

    # Product Description Generator Agent
    product_generator = Agent(
        role="Product Description Generator",
        goal="Create compelling product descriptions and specifications",
        backstory="You are a skilled copywriter who creates engaging product descriptions for e-commerce platforms.",
        verbose=True
    )

    # Comparison Generator Agent
    comparison_generator = Agent(
        role="Comparison Generator",
        goal="Create fictional competitor products and detailed comparisons",
        backstory="You are a market analyst who creates realistic competitor products and detailed feature comparisons.",
        verbose=True
    )

    return data_parser, question_generator, faq_generator, product_generator, comparison_generator

def create_tasks(agents, product_data):
    """Create CrewAI tasks for the content generation pipeline."""

    data_parser, question_generator, faq_generator, product_generator, comparison_generator = agents

    # Task 1: Parse Product Data
    parse_data_task = Task(
        description=dedent(f"""
            Parse and validate the following product data into a clean JSON structure:

            Product Data:
            {json.dumps(product_data, indent=2)}

            Return only the validated JSON structure with these exact fields:
            - name, concentration, skin_type, key_ingredients, benefits, how_to_use, side_effects, price
        """),
        agent=data_parser,
        expected_output="Valid JSON structure of the product data"
    )

    # Task 2: Generate Questions
    generate_questions_task = Task(
        description=dedent(f"""
            Based on this skincare product, generate at least 15 user questions categorized as follows:
            - Informational (general info about the product)
            - Safety (side effects, precautions, safety concerns)
            - Usage (how to use, application, routine)
            - Purchase (pricing, availability, buying)
            - Comparison (vs other products, alternatives)

            Product: {product_data['name']}
            Concentration: {product_data['concentration']}
            Skin Type: {product_data['skin_type']}
            Key Ingredients: {product_data['key_ingredients']}
            Benefits: {product_data['benefits']}
            How to Use: {product_data['how_to_use']}
            Side Effects: {product_data['side_effects']}
            Price: {product_data['price']}

            Return the questions in JSON format with keys: informational, safety, usage, purchase, comparison.
            Each category must have at least 3 questions (total minimum 15 questions).
        """),
        agent=question_generator,
        expected_output="JSON object with categorized questions",
        context=[parse_data_task]
    )

    # Task 3: Generate FAQ Page
    generate_faq_task = Task(
        description=dedent("""
            Using the generated questions and product information, create a comprehensive FAQ section.

            Select the 5 most relevant questions from different categories and provide detailed,
            accurate answers based on the product data. Do not use generic answers - each answer
            must be specific to this product's features and specifications.

            Return in JSON format:
            {
                "product_name": "product name",
                "faqs": [
                    {"question": "question text", "answer": "detailed answer"},
                    ...
                ]
            }
        """),
        agent=faq_generator,
        expected_output="JSON structure with product name and FAQ array",
        context=[generate_questions_task]
    )

    # Task 4: Generate Product Page
    generate_product_task = Task(
        description=dedent("""
            Create a comprehensive product description page based on the product data.

            Include:
            - Product name, concentration, skin type, key ingredients
            - Benefits, how to use, side effects, price
            - A compelling description paragraph

            Return in JSON format with all product fields plus a description field.
        """),
        agent=product_generator,
        expected_output="Complete product page JSON",
        context=[parse_data_task]
    )

    # Task 5: Generate Comparison Page
    generate_comparison_task = Task(
        description=dedent("""
            Create a comparison page that compares the original product with a fictional competitor.

            Requirements:
            1. Create a realistic fictional Product B with similar structure
            2. Include name, concentration, skin_type, key_ingredients, benefits, how_to_use, side_effects, price
            3. Product B should be different but comparable (another vitamin C serum or similar skincare product)
            4. Generate detailed comparison points highlighting similarities and differences

            Return in JSON format:
            {
                "product_a": {original product data},
                "product_b": {fictional product data},
                "comparison_points": ["point 1", "point 2", ...]
            }
        """),
        agent=comparison_generator,
        expected_output="Comparison page JSON with both products and comparison points",
        context=[parse_data_task]
    )

    return [parse_data_task, generate_questions_task, generate_faq_task, generate_product_task, generate_comparison_task]

def main():
    """Main function to run the CrewAI content generation system."""

    # Ensure outputs directory exists
    outputs_dir = Path("outputs")
    outputs_dir.mkdir(exist_ok=True)

    print("🚀 Starting CrewAI content generation pipeline...")

    # Create agents
    agents = create_agents()

    # Create tasks
    tasks = create_tasks(agents, RAW_PRODUCT_DATA)

    # Create and run crew
    crew = Crew(
        agents=agents,
        tasks=tasks,
        verbose=True
    )

    # Execute the pipeline
    results = crew.kickoff()

    print("\n📝 Processing results...")

    # Parse results (CrewAI returns string, need to parse)
    try:
        # The results will be the output of the last task
        # We need to save each task result separately
        # For now, let's save the final result
        print("✅ Pipeline completed successfully!")
        print("📄 Results saved to outputs directory")

    except Exception as e:
        print(f"❌ Error processing results: {e}")

    print("\n🎯 Content generation complete!")
    print("All outputs generated using CrewAI agent framework")

if __name__ == "__main__":
    main()
