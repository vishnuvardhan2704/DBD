from db import get_all_products, get_product_by_id
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class ESGScorer:
    """Enhanced ESG scoring system"""
    
    # Scoring weights
    WEIGHTS = {
        'organic': 3.0,
        'packaging': 2.0,
        'carbon': 2.5,
        'price_efficiency': 1.0
    }
    
    # Packaging scores
    PACKAGING_SCORES = {
        'glass': 2,
        'paper': 1.5,
        'cardboard': 1.5,
        'aluminum': 1,
        'plastic': -1,
        'styrofoam': -2
    }
    
    @classmethod
    def calculate_sustainability_score(cls, product: Dict[str, Any]) -> float:
        """Calculate comprehensive sustainability score"""
        score = 0.0
        
        # Organic bonus
        if product.get('is_organic'):
            score += cls.WEIGHTS['organic']
        
        # Packaging score
        packaging = (product.get('packaging', '')).lower()
        packaging_score = cls.PACKAGING_SCORES.get(packaging, 0)
        score += packaging_score * cls.WEIGHTS['packaging']
        
        # Carbon footprint score (lower is better)
        carbon_kg = product.get('carbon_kg', 0)
        if carbon_kg < 1.0:
            score += cls.WEIGHTS['carbon'] * 2
        elif carbon_kg < 2.0:
            score += cls.WEIGHTS['carbon']
        elif carbon_kg > 4.0:
            score -= cls.WEIGHTS['carbon']
        
        # Price efficiency (sustainability per dollar)
        price = product.get('price', 1)
        if price > 0:
            efficiency = score / price
            score += efficiency * cls.WEIGHTS['price_efficiency']
        
        return round(score, 2)
    
    @classmethod
    def get_sustainability_grade(cls, score: float) -> str:
        """Convert score to letter grade"""
        if score >= 8: return 'A+'
        elif score >= 6: return 'A'
        elif score >= 4: return 'B+'
        elif score >= 2: return 'B'
        elif score >= 0: return 'C'
        else: return 'D'

def find_greener_alternative(product: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Find the best sustainable alternative with enhanced scoring"""
    try:
        all_products = get_all_products()
        original_score = ESGScorer.calculate_sustainability_score(product)
        
        # Filter candidates: same category, different product, higher score
        candidates = []
        for p in all_products:
            if (p['category'] == product['category'] and 
                p['id'] != product['id']):
                
                candidate_score = ESGScorer.calculate_sustainability_score(p)
                if candidate_score > original_score:
                    candidates.append((candidate_score, p))
        
        if not candidates:
            logger.info(f"No greener alternative found for product {product['id']}")
            return None
        
        # Sort by score and return the best
        candidates.sort(reverse=True, key=lambda x: x[0])
        best_alternative = candidates[0][1]
        
        logger.info(f"Found greener alternative: {best_alternative['name']} "
                   f"(score: {candidates[0][0]} vs {original_score})")
        
        return best_alternative
        
    except Exception as e:
        logger.error(f"Error finding alternative for product {product.get('id')}: {e}")
        return None

def estimate_carbon_savings(original: Dict[str, Any], alternative: Dict[str, Any]) -> float:
    """Calculate carbon savings with validation"""
    try:
        original_carbon = float(original.get('carbon_kg', 0))
        alternative_carbon = float(alternative.get('carbon_kg', 0))
        
        savings = max(0.0, original_carbon - alternative_carbon)
        return round(savings, 2)
        
    except (ValueError, TypeError) as e:
        logger.error(f"Error calculating carbon savings: {e}")
        return 0.0

def get_product_insights(product: Dict[str, Any]) -> Dict[str, Any]:
    """Get detailed sustainability insights for a product"""
    score = ESGScorer.calculate_sustainability_score(product)
    grade = ESGScorer.get_sustainability_grade(score)
    
    insights = {
        'sustainability_score': score,
        'sustainability_grade': grade,
        'carbon_kg': product.get('carbon_kg', 0),
        'is_organic': product.get('is_organic', False),
        'packaging': product.get('packaging', 'unknown'),
        'recommendations': []
    }
    
    # Add improvement recommendations
    if not product.get('is_organic'):
        insights['recommendations'].append("Consider organic version for better sustainability")
    
    if product.get('packaging', '').lower() == 'plastic':
        insights['recommendations'].append("Look for alternatives with glass or paper packaging")
    
    if product.get('carbon_kg', 0) > 3.0:
        insights['recommendations'].append("High carbon footprint - consider lower-impact alternatives")
    
    return insights