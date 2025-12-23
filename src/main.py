import json
import os
from pathlib import Path
from .agents import OrchestratorAgent

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

def main():
    """Main function to run the content generation system."""

    # Ensure outputs directory exists
    outputs_dir = Path("outputs")
    outputs_dir.mkdir(exist_ok=True)

    # Initialize orchestrator
    orchestrator = OrchestratorAgent()

    # Execute the pipeline
    print("Starting content generation pipeline...")
    results = orchestrator.execute(RAW_PRODUCT_DATA)

    # Save outputs as JSON files
    print("Saving generated content...")

    # FAQ page
    faq_output = results["faq"].model_dump()
    with open(outputs_dir / "faq.json", "w") as f:
        json.dump(faq_output, f, indent=2)
    print("✓ FAQ page saved to outputs/faq.json")

    # Product page
    product_output = results["product"].model_dump()
    with open(outputs_dir / "product_page.json", "w") as f:
        json.dump(product_output, f, indent=2)
    print("✓ Product page saved to outputs/product_page.json")

    # Comparison page
    comparison_output = results["comparison"].model_dump()
    with open(outputs_dir / "comparison_page.json", "w") as f:
        json.dump(comparison_output, f, indent=2)
    print("✓ Comparison page saved to outputs/comparison_page.json")

    print("\nContent generation complete!")
    print(f"Generated {len(faq_output['faqs'])} FAQ items")
    print("All outputs saved in JSON format as required.")

if __name__ == "__main__":
    main()
