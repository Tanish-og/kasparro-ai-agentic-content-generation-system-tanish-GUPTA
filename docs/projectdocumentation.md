# Project Documentation

## Problem Statement
The challenge is to design a modular, agentic automation system that transforms unstructured or semi-structured product data into high-quality, structured content pages (FAQ, Product Description, Comparison). The system must avoid monolithic script design, ensure deterministic output quality (e.g., minimum question counts), and produce machine-readable JSON files, all while being powered by separate AI agents with distinct responsibilities.

## Solution Overview
This solution implements a multi-agent system using the **CrewAI** framework. It orchestrates specialized agents (Data Validator, Question Generator, FAQ Specialist, Copywriter, Analyst) to process input data through a sequential automation graph. 

Key architectural decisions:
- **Strict Validation**: We use **Pydantic** models not just for output structure but as a "Template Engine" to enforce business logic (e.g., ensuring >= 15 questions are generated).
- **Separation of Concerns**: Logic is decoupled into `agents.py` (roles), `tasks.py` (instructions/templates), `tools.py` (capabilities), and `models.py` (schemas).
- **Hybrid Intelligence**: While LLMs generate content, deterministic Python code (Validators and Tools) acts as a "Gatekeeper" to prevent hallucinations and enforce quantity requirements.

## Scopes & Assumptions
- **Scope**: The system is designed to handle the specific "GlowBoost Vitamin C Serum" dataset but is generic enough to handle similar skincare products via the input JSON.
- **Assumptions**: 
  - The environment provides a valid OpenAI API key.
  - "Product B" for comparison should be a realistic but fictional competitor retrieved via a simulated database tool.
  - Using Pydantic V2 for validation.

## System Design

### 1. Automation Graph (Sequential Pipeline)
The system follows a linear Directed Acyclic Graph (DAG) flow:
1.  **Input Injection**: `inputs/product.json` is loaded.
2.  **Data Validation Agent**: Parses raw JSON validation against the `Product` schema.
3.  **Question Generation Agent**: Brainstorms 25+ questions across 5 categories. *Output optimized via Pydantic Validator logic.*
4.  **FAQ Generation Agent**: Selects the best questions and drafts verified answers.
5.  **Product Page Agent**: Synthesizes a full landing page data structure.
6.  **Comparison Agent**: Uses `CompetitorLookupTool` to fetch fictional Product B data and generates a comparison matrix.

### 2. Logic Blocks & Templates
- **Template Engine**: We define "Templates" as strict Pydantic models in `src/models.py`. These models define the fields, types, and validation rules (e.g., `check_min_questions`) that the content must adhere to.
- **Reusable Logic**:
    - **Validation Logic**: Enforced in `src/models.py`.
    - **Competitor Retrieval Logic**: Encapuslated in `src/tools.py`.
    - **Task Templates**: Reusable prompt structures defined in `src/tasks.py`.

### 3. Agent Boundaries
| Agent | Role | Input | Output |
|-------|------|-------|--------|
| **Data Validator** | Data Parsing | Raw JSON | Validated `Product` Object |
| **Content Strategist** | Ideation | Product Data | `CategorizedQuestions` (>15 items) |
| **Customer Service** | Content Creation | Questions + Data | `FAQPage` (>5 items) |
| **Copywriter** | Synthesis | Product Data | `ProductPage` |
| **Market Analyst** | Research & Compare | Product Data | `ComparisonPage` |

## Output Structure
All final artifacts are saved to `outputs/` as clean JSON:
- `outputs/validated_product.json`
- `outputs/questions.json`
- `outputs/faq.json`
- `outputs/product_page.json`
- `outputs/comparison_page.json`
