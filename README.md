# **GlowBoost Multi-Agent Content Generation System**

An agentic AI pipeline designed for high-integrity e-commerce content generation. This system transforms raw product data into a structured suite of marketing and safety documentation using a decentralized multi-agent architecture.

## **🚀 Overview**

GlowBoost solves the "hallucination" problem in automated content creation. By utilizing a **State-Sharing Orchestration (Blackboard) Pattern**, the system ensures that every marketing claim is grounded in a Pydantic-validated Source of Truth.

### **Key Cognitive Phases**

1. **Inquiry (The Inquisitor):** Generates 15+ high-intent consumer queries based on raw attributes.  
2. **Grounding (The Researcher):** Validates queries against raw data to ensure 100% factual accuracy.  
3. **Synthesis (The Composer):** Assembles validated data into machine-readable JSON templates.

## **🛠️ Tech Stack**

* **Language:** Python 3.9+  
* **Data Validation:** Pydantic (Strict typing and schema enforcement)  
* **Architecture:** Orchestrator-Worker Pattern  
* **Output Format:** Structured JSON (Ready for Headless CMS integration)

## **📋 Features**

* **Zero-Hallucination Guardrails:** Agents are restricted to a closed knowledge base provided at runtime.  
* **Composable Logic Blocks:** Reusable functions for benefit transformation and ingredient analysis.  
* **Persona Simulation:** Generates questions categorized by Safety, Usage, and Value.  
* **Safety Mitigation:** Automatically injects medical disclaimers based on ingredient analysis.

## **Set Up Environment:**  
   python \-m venv venv  
   source venv/bin/activate  \# On Windows: venv\\Scripts\\activate

## **🏃 Usage**

Run the primary pipeline to process raw product data and generate the JSON ecosystem:

python orchestrator.py

The output will be generated in the /output directory:

* FAQ.json: Grounded Q\&A for customer support.  
* ProductPage.json: High-conversion product descriptions.  
* Comparison.json: Competitive analysis against synthetic benchmarks.

## **🧪 Project Structure**

* /agents.py: Contains Inquisitor, Researcher, and Composer logic.  
* /models.py: Pydantic schemas for state and product data.  
* /logic\_blocks.py: Pure functions for data transformation (Logic Blocks).  
* /orchestrator.py: Source of truth JSON files.

