import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "database", "yumcart.db")


class CustomerPanel:

    def __init__(self, master):
        self.master = master
        self.cart = []  # (id, name, price, category)

        # DB connection
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

        # ---------- CATEGORY DROPDOWN ----------
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(master, textvariable=self.category_var)
        self.category_combo.pack(pady=5)

        self.load_categories()
        self.category_combo.bind("<<ComboboxSelected>>", self.filter_by_category)

        # ---------- PRODUCTS TABLE (ID HIDDEN) ----------
        self.tree = ttk.Treeview(
            master,
            columns=("Name", "Price", "Category"),
            show="headings"
        )
        for col in ("Name", "Price", "Category"):
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10)

        # ---------- LOAD PRODUCTS ----------
        self.load_products()

    # ----------------- CATEGORIES -----------------
    def load_categories(self):
        self.cursor.execute("SELECT DISTINCT category FROM products")
        categories = [row[0] for row in self.cursor.fetchall()]
        self.category_combo["values"] = ["All"] + categories
        self.category_combo.current(0)

    # ----------------- PRODUCTS -----------------
    def load_products(self):
        self.filter_by_category()

    def filter_by_category(self, event=None):
        selected_category = self.category_var.get()

        for row in self.tree.get_children():
            self.tree.delete(row)

        if selected_category == "All":
            self.cursor.execute("SELECT id, name, price, category FROM products")
        else:
            self.cursor.execute(
                "SELECT id, name, price, category FROM products WHERE category = ?",
                (selected_category,)
            )

        for item in self.cursor.fetchall():
            pid, name, price, category = item

        
            self.tree.insert(
                "",
                tk.END,
                values=(name, price, category),
                tags=(pid,)
            )

    # ----------------- CART -----------------
    def add_selected_to_cart(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Select a product first!")
            return

        item = self.tree.item(selected)

        pid = item["tags"][0]          # hidden ID
        name = item["values"][0]       # Name
        price = item["values"][1]      # Price
        category = item["values"][2]   # Category

        self.cart.append((int(pid), name, float(price), category))
        messagebox.showinfo("Success", f"{name} added to cart!")

    def open_cart(self):
        if not self.cart:
            messagebox.showinfo("Cart", "Cart is empty!")
            return

        items = "\n".join(
            [f"{name} ({cat}) - Rs {price:.2f}"
             for (_, name, price, cat) in self.cart]
        )
        messagebox.showinfo("Your Cart", items)

    # ----------------- CHECKOUT -----------------
    def checkout(self):
        if not self.cart:
            messagebox.showinfo("Cart Empty", "Your cart is empty!")
            return

        total = sum(item[2] for item in self.cart)

        for item in self.cart:
            self.cursor.execute(
                "INSERT INTO orders (product_name, quantity, total_price) VALUES (?, ?, ?)",
                (item[1], 1, item[2])
            )

        self.conn.commit()
        self.cart.clear()
        messagebox.showinfo("Success", f"Order placed! Total: Rs {total:.2f}")

    # ----------------- ORDER HISTORY -----------------
    def view_orders(self):
        self.cursor.execute(
            "SELECT product_name, quantity, total_price, order_date FROM orders"
        )
        orders = self.cursor.fetchall()

        # if not orders:
        #     messagebox.showinfo("Orders", "No orders yet!")
        #     return

        items = "\n".join(
            [f"{name} x{qty} - Rs {price:.2f} ({date})"
             for name, qty, price, date in orders]
        )
        messagebox.showinfo("Order History", items)
