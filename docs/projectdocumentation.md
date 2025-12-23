# Kasparro AI Agentic Content Generation System

## Problem Statement

The challenge requires designing and implementing a modular agentic automation system that processes a small product dataset and autonomously generates structured, machine-readable content pages. The system must handle parsing product data, generating categorized user questions, creating templates for different page types, implementing reusable content logic blocks, and assembling three specific pages (FAQ, Product Description, Comparison) as clean JSON outputs. The entire pipeline must run through agents, not as a monolithic script, emphasizing multi-agent workflows, automation graphs, and system design principles.

## Solution Overview

This project implements a multi-agent content generation system using Python with Pydantic for data modeling and OpenAI's GPT for intelligent content generation. The architecture follows a modular design with clear agent boundaries, a sequential orchestration flow, reusable logic blocks for content transformation, and a custom template engine for structured output generation. The system processes the GlowBoost Vitamin C Serum product data to produce FAQ, product description, and comparison pages in JSON format.

## Scopes & Assumptions

- **Input Data**: Strictly uses only the provided GlowBoost Vitamin C Serum data; no external research or additional facts are added.
- **Product B**: For comparison page, creates a fictional but realistic skincare product with structured attributes.
- **AI Generation**: Leverages OpenAI's GPT-4 for content generation within defined templates and logic blocks.
- **Output Format**: All pages are generated as machine-readable JSON with consistent structure.
- **Agent Architecture**: Each agent has single responsibility, defined I/O, and operates without global state.
- **Orchestration**: Uses a linear pipeline flow for simplicity and reliability.
- **Dependencies**: Requires OpenAI API key for LLM functionality.

## System Design

### Agent Architecture

The system consists of four specialized agents, each with clear boundaries and responsibilities:

1. **DataParser Agent**
   - **Responsibility**: Parse and validate raw product data into structured internal model
   - **Input**: Raw product dictionary
   - **Output**: Validated Product Pydantic model
   - **Logic**: Converts string data to typed, validated structure

2. **QuestionGenerator Agent**
   - **Responsibility**: Generate at least 15 categorized user questions based on product data
   - **Input**: Product model
   - **Output**: Dictionary of categorized questions
   - **Logic**: Uses LLM to create relevant questions across categories (Informational, Safety, Usage, Purchase, Comparison)

3. **ContentAssembler Agent**
   - **Responsibility**: Assemble content pages using templates and logic blocks
   - **Input**: Product model, questions, template type
   - **Output**: JSON-structured page content
   - **Logic**: Applies appropriate logic blocks and templates for each page type

4. **Orchestrator Agent**
   - **Responsibility**: Coordinate the entire pipeline execution
   - **Input**: Raw product data
   - **Output**: Complete set of generated JSON pages
   - **Logic**: Executes agents in sequence, manages data flow

### Orchestration Flow

The system uses a sequential pipeline orchestration:

```
Raw Data → DataParser → QuestionGenerator → ContentAssembler (FAQ) → ContentAssembler (Product) → ContentAssembler (Comparison) → JSON Outputs
```

This linear flow ensures:
- Data validation before processing
- Question generation before content assembly
- Independent page generation with shared context
- Clear error propagation and debugging

### Reusable Logic Blocks

Logic blocks are pure functions that transform data into content:

1. **generate_benefits_description(product)**: Creates compelling benefit descriptions
2. **extract_usage_instructions(product)**: Formats usage instructions
3. **create_safety_summary(product)**: Summarizes safety information
4. **generate_comparison_points(product_a, product_b)**: Creates comparison bullet points
5. **select_faq_questions(questions, count)**: Intelligently selects relevant FAQ questions

### Template Engine

Custom template definitions as structured dictionaries:

```python
faq_template = {
    "fields": ["questions", "answers"],
    "rules": ["select_top_questions", "generate_answers"],
    "formatting": "q_and_a_pairs",
    "dependencies": ["question_selector", "answer_generator"]
}
```

Templates ensure consistent output structure while allowing flexibility in content generation.

### Data Flow & State Management

- Each agent maintains no internal state
- Data flows unidirectionally through the pipeline
- Pydantic models ensure type safety and validation
- JSON serialization handles output formatting

### Error Handling & Robustness

- Input validation at each agent boundary
- Graceful degradation for LLM failures
- Structured error messages for debugging
- Type checking with Pydantic models

### Scalability Considerations

- Modular agent design allows easy addition of new page types
- Logic blocks can be reused across different products
- Template system supports customization without code changes
- Agent boundaries enable potential parallelization

## Architecture Diagram

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Orchestrator  │───▶│   DataParser    │───▶│QuestionGenerator│
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
┌─────────────────┐    ┌─────────────────┐             ▼
│ ContentAssembler│◀───│   Logic Blocks  │    ┌─────────────────┐
│     (FAQ)       │    │                 │    │   Templates     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │
         ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ ContentAssembler│    │ ContentAssembler│    │ ContentAssembler│
│   (Product)     │    │  (Comparison)   │    │    Outputs      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

This design ensures modularity, testability, and maintainability while meeting all assignment requirements.
