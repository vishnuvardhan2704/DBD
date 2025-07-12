from db import get_all_products, get_product_by_id
from typing import Dict, Any, Optional

def calculate_sustainability_score(product: Dict[str, Any]) -> int:
    """Score product based on ESG rules."""
    score = 0
    if product['is_organic']:
        score += 2
    packaging = (product['packaging'] or '').lower()
    if packaging == 'glass':
        score += 1
    elif packaging == 'paper':
        score += 1
    elif packaging == 'plastic':
        score -= 1
    if product['carbon_kg'] < 2.0:
        score += 1
    return score

def find_greener_alternative(product: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Find a more sustainable alternative to the given product."""
    all_products = get_all_products()
    original_score = calculate_sustainability_score(product)
    # Only consider same category, not the same product
    candidates = [p for p in all_products if p['category'] == product['category'] and p['id'] != product['id']]
    # Score and filter
    better = []
    for p in candidates:
        score = calculate_sustainability_score(p)
        if score > original_score:
            better.append((score, p))
    if not better:
        return None
    # Pick the best
    better.sort(reverse=True, key=lambda x: x[0])
    return better[0][1]

def estimate_carbon_savings(original: Dict[str, Any], alternative: Dict[str, Any]) -> float:
    """Estimate carbon savings in kg CO2e."""
    return max(0.0, round(original['carbon_kg'] - alternative['carbon_kg'], 2)) 