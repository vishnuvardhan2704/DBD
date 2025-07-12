
# ESG Recommendation System - Working Prototype
# File: esg_recommender_prototype.py

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import json
from scipy.sparse import issparse

class ESGRecommendationSystem:
    def __init__(self):
        self.products = []
        self.embeddings = None
        self.rules = {}
        self.setup_sample_data()

    def setup_sample_data(self):
        """Create sample product data for demonstration"""
        self.products = [
            {"id": 1, "name": "Regular Chicken Breast", "category": "meat", "packaging": "plastic", "organic": False, "carbon_kg": 3.2, "price": 8.99},
            {"id": 2, "name": "Organic Free-Range Chicken", "category": "meat", "packaging": "paper", "organic": True, "carbon_kg": 2.1, "price": 12.99},
            {"id": 3, "name": "Regular Ground Beef", "category": "meat", "packaging": "plastic", "organic": False, "carbon_kg": 4.8, "price": 10.99},
            {"id": 4, "name": "Organic Grass-Fed Beef", "category": "meat", "packaging": "paper", "organic": True, "carbon_kg": 3.2, "price": 16.99},
            {"id": 5, "name": "Regular Milk", "category": "dairy", "packaging": "plastic", "organic": False, "carbon_kg": 1.9, "price": 3.99},
            {"id": 6, "name": "Organic Oat Milk", "category": "dairy", "packaging": "glass", "organic": True, "carbon_kg": 0.8, "price": 4.99},
            {"id": 7, "name": "Regular Yogurt", "category": "dairy", "packaging": "plastic", "organic": False, "carbon_kg": 1.2, "price": 2.99},
            {"id": 8, "name": "Organic Greek Yogurt", "category": "dairy", "packaging": "glass", "organic": True, "carbon_kg": 0.9, "price": 5.99},
            {"id": 9, "name": "White Rice", "category": "grains", "packaging": "plastic", "organic": False, "carbon_kg": 2.1, "price": 2.49},
            {"id": 10, "name": "Organic Brown Rice", "category": "grains", "packaging": "paper", "organic": True, "carbon_kg": 1.8, "price": 3.99},
        ]

        # Sustainability rules
        self.rules = {
            "organic_bonus": 2,
            "glass_packaging_bonus": 1,
            "paper_packaging_bonus": 1,
            "plastic_penalty": -1,
            "carbon_threshold": 2.0  # kg CO2e
        }

        # Generate embeddings
        self.generate_embeddings()

    def generate_embeddings(self):
        """Generate TF-IDF embeddings for products (simple version)"""
        descriptions = [f"{p['name']} {p['category']}" for p in self.products]
        vectorizer = TfidfVectorizer(stop_words='english')
        X = vectorizer.fit_transform(descriptions)
        self.embeddings = X.toarray()  # type: ignore[attr-defined]

    def find_similar_products(self, product_id, top_k=3):
        """Find similar products using cosine similarity"""
        if product_id >= len(self.products):
            return []

        similarities = cosine_similarity(self.embeddings)
        similar_indices = similarities[product_id].argsort()[-top_k-1:-1][::-1]
        # Remove the product itself
        similar_indices = similar_indices[similar_indices != product_id]
        return similar_indices[:top_k]

    def calculate_sustainability_score(self, product):
        """Calculate sustainability score based on rules"""
        score = 0

        # Organic bonus
        if product.get('organic'):
            score += self.rules['organic_bonus']

        # Packaging score
        packaging = product.get('packaging', '').lower()
        if packaging == 'glass':
            score += self.rules['glass_packaging_bonus']
        elif packaging == 'paper':
            score += self.rules['paper_packaging_bonus']
        elif packaging == 'plastic':
            score += self.rules['plastic_penalty']

        # Carbon footprint bonus (lower is better)
        carbon = product.get('carbon_kg', 0)
        if carbon < self.rules['carbon_threshold']:
            score += 1

        return score

    def recommend_sustainable_alternative(self, product_id):
        """Main recommendation function"""
        if product_id >= len(self.products):
            return {"error": "Product not found"}

        original_product = self.products[product_id]
        similar_products = self.find_similar_products(product_id)

        # Score all similar products
        recommendations = []
        for similar_id in similar_products:
            similar_product = self.products[similar_id]
            sustainability_score = self.calculate_sustainability_score(similar_product)
            original_score = self.calculate_sustainability_score(original_product)

            # Only recommend if it's more sustainable
            if sustainability_score > original_score:
                carbon_saved = original_product['carbon_kg'] - similar_product['carbon_kg']
                recommendations.append({
                    'product': similar_product,
                    'sustainability_score': sustainability_score,
                    'carbon_saved_kg': round(carbon_saved, 2),
                    'carbon_points_awarded': max(0, int(carbon_saved * 10))
                })

        # Sort by sustainability score
        recommendations.sort(key=lambda x: x['sustainability_score'], reverse=True)

        if recommendations:
            best_recommendation = recommendations[0]
            return {
                'original_item': original_product['name'],
                'suggested_item': best_recommendation['product']['name'],
                'sustainability_score': best_recommendation['sustainability_score'],
                'carbon_saved_kg': best_recommendation['carbon_saved_kg'],
                'carbon_points_awarded': best_recommendation['carbon_points_awarded'],
                'reason': self.generate_reason(original_product, best_recommendation['product'])
            }
        else:
            return {
                'original_item': original_product['name'],
                'message': 'No more sustainable alternatives found in similar products'
            }

    def generate_reason(self, original, recommended):
        """Generate explanation for recommendation"""
        reasons = []

        if recommended.get('organic') and not original.get('organic'):
            reasons.append("organic farming practices")

        if recommended.get('packaging') == 'glass' and original.get('packaging') != 'glass':
            reasons.append("recyclable glass packaging")
        elif recommended.get('packaging') == 'paper' and original.get('packaging') == 'plastic':
            reasons.append("biodegradable paper packaging")

        if recommended.get('carbon_kg', 0) < original.get('carbon_kg', 0):
            reasons.append("lower carbon footprint")

        if reasons:
            return f"Recommended due to: {', '.join(reasons)}"
        else:
            return "Similar product with better sustainability profile"

# Demo the system
if __name__ == "__main__":
    print("🌱 ESG Recommendation System - Demo")
    print("="*50)

    # Initialize system
    recommender = ESGRecommendationSystem()

    # Show all products
    print("\n📦 Available Products:")
    for i, product in enumerate(recommender.products):
        print(f"{i}: {product['name']} - {product['carbon_kg']} kg CO2e - ${product['price']}")

    # Test recommendations
    test_products = [0, 2, 4, 6]  # Regular chicken, beef, milk, yogurt

    for product_id in test_products:
        print(f"\n🔍 Recommendation for: {recommender.products[product_id]['name']}")
        result = recommender.recommend_sustainable_alternative(product_id)

        if 'suggested_item' in result:
            print(f"  ✅ Suggested: {result['suggested_item']}")
            print(f"  🌱 Carbon saved: {result['carbon_saved_kg']} kg CO2e")
            print(f"  🏆 Points awarded: {result['carbon_points_awarded']}")
            print(f"  💡 Reason: {result['reason']}")
        else:
            print(f"  ❌ {result.get('message', 'No recommendation available')}")

    print("\n🎯 System Features Demonstrated:")
    print("  • Product similarity matching")
    print("  • Rule-based sustainability scoring")
    print("  • Carbon footprint calculations")
    print("  • Recommendation reasoning")
    print("  • Points system for user engagement")
