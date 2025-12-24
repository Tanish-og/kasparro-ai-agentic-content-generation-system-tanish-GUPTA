from crewai import Agent
from .tools import CompetitorLookupTool

def create_agents():
    """Create CrewAI agents with proper tools and capabilities."""

    # Data Parser Agent
    data_parser = Agent(
        role="Data Validator",
        goal="Parse, validate, and structure product data into clean format",
        backstory="You are an expert data validator who ensures product information meets all requirements and is properly structured.",
        tools=[], 
        verbose=True
    )

    # Question Generator Agent
    question_generator = Agent(
        role="Content Strategist",
        goal="Generate exactly 15+ categorized questions for comprehensive FAQ coverage",
        backstory="You are a skilled content strategist who creates detailed, categorized question sets that cover all user concerns about skincare products.",
        tools=[], # Logic enforced by Pydantic model
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

    # Comparison Generator Agent with tool
    comparison_generator = Agent(
        role="Market Analyst",
        goal="Create structured, factual product comparisons with realistic competitors",
        backstory="You are a market analyst who creates detailed, objective product comparisons based on actual specifications.",
        tools=[CompetitorLookupTool()],
        verbose=True
    )

    return data_parser, question_generator, faq_generator, product_generator, comparison_generator
