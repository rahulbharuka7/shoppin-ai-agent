from typing import List, Dict, Any
import json
from tools import (
    search_products,
    estimate_shipping,
    check_discount,
    compare_prices,
    get_return_policy,
    Product
)

class ShoppingAgent:
    def __init__(self):
        self.context = {}
    
    def _parse_query(self, query: str) -> Dict[str, Any]:
        """Parse user query to extract relevant information"""
        query = query.lower()
        parsed = {}
        
        # Extract price constraints
        if "under $" in query:
            import re
            price_match = re.search(r'under \$(\d+)', query)
            if price_match:
                parsed['max_price'] = float(price_match.group(1))
        
        # Extract size
        if "size" in query:
            import re
            size_match = re.search(r'size (\w+)', query)
            if size_match:
                parsed['size'] = size_match.group(1)
        
        # Extract color
        colors = ['white', 'black', 'blue', 'red', 'green', 'yellow', 'purple', 'pink']
        for color in colors:
            if color in query:
                parsed['color'] = color
                break
        
        # Extract product type
        product_types = ['skirt', 'sneakers', 'jacket', 'dress']
        for product in product_types:
            if product in query:
                parsed['name'] = product
                break
        
        # Extract discount code
        if "code" in query:
            import re
            code_match = re.search(r"code '(\w+)'", query)
            if code_match:
                parsed['discount_code'] = code_match.group(1)
        
        return parsed
    
    def process_query(self, query: str) -> str:
        """Process user query and return appropriate response"""
        parsed_query = self._parse_query(query)
        response_parts = []
        
        # Search for products
        if any(key in parsed_query for key in ['name', 'max_price', 'color', 'size']):
            products = search_products(parsed_query)
            if products:
                response_parts.append(f"Found {len(products)} matching products:")
                for product in products:
                    response_parts.append(
                        f"- {product.name} ({product.color}, size {product.size}) "
                        f"at ${product.price:.2f} from {product.store}"
                    )
                    
                    # Check discount if code provided
                    if 'discount_code' in parsed_query:
                        discount = check_discount(product, parsed_query['discount_code'])
                        if discount.valid:
                            response_parts.append(
                                f"  Applied code '{discount.code}' for {discount.discount_percentage}% off. "
                                f"Final price: ${discount.final_price:.2f}"
                            )
                        else:
                            response_parts.append(f"  Discount code '{discount.code}' is invalid.")
                    
                    # Check shipping
                    shipping = estimate_shipping(product)
                    response_parts.append(
                        f"  Shipping: ${shipping.cost:.2f}, "
                        f"Estimated delivery: {shipping.estimated_delivery_date}"
                    )
                    
                    # Compare prices if mentioned
                    if "better deals" in query.lower() or "price comparison" in query.lower():
                        comparisons = compare_prices(product)
                        response_parts.append("  Price comparisons:")
                        for comp in comparisons:
                            status = "In stock" if comp.in_stock else "Out of stock"
                            response_parts.append(
                                f"    {comp.store}: ${comp.price:.2f} ({status})"
                            )
            else:
                response_parts.append("Sorry, no products found matching your criteria.")
        
        # Check return policy
        if "return" in query.lower():
            store = None
            for s in ['SiteA', 'SiteB', 'FashionHub', 'SneakerWorld']:
                if s.lower() in query.lower():
                    store = s
                    break
            
            if store:
                policy = get_return_policy(store)
                response_parts.append(f"\nReturn Policy for {store}:")
                response_parts.append(f"- {policy.days_to_return} days to return")
                response_parts.append(f"- {'Free returns' if policy.free_returns else 'Paid returns'}")
                response_parts.append("- Conditions:")
                for condition in policy.conditions:
                    response_parts.append(f"  * {condition}")
        
        return "\n".join(response_parts)

def main():
    agent = ShoppingAgent()
    
    print("Welcome to the AI Shopping Assistant! (Type 'exit' to quit)")
    print("\nExample queries:")
    print("1. Find a floral skirt under $40 in size S. Is it in stock, and can I apply a discount code 'SAVE10'?")
    print("2. I need white sneakers (size 8) for under $70 that can arrive by Friday.")
    print("3. I found a 'casual denim jacket' at $80 on SiteA. Any better deals?")
    print("4. I want to buy a cocktail dress from SiteB, but only if returns are hassle-free. Do they accept returns?")
    
    while True:
        print("\nWhat would you like to know? ")
        query = input("> ")
        
        if query.lower() == 'exit':
            print("Thank you for shopping with us!")
            break
        
        response = agent.process_query(query)
        print("\n" + response)

if __name__ == "__main__":
    main()