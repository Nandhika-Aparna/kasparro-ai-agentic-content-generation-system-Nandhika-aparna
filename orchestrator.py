"""
KASPARRO ORCHESTRATOR
Manages the shared state and coordinates independent agents.
Supports switching between LIVE API and MOCK MODE for development.
"""
import json
import os
from models import Product, AgenticState
from agents import InquisitorAgent
from agents import ResearcherAgent, ComposerAgent
from dotenv import load_dotenv

# Load environment variables (API Key)
load_dotenv()

# --- CONFIGURATION ---
# Set USE_MOCK to True to run without an OpenAI API Key
# Set USE_MOCK to False once you add your key to the .env file
USE_MOCK = True 

class KasparroOrchestrator:
    def __init__(self, raw_data: dict, competitor_data: dict):
        # Initialize Shared State
        self.state = AgenticState(raw_input=raw_data)
        self.raw_competitor = competitor_data
        
        # Initialize Agents
        # Note: We use a try-except block here to handle cases where 
        # agent_inquisitor.py hasn't been updated with the use_mock parameter yet.
        try:
            inquisitor = InquisitorAgent(use_mock=USE_MOCK)
        except TypeError:
            print("⚠️ Warning: InquisitorAgent class does not yet support 'use_mock' parameter.")
            print("Falling back to default initialization.")
            inquisitor = InquisitorAgent()

        self.agents = [
            inquisitor,
            ResearcherAgent(),
            ComposerAgent()
        ]

    def run_pipeline(self):
        mode_label = "MOCK MODE (No API usage)" if USE_MOCK else "LIVE API MODE"
        print(f"--- Starting Agentic Orchestration [{mode_label}] ---")
        
        # Step 1: Initialize and validate product models via Pydantic
        try:
            self.state.product_model = Product(**self.state.raw_input)
            self.state.competitor_model = Product(**self.raw_competitor)
            self.state.logs.append(f"State initialized for {self.state.product_model.name}")
        except Exception as e:
            print(f"❌ Validation Error: {e}")
            return
        
        # Step 2: Agent Processing
        # Agents update self.state autonomously
        for agent in self.agents:
            agent_name = agent.__class__.__name__
            print(f"🤖 Agent [{agent_name}] is processing...")
            
            # For the InquisitorAgent, we call generate_questions as per its specific implementation
            # This ensures compatibility between the specialized Inquisitor and generic Workers
            if hasattr(agent, 'generate_questions'):
                self.state.questions = agent.generate_questions(self.state.product_model)
            else:
                agent.process(self.state)
                
            self.state.logs.append(f"{agent_name} processing complete.")
            
        # Step 3: Export 3 JSON Files (Machine-Readable Artifacts)
        print("\n💾 Exporting generated pages...")
        for page_name, content in self.state.final_pages.items():
            filename = f"{page_name}.json"
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    # ensure_ascii=False handles the Rupee (₹) symbol correctly
                    json.dump(content, f, indent=4, ensure_ascii=False)
                print(f"✔️ Generated: {filename}")
            except Exception as e:
                print(f"❌ Error exporting {filename}: {e}")

        # Step 4: Final Audit Trail
        print("\n--- System Audit Trail ---")
        for log in self.state.logs:
            print(f"✅ {log}")

if __name__ == "__main__":
    # Primary product data
    glow_boost_dataset = {
        "name": "GlowBoost Vitamin C Serum",
        "concentration": "10% Vitamin C",
        "skin_types": ["Oily", "Combination"],
        "key_ingredients": ["Vitamin C", "Hyaluronic Acid"],
        "benefits": ["Brightening", "Fades dark spots"],
        "usage_instructions": "Apply 2-3 drops in the morning before sunscreen",
        "side_effects": "Mild tingling for sensitive skin",
        "price_in_inr": 699
    }
    
    # Competitor data for comparison logic
    radiant_c_dataset = {
        "name": "Radiant-C Premium",
        "concentration": "15% Vitamin C",
        "skin_types": ["Dry", "Normal"],
        "key_ingredients": ["Vitamin C", "Ferulic Acid"],
        "benefits": ["Anti-aging", "Hydration"],
        "usage_instructions": "Apply once daily at night",
        "side_effects": "Redness if used with Retinol",
        "price_in_inr": 1299
    }
    
    # Run the system
    orchestrator = KasparroOrchestrator(glow_boost_dataset, radiant_c_dataset)
    orchestrator.run_pipeline()