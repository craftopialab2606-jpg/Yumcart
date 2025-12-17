import unittest
from logic import (
    delete_product, extract_categories, validate_product,
    checkout, add_item, remove_item, get_categories
)


# ---------------- DELETE PRODUCT TESTS ----------------
class TestDelete(unittest.TestCase):
    def test_valid_id(self):
        self.assertTrue(delete_product(5))

    def test_invalid(self):
        self.assertFalse(delete_product(0))
        self.assertFalse(delete_product(None))
        self.assertFalse(delete_product("abc"))


# ---------------- CATEGORY EXTRACTION ----------------
class TestCategories(unittest.TestCase):
    def test_extract(self):
        data = [
            {"category": "Cake"},
            {"category": "Brownie"},
            {"category": "Cake"},
            {"name": "NoCat"}
        ]
        self.assertEqual(extract_categories(data), ["Brownie", "Cake"])

    def test_empty(self):
        self.assertEqual(extract_categories([]), [])


# ---------------- PRODUCT VALIDATION ----------------
class TestValidation(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(validate_product("Cake", 200, "Dessert"))

    def test_invalid(self):
        self.assertFalse(validate_product("", 200, "Dessert"))
        self.assertFalse(validate_product("Cake", 0, "Dessert"))
        self.assertFalse(validate_product("Cake", -10, "Dessert"))
        self.assertFalse(validate_product("Cake", "abc", "Dessert"))
        self.assertFalse(validate_product("Cake", 200, ""))


# ---------------- CHECKOUT ----------------
class TestCheckout(unittest.TestCase):
    def test_single(self):
        cart = [(1, "Cake", 200, "Dessert")]
        self.assertEqual(checkout(cart), 200)

    def test_mixed(self):
        cart = [
            (1, "Cake", 200, "Dessert"),
            {"id": 2, "price": 300}
        ]
        self.assertEqual(checkout(cart), 500)

    def test_empty(self):
        self.assertEqual(checkout([]), 0)


# ---------------- CART OPERATIONS ----------------
class TestCart(unittest.TestCase):
    def test_add_valid(self):
        cart = []
        add_item(cart, {"id": 1, "price": 200})
        self.assertEqual(len(cart), 1)

    def test_add_invalid(self):
        cart = []
        with self.assertRaises(ValueError):
            add_item(cart, ["wrong"])

        with self.assertRaises(ValueError):
            add_item(cart, {"name": "Cake"})

    def test_remove_existing(self):
        cart = [{"id": 1}, {"id": 2}]
        updated = remove_item(cart, 1)
        self.assertEqual(len(updated), 1)
        self.assertEqual(updated[0]["id"], 2)

    def test_remove_non_existing(self):
        cart = [{"id": 1}]
        updated = remove_item(cart, 99)
        self.assertEqual(len(updated), 1)


# ---------------- CATEGORY LIST ----------------
class TestStaticCategories(unittest.TestCase):
    def test_category_list(self):
        cats = get_categories()
        self.assertEqual(len(cats), 5)
        self.assertIn("Dessert", cats)


if __name__ == '__main__':
    unittest.main()
