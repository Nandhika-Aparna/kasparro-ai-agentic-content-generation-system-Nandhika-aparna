from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class Product(BaseModel):
    name: str
    concentration: str
    skin_types: List[str]
    key_ingredients: List[str]
    benefits: List[str]
    usage_instructions: str
    side_effects: Optional[str]
    price_in_inr: int

class Question(BaseModel):
    category: str
    question_text: str

class QuestionList(BaseModel):
    """Container for batch question generation by the Inquisitor Agent."""
    questions: List[Question]

class AgenticState(BaseModel):
    """
    The Shared State (Environment) for the Multi-Agent System.
    Aligned with Kasparro requirements for 3-page autonomous generation.
    """
    raw_input: Dict[str, Any]
    product_model: Optional[Product] = None
    competitor_model: Optional[Product] = None  # Required for Comparison Page
    
    # Agent Communication Channels
    questions: List[Question] = []
    grounded_data: List[Dict] = []
    
    # Final Output Storage (Must result in faq.json, product_page.json, comparison_page.json)
    final_pages: Dict[str, Any] = {
        "faq": {},
        "product_page": {},
        "comparison_page": {}
    }
    
    logs: List[str] = []

class SystemState(BaseModel):
    """Legacy state for backward compatibility with initialization scripts."""
    primary_product: Product
    competitor_product: Optional[Product] = None