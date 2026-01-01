Project Documentation: GlowBoost Multi-Agent Content Generation System

1. Problem Statement

In modern e-commerce and dermatological technology, manual content creation for product catalogs is a bottleneck that scales poorly and is prone to human error or "hallucinated" marketing claims. Traditional automated systems often rely on monolithic scripts that lack flexibility, factual grounding, and the ability to handle complex reasoning—such as competitive analysis or safety risk mitigation.

The challenge is to build a system that can take a minimal set of raw product attributes (Source of Truth) and autonomously generate a multi-page, structured content suite (FAQ, Product Page, and Comparison Analysis) while maintaining 100% factual integrity and architectural modularity.

2. Solution Overview

The GlowBoost Multi-Agent System is a decentralized agentic pipeline designed to transform raw product data into a high-conversion, machine-readable content ecosystem.

Instead of a single execution block, the solution employs a "State-Sharing Orchestration" pattern. The system breaks down the content lifecycle into three distinct cognitive phases:

Inquiry Generation (The Inquisitor): Simulating customer personas to expand raw data into 15+ high-intent queries.

Fact-Checking & Grounding (The Researcher): Cross-referencing queries against a Pydantic-validated "Source of Truth" to ensure zero hallucinations.

Content Synthesis (The Composer): Transforming validated data points into structured JSON templates using reusable logic blocks.

This modular approach ensures that each stage of the pipeline can be scaled, tested, and audited independently.

3. Scopes & Assumptions

Scope

Data Validation: Strict type-enforcement using Pydantic models.

Persona Simulation: Automated generation of Categorized Questions (Safety, Usage, Value, etc.).

Competitive Intelligence: Programmatic comparison between a primary product and synthetic competitors.

Safety Guardrails: Automatic detection of medical keywords and insertion of required disclaimers.

Output: Production-ready, machine-readable JSON files.

Assumptions

Closed Knowledge Base: The system operates under a "Zero-Knowledge" external assumption, utilizing only provided data to prevent unauthorized medical claims.

Sequential Execution: While agents are logically independent, the current implementation follows a linear Directed Acyclic Graph (DAG) for state consistency.

Consumer Safety: It is assumed that "Side Effects" data provided in the source is the absolute limit of safety information available to the system.

4. System Design (Mandatory)

4.1 Architectural Pattern: Orchestrator-Worker

The system utilizes a Message-Passing Orchestrator pattern. A central AgenticState object acts as the "Environment" or "Blackboard" where agents read and write data.

The Shared State: Every agent receives the current AgenticState. They do not communicate with each other directly; they only modify the state. This decouples the "Inquisitor" from the "Composer," allowing for asynchronous or parallel processing.

Pydantic Data Contracts: To prevent "state drift," every data object (Product, Question, State) is governed by a Pydantic model. This ensures that if one agent produces malformed data, the pipeline halts immediately rather than propagating errors.

4.2 Reusable Logic Blocks

To satisfy the requirement for composable engineering, content transformation is moved into "Pure Functions" within logic_blocks.py:

Benefits Transformer: Converts raw strings into high-conversion marketing bullets.

Ingredient Clash Logic: Performs set-intersection analysis to determine shared vs. unique active ingredients between products.

Protocol Merger: Combines usage steps with safety warnings to create a cohesive "Application Protocol."

4.3 Template Engine Design

The templates are defined as Structured JSON Schemas rather than string literals.

Dynamic Mapping: The ComposerAgent maps grounded data points into specific keys within the final output dictionary.

Machine-Readability: By outputting JSON, the system supports headless CMS integration, mobile apps, and dynamic web components simultaneously.

4.4 The Agentic Pipeline Flow (Sequence)

Initialization: main.py validates the raw JSON and populates the SystemState.

Expansion: InquisitorAgent generates 15+ questions across 5 categories based on product attributes.

Verification: ResearcherAgent scans the ProductModel to provide answers and attaches an is_grounded flag.

Composition: ComposerAgent calls logic blocks to assemble the final FAQ, product page, and comparison objects.

Export: The Orchestrator flushes the state to distinct JSON files.

5. Visual Representation

System Architecture Flow

[ Raw Data ] --> [ Pydantic Validator ] 
                 |
         [ AgenticState (Blackboard) ]
                 |
         ------------------------------------------
         |                |               |
  [Inquisitor]  -->  [Researcher] --> [Composer]
  (15+ Queries)      (Grounding)      (Templates)
         |                |               |
         ------------------------------------------
                 |
         [ Content Output ]
    (FAQ.json | Product.json | Comp.json)


Logical Sequence Diagram

Trigger: System executes run_pipeline.py.

Load: Orchestrator loads GlowBoost data into AgenticState.

Inquire: Inquisitor reads State -> Appends 15+ Question objects.

Research: Researcher reads State -> Maps Questions to Product attributes -> Appends Grounded Answers.

Compose: Composer reads Grounded Data -> Executes Logic Blocks -> Populates Page Templates.

Deliver: Orchestrator writes results to local JSON files.