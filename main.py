# shopping_assistant.py
import json
from typing import Dict, List

# ------------------------- Mock Tool Implementations -------------------------
def search_products(name: str = None, color: str = None, min_price: float = 0, max_price: float = 1000, size: str = None) -> List[Dict]:
    """Mock e-commerce search aggregator."""
    mock_products = [
        {"name": "Red Summer Dress", "price": 45.99, "color": "red", "size": "M", "store": "FashionHub"},
        {"name": "Blue Jeans", "price": 59.99, "color": "blue", "size": "L", "store": "ShopStyle"},
        {"name": "Black Sneakers", "price": 79.99, "color": "black", "size": "10", "store": "ShoePalace"},
    ]
    filtered = [
        p for p in mock_products
        if (name.lower() in p["name"].lower() if name else True)
        and (color == p["color"] if color else True)
        and (min_price <= p["price"] <= max_price)
        and (size == p["size"] if size else True)
    ]
    return filtered

def estimate_shipping(user_location: str, delivery_date: str) -> Dict:
    """Mock shipping estimator."""
    shipping_cost = 5.0 if "New York" in user_location else 15.0
    estimated_days = 3 if "New York" in user_location else 7
    return {
        "feasible": True,
        "cost": shipping_cost,
        "delivery_date": f"{estimated_days} business days after order",
    }

def apply_promo_code(base_price: float, promo_code: str) -> float:
    """Mock discount/promo code applier."""
    promo_db = {"SUMMER20": 0.2, "FREESHIP": 0.0}
    discount = promo_db.get(promo_code, 0)
    return base_price * (1 - discount)

def compare_prices(product_name: str) -> List[Dict]:
    """Mock competitor price comparison."""
    mock_comparisons = {
        "Red Summer Dress": [
            {"store": "FashionHub", "price": 45.99},
            {"store": "StyleMart", "price": 42.50},
            {"store": "TrendyStore", "price": 49.99},
        ],
        "Blue Jeans": [
            {"store": "ShopStyle", "price": 59.99},
            {"store": "DenimWorld", "price": 54.99},
        ],
    }
    return mock_comparisons.get(product_name, [])

def check_return_policy(store_name: str) -> str:
    """Mock return policy checker."""
    policies = {
        "FashionHub": "30-day returns",
        "ShopStyle": "14-day returns",
        "StyleMart": "7-day returns",
        "TrendyStore": "Exchange only",
        "DenimWorld": "Store credit only",
    }
    return policies.get(store_name, "No policy found")

# ------------------------- Shopping Assistant Agent -------------------------
class ShoppingAssistant:
    def __init__(self):
        self.tools = {
            "search": search_products,
            "shipping": estimate_shipping,
            "discount": apply_promo_code,
            "compare": compare_prices,
            "returns": check_return_policy,
        }

    def parse_query(self, query: str) -> Dict:
        """Extract key criteria from user query (simplified NLP)."""
        parsed = {"promo_code": None, "location": "New York"}  # default location
        if "under $" in query:
            parsed["max_price"] = float(query.split("under $")[1].split()[0])
        if "promo code" in query:
            parsed["promo_code"] = query.split("promo code ")[1].split()[0]
        if "shipping to " in query:
            parsed["location"] = query.split("shipping to ")[1].split()[0]
        
        # Detect product type and color (basic keyword matching)
        colors = ["red", "blue", "black"]
        for color in colors:
            if color in query.lower():
                parsed["color"] = color
                break
        if "dress" in query.lower():
            parsed["product"] = "dress"
        elif "jeans" in query.lower():
            parsed["product"] = "jeans"
        elif "sneakers" in query.lower():
            parsed["product"] = "sneakers"
        return parsed

    def execute_plan(self, parsed_query: Dict) -> Dict:
        """Orchestrate tool usage based on parsed query."""
        # Step 1: Search for products
        products = self.tools["search"](
            name=parsed_query.get("product"),
            color=parsed_query.get("color"),
            max_price=parsed_query.get("max_price", 1000)
        )
        
        # Step 2: Compare prices across competitors
        all_options = []
        for p in products:
            all_options.append(p)  # Original product
            competitors = self.tools["compare"](p["name"])
            all_options.extend([
                {**p, "store": c["store"], "price": c["price"]} 
                for c in competitors
            ])
        
        # Step 3: Apply discounts and gather results
        results = []
        for item in all_options:
            final_price = self.tools["discount"](
                item["price"], parsed_query.get("promo_code")
            )
            shipping = self.tools["shipping"](
                parsed_query["location"], "2024-03-30"  # Mock delivery date
            )
            return_policy = self.tools["returns"](item["store"])
            
            results.append({
                "name": item["name"],
                "store": item["store"],
                "final_price": round(final_price, 2),
                "shipping_cost": shipping["cost"],
                "return_policy": return_policy,
            })
        
        return results

    def generate_response(self, results: List[Dict]) -> str:
        """Convert structured results into natural language."""
        if not results:
            return "Sorry, no products found matching your criteria."
        
        response = "Here are your best options:\n"
        for idx, item in enumerate(results, 1):
            response += (
                f"\n{idx}. {item['name']} from {item['store']}\n"
                f"   Price: ${item['final_price']} "
                f"(Shipping: ${item['shipping_cost']})\n"
                f"   Return Policy: {item['return_policy']}\n"
            )
        return response

# ------------------------- Example Usage -------------------------
if __name__ == "__main__":
    agent = ShoppingAssistant()
    
    # Example query
    user_query = "Find me a red dress under $50 with promo code SUMMER20. Shipping to New York."
    
    # Agent workflow
    parsed = agent.parse_query(user_query)
    results = agent.execute_plan(parsed)
    response = agent.generate_response(results)
    
    print("User Query:", user_query)
    print("\nAgent Response:\n", response)