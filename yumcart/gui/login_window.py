# login_window.py
import tkinter as tk
from tkinter import messagebox
import os
import sqlite3
from gui.admin_panel import open_admin_panel

# Constants
BG = "#FFF7E6"
BTN = "#FFB6C1"
HEADING = "#D35400"

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "database", "yumcart.db")
def get_db():
    return sqlite3.connect(DB_PATH)

def login_window(master=None):
    if master is None:
        master = tk.Tk()
        master.withdraw()

    win = tk.Toplevel(master)
    win.title("YUMCART login")
    win.geometry("400x350")
    win.config(bg=BG)

    tk.Label(win, text="YUMCART login", font=("Arial", 24, "bold"),
             fg=HEADING, bg=BG).pack(pady=20)

    tk.Label(win, text="Username:", bg=BG).pack()
    username = tk.Entry(win)
    username.pack()

    tk.Label(win, text="Password:", bg=BG).pack()
    password = tk.Entry(win, show="*")
    password.pack()


    def check_login():
        u = username.get().strip()
        p = password.get().strip()

        try:
            if u == "admin" and p == "123":
                messagebox.showinfo("Success", "Welcome Admin!")
                open_admin_panel()
                win.destroy()
            else:
                raise ValueError("Invalid credentials")

        except ValueError:
            messagebox.showerror("Error", "Incorrect username or password!")

    btn = tk.Button(win, text="Login", bg=BTN, font=("Arial", 14),
                    command=check_login)
    btn.pack(pady=20)

    return win

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("YumCart Main")
    root.withdraw() 
    login_window(root)
    root.mainloop()
