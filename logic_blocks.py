"""
REUSABLE LOGIC BLOCKS
Pure functions designed for deterministic content transformation. 
These are called by the Composer Agent to populate templates.
"""

def generate_benefits_block(benefits: list) -> str:
    """Formats raw benefit strings into high-conversion marketing bullets."""
    if not benefits:
        return "No benefits data available."
    return "\n".join([f"✨ {item.strip()}" for item in benefits])

def extract_usage_block(instructions: str, side_effects: str) -> str:
    """Composes a safe usage protocol by merging application steps and warnings."""
    protocol = f"APPLICATION: {instructions}\n"
    if side_effects:
        protocol += f"SAFETY WARNING: {side_effects}"
    return protocol

def compare_ingredients_block(primary_ingredients: list, competitor_ingredients: list) -> dict:
    """Performs set analysis to find unique and shared active ingredients."""
    primary_set = set([i.lower() for i in primary_ingredients])
    comp_set = set([i.lower() for i in competitor_ingredients])
    
    return {
        "shared": list(primary_set.intersection(comp_set)),
        "unique_to_product": list(primary_set - comp_set),
        "missing_actives": list(comp_set - primary_set)
    }