import json
import os
from pathlib import Path
from crewai import Crew
from dotenv import load_dotenv

from .models import Product, CategorizedQuestions, FAQPage, ProductPage, ComparisonPage
from .agents import create_agents
from .tasks import create_tasks

# Load environment variables
load_dotenv()

def load_product_data(filepath: str) -> dict:
    """Load product data from external JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file not found: {filepath}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in input file: {filepath}")

def save_json(data: dict, filepath: Path):
    """Save dictionary to JSON file."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {filepath}")

def main():
    print("🔧 Initializing Kasparro AI Agent System...")
    
    # 1. Load Data
    try:
        inputs_path = Path("inputs/product.json")
        product_data = load_product_data(str(inputs_path))
        print(f"📦 Loaded product: {product_data.get('name')}")
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return

    # 2. Setup Agents and Tasks
    agents = create_agents()
    tasks = create_tasks(agents, product_data)
    
    # 3. Create Crew
    crew = Crew(
        agents=agents,
        tasks=tasks,
        verbose=True,
        memory=False # Deterministic
    )

    # 4. Execute
    print("🚀 executing crew...")
    try:
        # Kickoff returns the final task output, but we need intermediate outputs too
        # In modern CrewAI, we can access task.output after execution
        crew.kickoff() 
        
        # 5. Extract and Save Outputs (Real File I/O)
        outputs_dir = Path("outputs")
        
        # Mapping tasks to output filenames based on expected type
        # We know the order of tasks from create_tasks:
        # 0: validated_product (Product)
        # 1: questions (CategorizedQuestions)
        # 2: faq (FAQPage)
        # 3: product_page (ProductPage)
        # 4: comparison (ComparisonPage)
        
        # Retrieve Pydantic models from task outputs
        validated_product = tasks[0].output.pydantic
        questions = tasks[1].output.pydantic
        faq_page = tasks[2].output.pydantic
        product_page = tasks[3].output.pydantic
        comparison_page = tasks[4].output.pydantic

        # Save files
        if validated_product:
            save_json(validated_product.model_dump(), outputs_dir / "validated_product.json")
        else:
            print("⚠️ Failed to get Validated Product output")

        if questions:
            save_json(questions.model_dump(), outputs_dir / "questions.json")
        else:
            print("⚠️ Failed to get Questions output")

        if faq_page:
            save_json(faq_page.model_dump(), outputs_dir / "faq.json")
        else:
            print("⚠️ Failed to get FAQ output")
            
        if product_page:
            save_json(product_page.model_dump(), outputs_dir / "product_page.json")
        else:
            print("⚠️ Failed to get Product Page output")
            
        if comparison_page:
            save_json(comparison_page.model_dump(), outputs_dir / "comparison_page.json")
        else:
            print("⚠️ Failed to get Comparison output")

        print("\n🎉 Pipeline completed successfully!")

    except Exception as e:
        print(f"\n❌ Pipeline failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
