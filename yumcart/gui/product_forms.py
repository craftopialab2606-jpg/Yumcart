import tkinter as tk
from tkinter import ttk, messagebox
from database.database import get_db

BG = "#FFF7E6"
BTN = "#FFB6C1"
HEADING = "#D35400"

# ------------------ ADD PRODUCT ------------------
def add_product_form():
    win = tk.Toplevel()
    win.title("Add Dessert")
    win.geometry("400x500")
    win.config(bg=BG)

    tk.Label(win, text="Add Dessert", font=("Arial", 24, "bold"),
             bg=BG, fg=HEADING).pack(pady=10)

    tk.Label(win, text="Name:", bg=BG).pack()
    name_entry = tk.Entry(win)
    name_entry.pack()

    tk.Label(win, text="Price:", bg=BG).pack()
    price_entry = tk.Entry(win)
    price_entry.pack()

    tk.Label(win, text="Category:", bg=BG).pack(pady=(10,0))
    categories = ["Cake", "Cookies", "Sundae", "Brownie", "Coffee"]
    category_var = tk.StringVar()
    category_dropdown = ttk.Combobox(win, textvariable=category_var, values=categories, state="readonly")
    category_dropdown.pack()
    category_dropdown.current(1)  # Default "Cookies" (index 1)

   
    def save():
        name = name_entry.get().strip()
        price = price_entry.get().strip()
        category = category_var.get()

        if not name or not price:
            messagebox.showwarning("Error", "Please enter name and price!")
            return

        try:
            price_val = float(price)
        except:
            messagebox.showwarning("Error", "Price must be a number!")
            return

        conn = get_db()
        cur = conn.cursor()


        cur.execute("SELECT * FROM products WHERE name = ? AND category = ?", (name, category))
        existing = cur.fetchone()
        if existing:
            messagebox.showerror("Duplicate", f"'{name}' already exists in '{category}' category!")
            conn.close()
            return

        
        cur.execute("INSERT INTO products (name, price, category) VALUES (?, ?, ?)",
                    (name, price_val, category))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"{name} added successfully!")
        win.destroy() 

    tk.Button(win, text="Save", bg=BTN, font=("Arial", 14), command=save).pack(pady=15)

def edit_product_form(pid):
    win = tk.Toplevel()
    win.title("Edit Dessert")
    win.geometry("400x500")
    win.config(bg=BG)

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE id=?", (pid,))
    p = cur.fetchone()
    conn.close()

    tk.Label(win, text="Edit Dessert", font=("Arial", 24, "bold"),
             bg=BG, fg=HEADING).pack(pady=10)

    tk.Label(win, text="Name:", bg=BG).pack()
    name_entry = tk.Entry(win)
    name_entry.insert(0, p[1])
    name_entry.pack()

    tk.Label(win, text="Price:", bg=BG).pack()
    price_entry = tk.Entry(win)
    price_entry.insert(0, p[2])
    price_entry.pack()

    tk.Label(win, text="Category:", bg=BG).pack(pady=(10,0))
    categories = ["Cake", "Cookies", "Sundae", "Brownie", "Coffee"]
    category_var = tk.StringVar()
    category_dropdown = ttk.Combobox(win, textvariable=category_var, values=categories, state="readonly")
    category_dropdown.pack()
    # Set selected category
    if p[3] in categories:
        category_dropdown.current(categories.index(p[3]))
    else:
        category_dropdown.current(0)

    # SAVE CHANGES BUTTON
    def save():
        name = name_entry.get().strip()
        price = price_entry.get().strip()
        category = category_var.get()

        if not name or not price:
            messagebox.showwarning("Error", "Please enter name and price!")
            return

        try:
            price_val = float(price)
        except:
            messagebox.showwarning("Error", "Price must be a number!")
            return

        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            UPDATE products
            SET name=?, price=?, category=?
            WHERE id=?
        """, (name, price_val, category, pid))
        conn.commit()
        conn.close()
        messagebox.showinfo("Updated", f"{name} updated successfully!")
        win.destroy()

    tk.Button(win, text="Save Changes", bg=BTN, font=("Arial", 14), command=save).pack(pady=15)
