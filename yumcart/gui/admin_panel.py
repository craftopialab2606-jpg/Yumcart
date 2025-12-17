import tkinter as tk
from tkinter import messagebox
from database.database import get_db
from .product_forms import add_product_form, edit_product_form


BG = "#FFF7E6"
BTN = "#FFB6C1"
BTN_HOVER = "#FF9AA2"
HEADING = "#D35400"

def open_admin_panel():
    win = tk.Toplevel()
    win.title("Admin Panel")
    win.geometry("650x550")
    win.config(bg=BG)

    tk.Label(win, text="Admin Dashboard", font=("Arial", 28, "bold"),
             fg=HEADING, bg=BG).pack(pady=20)

    # -------- ADD PRODUCT ----------
    tk.Button(win, text="Add Dessert", font=("Arial", 16), bg=BTN,
              command=lambda: add_product_form()).pack(pady=5)

    # -------- VIEW ALL PRODUCTS ----
    tk.Button(win, text="View All Desserts", font=("Arial", 16), bg=BTN,
              command=view_products).pack(pady=5)

    # -------- VIEW CATEGORIES -------
    tk.Button(win, text="View Categories", font=("Arial", 16), bg=BTN,
              command=view_categories).pack(pady=5)

def view_products():
    win = tk.Toplevel()
    win.title("All Products")
    win.geometry("650x550")
    win.config(bg="#FFF7E6")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    rows = cur.fetchall()
    conn.close()

    for p in rows:
        frame = tk.Frame(win, bg="#FFF7E6")
        frame.pack(pady=4)

        tk.Label(frame, text=f"{p[1]} - Rs {p[2]} ({p[3]})",
                 font=("Arial", 14), bg="#FFF7E6").grid(row=0, column=0, padx=10)

        tk.Button(frame, text="Edit", bg="#FFB6C1",
                  command=lambda x=p[0]: edit_product_form(x)).grid(row=0, column=1, padx=5)

        tk.Button(frame, text="Delete", bg="#FFB6C1",
                  command=lambda x=p[0], w=win: delete_product(x, w)).grid(row=0, column=2, padx=5)


def delete_product(pid, window):
    confirm = messagebox.askyesnocancel("Confirm", "Delete this dessert?")
    if confirm:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM products WHERE id=?", (pid,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Deleted", "Dessert deleted!")
        window.destroy()
        view_products()


def view_categories():
    win = tk.Toplevel()
    win.title("Categories")
    win.geometry("400x400")
    win.config(bg=BG)

    tk.Label(win, text="Available Categories", font=("Arial", 22, "bold"),
             bg=BG, fg=HEADING).pack(pady=10)

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT category FROM products")
    categories = cur.fetchall()
    conn.close()

    for c in categories:
        tk.Label(win, text=c[0], font=("Arial", 16),
                 bg=BG).pack(pady=4)
