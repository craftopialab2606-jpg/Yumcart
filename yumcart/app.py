import tkinter as tk
from database.database import setup_tables
from gui.customer_panel import CustomerPanel
from gui.login_window import login_window

BG = "#FFF7E6"
HEADING = "#D35400"
PANEL_BG = "#FFEBD2"
BTN = "#FFB6C1"

setup_tables()

root = tk.Tk()
root.title("YUMCART")
root.geometry("900x550")
root.config(bg=BG)

# -------------------- TOP HEADER BAR --------------------
header_frame = tk.Frame(root, bg=BG)
header_frame.pack(fill="x", pady=10, padx=10)

title_label = tk.Label(
    header_frame,
    text="     WELCOME TO YUM-CART BAKESHOP   ",
    font=("Arial", 26, "bold"),
    fg=HEADING,
    bg=BG
)

title_label.pack(side="left", padx=250, pady=20)

login_btn = tk.Button(
    header_frame,
    text="Login",
    font=("Arial", 15, "bold"),
    bg=BTN,
    command=lambda: login_window(root)
)
login_btn.pack(side="right", padx=10, pady=10)

# -------------------- MAIN CONTENT AREA --------------------
main_frame = tk.Frame(root, bg=BG)
main_frame.pack(fill="both", expand=True, padx=15, pady=10)

# ---- LEFT PRODUCT AREA ----
product_frame = tk.Frame(main_frame, bg=PANEL_BG, bd=2, relief="solid")
product_frame.pack(side="left", fill="both", expand=True, padx=10)

tk.Label(
    product_frame,
    text="Available Desserts",
    bg=PANEL_BG,
    fg=HEADING,
    font=("Arial", 20, "bold")
).pack(pady=10)

# Create CustomerPanel and store reference
cp = CustomerPanel(product_frame)

# -------------------- RIGHT ACTION PANEL --------------------
action_frame = tk.Frame(main_frame, bg=PANEL_BG, width=200, bd=2, relief="solid")
action_frame.pack(side="right", fill="y", padx=10)

tk.Label(
    action_frame,
    text="Place Order",
    bg=PANEL_BG,
    fg=HEADING,
    font=("Arial", 18, "bold")
).pack(pady=15)

btn_style = {"font": ("Arial", 14), "bg": BTN, "width": 15, "pady": 5}

tk.Button(
    action_frame,
    text="Add to Cart",
    command=lambda: cp.add_selected_to_cart(),
    **btn_style
).pack(pady=10)

tk.Button(
    action_frame,
    text="View Cart",
    command=lambda: cp.open_cart(),
    **btn_style
).pack(pady=10)

tk.Button(
    action_frame,
    text="Checkout",
    command=lambda: cp.checkout(),
    **btn_style
).pack(pady=10)

tk.Button(
    action_frame,
    text="Orders History",
    command=lambda: cp.view_orders(),
    font=("Arial", 14),
    bg=BTN,
    width=15,
    pady=5
).pack(pady=10)

root.mainloop()
