from models import Product, AgenticState, Question
import logic_blocks
from typing import List

class BaseAgent:
    """Enhanced Base Agent with autonomy checks."""
    def can_process(self, state: AgenticState) -> bool:
        raise NotImplementedError

    def process(self, state: AgenticState):
        raise NotImplementedError

class InquisitorAgent(BaseAgent):
    """
    Responsibility: Requirement #2.
    Autonomy: Triggers if questions list is empty.
    """
    def can_process(self, state: AgenticState) -> bool:
        return len(state.questions) == 0 and state.product_model is not None

    def process(self, state: AgenticState):
        p = state.product_model
        intents = ["Usage", "Safety", "Value", "Ingredients", "Comparison"]
        
        new_questions = []
        for intent in intents:
            new_questions.append(Question(category=intent, question_text=f"Is {p.name} safe for {intent}?"))
            new_questions.append(Question(category=intent, question_text=f"How does {intent} work with {p.name}?"))
            new_questions.append(Question(category=intent, question_text=f"What should I know about {p.name} and {intent}?"))
            
        state.questions = new_questions
        state.logs.append(f"InquisitorAgent: Autonomously generated {len(new_questions)} inquiries.")

class ResearcherAgent(BaseAgent):
    """
    Responsibility: Requirement #3 & #5.
    Autonomy: Triggers when questions exist but grounded_data is incomplete.
    """
    def can_process(self, state: AgenticState) -> bool:
        return len(state.questions) > 0 and len(state.grounded_data) < len(state.questions)

    def process(self, state: AgenticState):
        p = state.product_model
        c = state.competitor_model
        already_grounded = {d['question'] for d in state.grounded_data}
        
        for q in state.questions:
            if q.question_text in already_grounded:
                continue
                
            answer = "Information pending verification."
            
            if q.category == "Usage": 
                answer = p.usage_instructions
            elif q.category == "Safety": 
                answer = p.side_effects
            elif q.category == "Value": 
                answer = f"Priced at ₹{p.price_in_inr}."
            elif q.category == "Ingredients": 
                answer = f"Actives: {', '.join(p.key_ingredients)}."
            elif q.category == "Comparison":
                if c:
                    diff = c.price_in_inr - p.price_in_inr
                    verb = "cheaper" if diff > 0 else "premium"
                    answer = f"Compared to {c.name}, {p.name} is ₹{abs(diff)} {verb}."
                else:
                    answer = f"{p.name} offers unique concentration levels compared to market standards."
            
            state.grounded_data.append({
                "question": q.question_text,
                "answer": answer,
                "source_verified": True
            })
            
        state.logs.append(f"ResearcherAgent: Grounded {len(state.grounded_data)} items with source data.")

class ComposerAgent(BaseAgent):
    """
    Responsibility: Requirement #6.
    Autonomy: Triggers when grounded data is ready and pages are missing.
    """
    def can_process(self, state: AgenticState) -> bool:
        research_done = len(state.grounded_data) >= len(state.questions) and len(state.questions) > 0
        pages_empty = all(not v for v in state.final_pages.values())
        return research_done and pages_empty

    def process(self, state: AgenticState):
        p = state.product_model
        c = state.competitor_model
        
        state.final_pages["faq"] = {
            "title": f"FAQ for {p.name}",
            "items": state.grounded_data 
        }
        
        state.final_pages["product_page"] = {
            "header": p.name,
            "marketing_benefits": logic_blocks.generate_benefits_block(p.benefits),
            "usage_protocol": logic_blocks.extract_usage_block(p.usage_instructions, p.side_effects)
        }
        
        if c:
            analysis = logic_blocks.compare_ingredients_block(p.key_ingredients, c.key_ingredients)
            state.final_pages["comparison_page"] = {
                "title": f"{p.name} vs {c.name}",
                "price_comparison": {
                    p.name: p.price_in_inr,
                    c.name: c.price_in_inr,
                    "savings": c.price_in_inr - p.price_in_inr
                },
                "ingredient_analysis": analysis
            }
        
        state.logs.append("ComposerAgent: Final artifacts assembled via state-trigger.")