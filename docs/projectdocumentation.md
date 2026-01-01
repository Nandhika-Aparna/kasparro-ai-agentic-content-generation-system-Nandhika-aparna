Project Documentation: GlowBoost Multi-Agent Content Generation System

1. Problem Statement

In modern e-commerce, manual content creation is a bottleneck that scales poorly and is prone to human error or "hallucinated" marketing claims. Traditional automated systems often rely on monolithic scripts that lack flexibility and factual grounding.

The challenge is to build a system that takes raw product attributes (Source of Truth) and autonomously generates a multi-page, structured content suite (FAQ, Product Page, and Comparison Analysis) while maintaining 100% factual integrity and architectural modularity.

2. Solution Overview

The GlowBoost Multi-Agent System is a decentralized, autonomous agentic environment designed to transform raw product data into a high-conversion content ecosystem.

Instead of a hard-coded sequential script, this solution employs a Dynamic Coordination Loop (Convergence Pattern). The system utilizes three independent agents that interact through a shared state:

The Inquisitor: Simulates customer personas to expand raw data into 15+ high-intent queries.

The Researcher: Autonomously grounds and verifies data against the Pydantic-validated "Source of Truth."

The Composer: Assembles final structured JSON artifacts using reusable logic blocks and templates.

3. Scopes & Assumptions

Scope

Autonomous Coordination: Agents decide when to act based on environmental triggers.

Data Validation: Strict type-enforcement using Pydantic models.

Competitive Intelligence: Programmatic comparison between a primary product and synthetic competitors.

Output: Machine-readable JSON files (faq.json, product_page.json, comparison_page.json).

Assumptions

Closed Knowledge Base: The system uses only provided data to prevent unauthorized claims.

Convergence: The pipeline is considered complete when all agents report no further work to perform.

Zero-Knowledge External: No external research is performed to ensure compliance with the provided dataset.

4. System Design

4.1 Architectural Pattern: Dynamic Orchestration (Blackboard)

The system moves beyond a standard Directed Acyclic Graph (DAG) to a Blackboard Architecture:

The Shared State (AgenticState): Acts as the central environment. Agents monitor this state and act when specific conditions are met.

Agent Autonomy: Each agent implements a can_process() sensor. The Orchestrator does not "call" agents in a fixed order; it hosts a loop where agents autonomously take control when they detect relevant work.

4.2 Reusable Logic Blocks

Transformation rules are encapsulated in "Pure Functions" within logic_blocks.py:

Benefits Transformer: Maps product benefits to marketing-optimized bullets.

Comparison Logic: Programmatically determines price deltas and unique ingredient propositions.

Protocol Extractor: Merges usage steps and safety warnings into a coherent protocol.

4.3 Template Engine Design

Templates are defined as structured schemas within the ComposerAgent. This allows for:

Consistency: Ensures every JSON output follows a predictable, machine-readable structure.

Modularity: Formatting rules are decoupled from the raw data gathering process.

4.4 The Agentic Pipeline Flow (Convergence)

Validation: The Orchestrator initializes the AgenticState and validates raw inputs.

The Autonomous Loop:

Inquisitor detects empty question sets and populates inquiries.

Researcher detects unverified questions and applies grounding logic.

Composer detects a completed knowledge base and assembles the final pages.

Termination: The loop breaks once all agents return False for their activation triggers.

Export: Final artifacts are flushed to the local file system.

5. Visual Representation

System Architecture Flow

[ Raw Data ] --> [ Pydantic Validator ] 
                 |
         [ AgenticState (Blackboard) ] <-----------------------
                 |                                            |
         ------------------------------------------           |
         |                |               |               |
  [Inquisitor]     [Researcher]    [Composer]      [Audit Log]
  (Ideation)       (Grounding)     (Synthesis)     (Tracking)
         |                |               |               |
         ------------------------------------------           |
                 |                                            |
                 ----------------------------------------------
                                 |
                        [ Content Output ]
            (faq.json | product_page.json | comparison_page.json)


Logical Sequence (Autonomous)

Trigger: orchestrator.run_pipeline() starts.

Observation: Agents poll the AgenticState.

Action: Inquisitor acts first as its trigger (empty questions) is met.

Reaction: Researcher observes the new questions and begins verification.

Finalization: Composer observes that len(grounded_data) == len(questions) and triggers assembly.

Delivery: Orchestrator writes the final_pages map to JSON files.