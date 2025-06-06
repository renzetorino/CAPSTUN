import tkinter as tk
from tkinter import ttk

# Create main window
root = tk.Tk()
root.title("Inventory Manager")
root.geometry("1300x700")
root.configure(bg="#F4F6F8")

# Sidebar
sidebar = tk.Frame(root, bg="#F4F6F8", width=200)
sidebar.pack(side=tk.LEFT, fill=tk.Y)

def add_sidebar_button(text):
    return tk.Button(sidebar, text=text, anchor='w', bg="#F4F6F8", fg="#333", font=("Segoe UI", 10, "bold"), bd=0, padx=20, pady=10, highlightthickness=0, activebackground="#E0E0E0")

tk.Label(sidebar, text="BuisWaiz", bg="#F4F6F8", font=("Segoe UI", 16, "bold"), fg="#009FFD").pack(pady=(20, 30))
add_sidebar_button("📊 Dashboard").pack(fill=tk.X)
add_sidebar_button("📦 Inventory").pack(fill=tk.X)
add_sidebar_button("🛒 Sales").pack(fill=tk.X)
add_sidebar_button("💸 Expenses").pack(fill=tk.X)
tk.Label(sidebar, text="SUPPORT", bg="#F4F6F8", fg="#888", font=("Segoe UI", 9, "bold")).pack(pady=(30, 5))
add_sidebar_button("❓ Help").pack(fill=tk.X)
add_sidebar_button("⚙️ Settings").pack(fill=tk.X)

# Main content area
main = tk.Frame(root, bg="white")
main.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Top bar
topbar = tk.Frame(main, bg="white")
topbar.pack(fill=tk.X, padx=20, pady=10)

search_entry = tk.Entry(topbar, font=("Segoe UI", 10), width=50)
search_entry.pack(side=tk.LEFT, padx=(0, 10))
search_entry.insert(0, "Search")

add_button = tk.Button(topbar, text="➕ Add New Product", bg="#00A6FB", fg="white", font=("Segoe UI", 10, "bold"), padx=15, pady=5)
add_button.pack(side=tk.RIGHT)

# Title
title_label = tk.Label(main, text="Product List", bg="white", font=("Segoe UI", 14, "bold"), anchor='w')
title_label.pack(fill=tk.X, padx=20)

# Table
columns = ("Name", "Code", "Size", "Gender", "Color", "Supplier", "Price", "Quantity")
tree = ttk.Treeview(main, columns=columns, show="headings", height=20)
tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)

root.mainloop()
