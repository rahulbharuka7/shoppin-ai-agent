from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass
import json

@dataclass
class Product:
    id: str
    name: str
    price: float
    color: str
    size: str
    store: str
    in_stock: bool

@dataclass
class ShippingEstimate:
    available: bool
    cost: float
    estimated_days: int
    estimated_delivery_date: str

@dataclass
class DiscountResult:
    code: str
    valid: bool
    discount_percentage: float
    final_price: float

@dataclass
class PriceComparison:
    store: str
    price: float
    in_stock: bool
    link: str

@dataclass
class ReturnPolicy:
    store: str
    days_to_return: int
    free_returns: bool
    conditions: List[str]

# Mock database
MOCK_PRODUCTS = [
    Product("1", "Floral Summer Skirt", 35.99, "Blue", "S", "FashionHub", True),
    Product("2", "White Sneakers", 65.99, "White", "8", "SneakerWorld", True),
    Product("3", "Casual Denim Jacket", 79.99, "Blue", "M", "SiteA", True),
    Product("4", "Cocktail Dress", 89.99, "Black", "M", "SiteB", True),
]

MOCK_STORES = {
    "FashionHub": {"shipping_base": 5.99, "free_shipping_threshold": 50},
    "SneakerWorld": {"shipping_base": 7.99, "free_shipping_threshold": 75},
    "SiteA": {"shipping_base": 4.99, "free_shipping_threshold": 60},
    "SiteB": {"shipping_base": 6.99, "free_shipping_threshold": 80},
}

MOCK_RETURN_POLICIES = {
    "FashionHub": ReturnPolicy("FashionHub", 30, True, ["Items must be unworn", "Original tags attached"]),
    "SneakerWorld": ReturnPolicy("SneakerWorld", 45, True, ["Unworn condition", "Original box required"]),
    "SiteA": ReturnPolicy("SiteA", 14, False, ["Store credit only", "Within 14 days"]),
    "SiteB": ReturnPolicy("SiteB", 30, True, ["Free returns within 30 days", "Original condition"]),
}

def search_products(query: Dict) -> List[Product]:
    """Search for products based on criteria"""
    results = []
    
    for product in MOCK_PRODUCTS:
        matches = True
        if 'name' in query and query['name'].lower() not in product.name.lower():
            matches = False
        if 'max_price' in query and product.price > query['max_price']:
            matches = False
        if 'color' in query and query['color'].lower() != product.color.lower():
            matches = False
        if 'size' in query and query['size'].lower() != product.size.lower():
            matches = False
            
        if matches:
            results.append(product)
            
    return results

def estimate_shipping(product: Product, delivery_date: Optional[str] = None) -> ShippingEstimate:
    """Estimate shipping cost and delivery time"""
    store_info = MOCK_STORES[product.store]
    
    # Calculate shipping cost
    shipping_cost = 0 if product.price >= store_info["free_shipping_threshold"] else store_info["shipping_base"]
    
    # Calculate delivery estimate
    estimated_days = 3 if shipping_cost == 0 else 5
    delivery_date = (datetime.now() + timedelta(days=estimated_days)).strftime("%Y-%m-%d")
    
    return ShippingEstimate(True, shipping_cost, estimated_days, delivery_date)

def check_discount(product: Product, code: str) -> DiscountResult:
    """Check and apply discount code"""
    valid_codes = {
        "SAVE10": 10,
        "SUMMER20": 20,
        "WELCOME15": 15
    }
    
    if code in valid_codes:
        discount = valid_codes[code]
        final_price = product.price * (1 - discount/100)
        return DiscountResult(code, True, discount, final_price)
    
    return DiscountResult(code, False, 0, product.price)

def compare_prices(product: Product) -> List[PriceComparison]:
    """Compare prices across different stores"""
    comparisons = []
    base_price = product.price
    
    for store in MOCK_STORES.keys():
        if store != product.store:
            # Simulate different prices across stores
            price_diff = (hash(store + product.name) % 30) - 15
            price = base_price + price_diff
            in_stock = bool(hash(store + product.name) % 2)
            link = f"https://{store.lower()}.com/products/{product.name.lower().replace(' ', '-')}"
            
            comparisons.append(PriceComparison(store, price, in_stock, link))
    
    return comparisons

def get_return_policy(store: str) -> ReturnPolicy:
    """Get return policy for a store"""
    return MOCK_RETURN_POLICIES.get(store)