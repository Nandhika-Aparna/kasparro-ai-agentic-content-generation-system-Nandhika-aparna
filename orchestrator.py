import json
import os
from models import Product, AgenticState
from agents import InquisitorAgent, ResearcherAgent, ComposerAgent
from dotenv import load_dotenv

# Load environment variables (API Key)
load_dotenv()

# --- CONFIGURATION ---
# Set USE_MOCK to True to run without an OpenAI API Key
# Set USE_MOCK to False once you add your key to the .env file
USE_MOCK = True 

class KasparroOrchestrator:
    def __init__(self, raw_data: dict, competitor_data: dict):
        self.state = AgenticState(raw_input=raw_data)
        self.raw_competitor = competitor_data
        
        # Modular Agent Registration: These agents operate independently
        # Note: If agents are updated to use LLMs, pass USE_MOCK to them here.
        self.agents = [
            InquisitorAgent(), 
            ResearcherAgent(), 
            ComposerAgent()
        ]

    def run_pipeline(self):
        """
        Implements an Autonomous Coordination Loop.
        Instead of static sequential logic, agents monitor the shared state 
        and execute based on internal autonomy logic (can_process).
        """
        mode_label = "MOCK MODE (No API usage)" if USE_MOCK else "LIVE API MODE"
        print(f"--- Starting Agentic Orchestration [{mode_label}] ---")
        
        # Initial Validation: Converting raw input to clean internal Pydantic models
        try:
            self.state.product_model = Product(**self.state.raw_input)
            self.state.competitor_model = Product(**self.raw_competitor)
            self.state.logs.append(f"Models validated for {self.state.product_model.name}")
        except Exception as e:
            print(f"❌ Validation Error: {e}")
            return

        # DYNAMIC CONVERGENCE LOOP
        # This replaces static control flow with dynamic orchestration.
        # The system continues to iterate until no agent has further work to perform.
        max_iterations = 10
        for i in range(max_iterations):
            work_done_this_round = False
            
            for agent in self.agents:
                # Agent Autonomy: The agent decides if it should act based on the environment
                if agent.can_process(self.state):
                    print(f"🤖 Agent [{agent.__class__.__name__}] is taking control...")
                    agent.process(self.state)
                    work_done_this_round = True
            
            # If no agent acted, the system has reached its goal state
            if not work_done_this_round:
                print("🏁 No more agents require processing. Pipeline converged.")
                break

        self.export_artifacts()

    def export_artifacts(self):
        """Standardized JSON export for machine-readable results."""
        print("\n💾 Exporting generated pages...")
        for page_name, content in self.state.final_pages.items():
            if content:
                filename = f"{page_name}.json"
                try:
                    with open(filename, "w", encoding="utf-8") as f:
                        json.dump(content, f, indent=4, ensure_ascii=False)
                    print(f"✔️ Exported: {filename}")
                except Exception as e:
                    print(f"❌ Error exporting {filename}: {e}")

        # Final Audit Trail
        print("\n--- System Audit Trail ---")
        for log in self.state.logs:
            print(f"✅ {log}")

if __name__ == "__main__":
    # Primary product data (Requirement #1)
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
    
    # Fictional Product B for Comparison Page (Requirement #5)
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
    
    # Initialize and execute the autonomous system
    orchestrator = KasparroOrchestrator(glow_boost_dataset, radiant_c_dataset)
    orchestrator.run_pipeline()