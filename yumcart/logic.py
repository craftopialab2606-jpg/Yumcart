# ---------------- DELETE PRODUCT ----------------
def delete_product(product_id):
    return isinstance(product_id, int) and product_id > 0


# ---------------- EXTRACT CATEGORIES ----------------
def extract_categories(products):
    cats = {p.get("category") for p in products if p.get("category")}
    return sorted(list(cats))


# ---------------- VALIDATE PRODUCT ----------------
def validate_product(name, price, category):
    if not name or not category:
        return False
    try:
        price_val = float(price)
        return price_val > 0
    except:
        return False


# ---------------- CHECKOUT ----------------
def checkout(cart):
    if not cart:
        return 0
    total = 0
    for item in cart:
        if isinstance(item, (list, tuple)):
            total += item[2]  # price at index 2
        else:
            total += item.get("price", 0)
    return total


# ---------------- ADD ITEM ----------------
def add_item(cart, product):
    if not isinstance(product, dict):
        raise ValueError("Product must be a dict")
    if "id" not in product or "price" not in product:
        raise ValueError("Product must have 'id' and 'price'")
    cart.append(product)
    return cart


# ---------------- REMOVE ITEM ----------------
def remove_item(cart, item_id):
    return [i for i in cart if i.get("id") != item_id]


# ---------------- CATEGORY LIST ----------------
def get_categories():
    return ["Fast Food", "Dessert", "Drinks", "Bakery", "Others"]
