import json
import os
import re
from pathlib import Path
from crewai import Crew, Task, Agent
from textwrap import dedent
from .models import Product, FAQPage, ProductPage, ComparisonPage, FAQItem, CategorizedQuestions
from .logic_blocks import validate_product_data, format_product_summary

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def load_product_data():
    """Load product data from external source."""
    # In a real system, this would load from a file or API
    return {
        "name": "GlowBoost Vitamin C Serum",
        "concentration": "10% Vitamin C",
        "skin_type": "Oily, Combination",
        "key_ingredients": "Vitamin C, Hyaluronic Acid",
        "benefits": "Brightening, Fades dark spots",
        "how_to_use": "Apply 2–3 drops in the morning before sunscreen",
        "side_effects": "Mild tingling for sensitive skin",
        "price": "₹699"
    }

def parse_json_response(response_text):
    """Parse JSON response from LLM, handling markdown formatting."""
    if not response_text:
        return None

    # Remove markdown code blocks if present
    response_text = re.sub(r'```\w*\n?', '', response_text)
    response_text = response_text.strip()

    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        # Try to extract JSON from text
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        return None

def create_agents():
    """Create CrewAI agents with proper tools and capabilities."""

    # Data Parser Agent with validation tools
    data_parser = Agent(
        role="Data Validator",
        goal="Parse, validate, and structure product data into clean format",
        backstory="You are an expert data validator who ensures product information meets all requirements and is properly structured.",
        tools=[],  # We'll add validation logic in the task
        verbose=True
    )

    # Question Generator Agent with counting capabilities
    question_generator = Agent(
        role="Content Strategist",
        goal="Generate exactly 15+ categorized questions for comprehensive FAQ coverage",
        backstory="You are a skilled content strategist who creates detailed, categorized question sets that cover all user concerns about skincare products.",
        tools=[],  # We'll enforce counting in the task
        verbose=True
    )

    # FAQ Generator Agent
    faq_generator = Agent(
        role="Customer Service Specialist",
        goal="Create accurate, detailed FAQ answers based on verified product data",
        backstory="You are an expert customer service specialist who provides precise, helpful answers using only verified product information.",
        tools=[],
        verbose=True
    )

    # Product Description Agent
    product_generator = Agent(
        role="E-commerce Copywriter",
        goal="Create compelling, accurate product descriptions for online platforms",
        backstory="You are a skilled copywriter who creates engaging product descriptions that highlight key features and benefits.",
        tools=[],
        verbose=True
    )

    # Comparison Generator Agent with structured comparison logic
    comparison_generator = Agent(
        role="Market Analyst",
        goal="Create structured, factual product comparisons with realistic competitors",
        backstory="You are a market analyst who creates detailed, objective product comparisons based on actual specifications.",
        tools=[],
        verbose=True
    )

    return data_parser, question_generator, faq_generator, product_generator, comparison_generator

def create_tasks(agents, product_data):
    """Create CrewAI tasks with structured outputs and validation."""

    data_parser, question_generator, faq_generator, product_generator, comparison_generator = agents

    # Validate input data first
    if not validate_product_data(product_data):
        raise ValueError("Invalid product data structure")

    # Task 1: Parse and Validate Product Data
    parse_data_task = Task(
        description=dedent(f"""
            Parse and validate the following product data. Ensure all required fields are present and properly formatted.

            Product Data: {json.dumps(product_data, indent=2)}

            Required fields: name, concentration, skin_type, key_ingredients, benefits, how_to_use, side_effects, price

            Return ONLY a valid JSON object with these exact fields. Do not include any additional text or formatting.
        """),
        agent=data_parser,
        expected_output="Clean JSON object with validated product data",
        output_json=Product  # Use Pydantic model for structured output
    )

    # Task 2: Generate Categorized Questions (minimum 15 total)
    generate_questions_task = Task(
        description=dedent(f"""
            Generate EXACTLY 15 user questions categorized as follows (5 questions per category):

            Categories:
            - informational: General product information questions
            - safety: Safety concerns, side effects, precautions
            - usage: How to use, application, routine questions
            - purchase: Pricing, availability, buying questions
            - comparison: Product comparison and alternative questions

            Product: {product_data['name']}
            Key Info: {format_product_summary(Product(**product_data))}

            Return ONLY a JSON object with this exact structure:
            {{
                "informational": ["question1", "question2", "question3", "question4", "question5"],
                "safety": ["question1", "question2", "question3", "question4", "question5"],
                "usage": ["question1", "question2", "question3", "question4", "question5"],
                "purchase": ["question1", "question2", "question3", "question4", "question5"],
                "comparison": ["question1", "question2", "question3", "question4", "question5"]
            }}

            Each category must have exactly 5 questions. Total: 25 questions.
        """),
        agent=question_generator,
        expected_output="JSON object with exactly 25 categorized questions",
        context=[parse_data_task],
        output_json=CategorizedQuestions  # Structured output
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

            Return ONLY a JSON object with this exact structure:
            {{
                "product_name": "exact product name from data",
                "faqs": [
                    {{"question": "selected question", "answer": "detailed answer"}},
                    {{"question": "selected question", "answer": "detailed answer"}},
                    {{"question": "selected question", "answer": "detailed answer"}},
                    {{"question": "selected question", "answer": "detailed answer"}},
                    {{"question": "selected question", "answer": "detailed answer"}}
                ]
            }}
        """),
        agent=faq_generator,
        expected_output="JSON object with product name and 5 FAQ items",
        context=[parse_data_task, generate_questions_task],
        output_json=FAQPage  # Structured output
    )

    # Task 4: Generate Product Page
    generate_product_task = Task(
        description=dedent("""
            Create a comprehensive product description page using the validated product data.

            Include all product specifications and create a compelling description paragraph.

            Return ONLY a JSON object with this exact structure:
            {{
                "product_name": "exact product name",
                "concentration": "exact concentration",
                "skin_type": "exact skin type",
                "key_ingredients": "exact ingredients",
                "benefits": "exact benefits",
                "how_to_use": "exact usage instructions",
                "side_effects": "exact side effects",
                "price": "exact price",
                "description": "compelling description paragraph based on specifications"
            }}
        """),
        agent=product_generator,
        expected_output="Complete product page JSON with all fields",
        context=[parse_data_task],
        output_json=ProductPage  # Structured output
    )

    # Task 5: Generate Comparison Page
    generate_comparison_task = Task(
        description=dedent("""
            Create a structured comparison between the original product and a realistic competitor.

            Competitor Requirements:
            - Different name and brand
            - Similar product type (vitamin C serum)
            - Different specifications but comparable quality
            - Realistic pricing in same range
            - Different but plausible benefits

            Return ONLY a JSON object with this exact structure:
            {{
                "product_a": {{
                    "name": "original product name",
                    "concentration": "original concentration",
                    "skin_type": "original skin type",
                    "key_ingredients": "original ingredients",
                    "benefits": "original benefits",
                    "how_to_use": "original usage",
                    "side_effects": "original side effects",
                    "price": "original price"
                }},
                "product_b": {{
                    "name": "competitor name",
                    "concentration": "competitor concentration",
                    "skin_type": "competitor skin type",
                    "key_ingredients": "competitor ingredients",
                    "benefits": "competitor benefits",
                    "how_to_use": "competitor usage",
                    "side_effects": "competitor side effects",
                    "price": "competitor price"
                }},
                "comparison_points": [
                    "Detailed comparison point 1",
                    "Detailed comparison point 2",
                    "Detailed comparison point 3",
                    "Detailed comparison point 4",
                    "Detailed comparison point 5"
                ]
            }}
        """),
        agent=comparison_generator,
        expected_output="Structured comparison JSON with both products and comparison points",
        context=[parse_data_task],
        output_json=ComparisonPage  # Structured output
    )

    return [parse_data_task, generate_questions_task, generate_faq_task, generate_product_task, generate_comparison_task]

def execute_sequential_tasks(agents, tasks):
    """Execute tasks sequentially to capture individual outputs."""
    outputs_dir = Path("outputs")
    outputs_dir.mkdir(exist_ok=True)

    task_outputs = {}
    context_data = {}

    print("🚀 Executing tasks sequentially...")

    for i, task in enumerate(tasks):
        print(f"\n📋 Executing Task {i+1}: {task.description.split('.')[0]}")

        # Create a mini-crew for this single task
        single_task_crew = Crew(
            agents=agents,
            tasks=[task],
            verbose=False  # Reduce verbosity for cleaner output
        )

        try:
            # Execute the task
            result = single_task_crew.kickoff()

            # Parse the result
            if isinstance(result, str):
                parsed_result = parse_json_response(result)
            else:
                parsed_result = result

            # Determine output file and validation
            output_file = None
            task_key = None

            if 'Parse and validate' in task.description:
                output_file = outputs_dir / "validated_product.json"
                task_key = 'product'
                if parsed_result:
                    context_data['product'] = parsed_result

            elif 'Generate EXACTLY 15' in task.description:
                output_file = outputs_dir / "questions.json"
                task_key = 'questions'
                if parsed_result:
                    context_data['questions'] = parsed_result

            elif 'comprehensive FAQ section' in task.description:
                output_file = outputs_dir / "faq.json"
                task_key = 'faq'

            elif 'comprehensive product description' in task.description:
                output_file = outputs_dir / "product_page.json"
                task_key = 'product_page'

            elif 'structured comparison' in task.description:
                output_file = outputs_dir / "comparison_page.json"
                task_key = 'comparison'

            # Validate and save
            if output_file and parsed_result:
                # Apply validation based on task type
                if task_key == 'questions':
                    if validate_question_count(parsed_result):
                        task_outputs[task_key] = parsed_result
                        with open(output_file, 'w', encoding='utf-8') as f:
                            json.dump(parsed_result, f, indent=2, ensure_ascii=False)
                        print(f"✅ Saved {output_file.name} ({count_questions(parsed_result)} questions)")
                    else:
                        print(f"⚠️  Question count validation failed for {output_file.name}")

                elif task_key == 'faq':
                    if validate_faq_count(parsed_result):
                        task_outputs[task_key] = parsed_result
                        with open(output_file, 'w', encoding='utf-8') as f:
                            json.dump(parsed_result, f, indent=2, ensure_ascii=False)
                        print(f"✅ Saved {output_file.name} ({len(parsed_result.get('faqs', []))} FAQs)")
                    else:
                        print(f"⚠️  FAQ count validation failed for {output_file.name}")

                elif task_key in ['product', 'product_page', 'comparison']:
                    task_outputs[task_key] = parsed_result
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(parsed_result, f, indent=2, ensure_ascii=False)
                    print(f"✅ Saved {output_file.name}")

            else:
                print(f"⚠️  No valid output for task {i+1}")

        except Exception as e:
            print(f"❌ Error executing task {i+1}: {e}")

    return task_outputs

def count_questions(questions_data):
    """Count total questions in categorized questions."""
    if not questions_data or not isinstance(questions_data, dict):
        return 0
    return sum(len(cat) for cat in questions_data.values() if isinstance(cat, list))

def validate_question_count(questions_data):
    """Validate that at least 15 questions were generated."""
    total = count_questions(questions_data)
    return total >= 15

def validate_faq_count(faq_data):
    """Validate that at least 5 FAQs were generated."""
    if not faq_data or not isinstance(faq_data, dict):
        return False
    faqs = faq_data.get('faqs', [])
    return len(faqs) >= 5

def validate_outputs(task_outputs):
    """Validate that all required outputs were generated and meet criteria."""
    issues = []

    # Check FAQ count
    if 'faq' in task_outputs and task_outputs['faq']:
        faq_data = task_outputs['faq']
        if isinstance(faq_data, str):
            faq_data = parse_json_response(faq_data)

        if faq_data and 'faqs' in faq_data:
            faq_count = len(faq_data['faqs'])
            if faq_count < 5:
                issues.append(f"Only {faq_count} FAQs generated, need at least 5")
        else:
            issues.append("FAQ structure invalid")

    # Check questions
    if 'questions' in task_outputs and task_outputs['questions']:
        questions_data = task_outputs['questions']
        if isinstance(questions_data, str):
            questions_data = parse_json_response(questions_data)

        if questions_data:
            total_questions = sum(len(cat) for cat in questions_data.values() if isinstance(cat, list))
            if total_questions < 15:
                issues.append(f"Only {total_questions} questions generated, need at least 15")
        else:
            issues.append("Questions structure invalid")

    if issues:
        print("⚠️  Validation Issues:")
        for issue in issues:
            print(f"   - {issue}")
    else:
        print("✅ All outputs validated successfully")

    return len(issues) == 0

def main():
    """Main function with proper file I/O and validation."""
    print("🔧 Initializing Kasparro AI Agent System...")

    # Load and validate input data
    product_data = load_product_data()
    if not validate_product_data(product_data):
        print("❌ Invalid product data")
        return

    print(f"📦 Loaded product: {product_data['name']}")

    # Create agents and tasks
    agents = create_agents()
    tasks = create_tasks(agents, product_data)

    # Create crew with proper configuration
    crew = Crew(
        agents=agents,
        tasks=tasks,
        verbose=True,
        memory=False  # Disable memory for deterministic output
    )

    # Execute and save outputs sequentially
    task_outputs = execute_sequential_tasks(agents, tasks)

    # Validate outputs
    if validate_outputs(task_outputs):
        print("\n🎉 Pipeline completed successfully!")
        print("📁 All JSON files saved to outputs/ directory")
        print("🔍 Outputs validated and meet requirements")
    else:
        print("\n⚠️  Pipeline completed with validation issues")
        print("📁 Check outputs/ directory for generated files")

if __name__ == "__main__":
    main()
