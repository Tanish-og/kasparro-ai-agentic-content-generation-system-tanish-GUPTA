# Kasparro AI Agentic Content Generation System

## Problem Statement

The challenge requires designing and implementing a modular agentic automation system that processes a small product dataset and autonomously generates structured, machine-readable content pages. The system must handle parsing product data, generating categorized user questions, creating templates for different page types, implementing reusable content logic blocks, and assembling three specific pages (FAQ, Product Description, Comparison) as clean JSON outputs. The entire pipeline must run through agents, not as a monolithic script, emphasizing multi-agent workflows, automation graphs, and system design principles.

## Solution Overview

This project implements a multi-agent content generation system using CrewAI framework with specialized agents for different aspects of content creation. The system uses OpenAI's GPT-4 through CrewAI agents to autonomously generate all content without hardcoded fallbacks or fake outputs. The architecture follows proper agent orchestration with clear roles, responsibilities, and task dependencies. The system processes the GlowBoost Vitamin C Serum product data to produce FAQ, product description, and comparison pages in JSON format.

## Scopes & Assumptions

- **Input Data**: Strictly uses only the provided GlowBoost Vitamin C Serum data; no external research or additional facts are added.
- **Product B**: For comparison page, AI generates a fictional but realistic skincare product dynamically.
- **AI Generation**: Uses CrewAI with OpenAI GPT-4 for all content generation - no hardcoded answers or fallbacks.
- **Output Format**: All pages are generated as machine-readable JSON with consistent structure.
- **Agent Framework**: Uses CrewAI (required framework) for proper multi-agent orchestration.
- **Question Count**: Generates at least 15 categorized questions as required.
- **No Fakes**: All content is AI-generated in real-time, no static strings or rule-based fallbacks.

## System Design

### CrewAI Agent Architecture

The system consists of five specialized CrewAI agents, each with distinct roles and expertise:

1. **Data Parser Agent**
   - **Role**: Data Validator
   - **Goal**: Parse and validate raw product data into structured format
   - **Backstory**: Expert data validator ensuring product information is correctly structured
   - **Output**: Validated JSON structure of product data

2. **Question Generator Agent**
   - **Role**: Content Strategist
   - **Goal**: Generate at least 15 categorized user questions based on product data
   - **Backstory**: Creates comprehensive questions that users typically ask about skincare products
   - **Output**: JSON with categorized questions (informational, safety, usage, purchase, comparison)

3. **FAQ Generator Agent**
   - **Role**: Customer Service Specialist
   - **Goal**: Generate detailed FAQ answers based on product information and user questions
   - **Backstory**: Provides accurate, helpful answers to skincare product questions
   - **Output**: JSON structure with product name and FAQ array

4. **Product Description Generator Agent**
   - **Role**: Copywriter
   - **Goal**: Create compelling product descriptions and specifications
   - **Backstory**: Skilled copywriter creating engaging product descriptions for e-commerce
   - **Output**: Complete product page JSON with description

5. **Comparison Generator Agent**
   - **Role**: Market Analyst
   - **Goal**: Create fictional competitor products and detailed comparisons
   - **Backstory**: Market analyst creating realistic competitor products and comparisons
   - **Output**: Comparison page JSON with both products and comparison points

### CrewAI Orchestration Flow

The system uses CrewAI's task orchestration with dependencies:

```
Raw Data → Data Parser Task → Question Generator Task → FAQ Generator Task
                                                         → Product Generator Task
                                                         → Comparison Generator Task → Outputs
```

Key orchestration features:
- **Task Dependencies**: Each task has proper context from previous tasks
- **Sequential Execution**: Agents work in logical order with data flow
- **Real AI Generation**: Every output is generated fresh by GPT-4 through CrewAI
- **No Fallbacks**: All generation happens live, no hardcoded content

### Agent Communication & Context

- **Context Passing**: Task outputs are passed as context to dependent tasks
- **Data Flow**: Product data flows through the entire pipeline
- **Question Integration**: Generated questions feed into FAQ generation
- **Dynamic Content**: All content is generated based on actual product data

### Quality Assurance

- **No Hardcoded Content**: All text is AI-generated in real-time
- **Minimum Requirements Met**: At least 15 questions, 5 FAQ items
- **JSON Structure**: Consistent output formatting
- **Product-Specific Answers**: All responses reference actual product details

## Architecture Diagram

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CrewAI Crew   │───▶│ Data Parser     │───▶│Question Generator│
│   Orchestrator  │    │   Agent         │    │   Agent          │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
┌─────────────────┐    ┌─────────────────┐             ▼
│ FAQ Generator   │◀───│   Context       │    ┌─────────────────┐
│   Agent         │    │   Passing       │    │ Product Generator│
└─────────────────┘    └─────────────────┘    │   Agent          │
         │                                   └─────────────────┘
         ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Comparison      │    │   Outputs       │    │   JSON Files    │
│ Generator Agent │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Technical Implementation

### CrewAI Framework Usage

- **Agent Definition**: Each agent has role, goal, and backstory for proper AI behavior
- **Task Creation**: Tasks define specific objectives with context dependencies
- **Crew Execution**: Orchestrates agent collaboration and task completion
- **Result Processing**: Handles AI-generated content and formats outputs

### Data Models (Pydantic)

- **Product**: Core product data structure
- **FAQPage**: FAQ content with questions and answers
- **ProductPage**: Complete product information
- **ComparisonPage**: Side-by-side product comparison

### Environment & Dependencies

- **CrewAI**: Multi-agent orchestration framework
- **OpenAI GPT-4**: AI content generation
- **Pydantic**: Data validation and models
- **python-dotenv**: Environment variable management

This CrewAI-based design ensures real AI-powered generation without any hardcoded fallbacks, meeting all assignment requirements for genuine agentic systems.
