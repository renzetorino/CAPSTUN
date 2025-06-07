import tkinter as tk
from tkinter import ttk, messagebox
from supabase import create_client, Client
import add_product

# --- Supabase Setup ---
SUPABASE_URL = "https://qyeegnjmzfyyhecbjomm.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF5ZWVnbmptemZ5eWhlY2Jqb21tIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDkxOTcxNjEsImV4cCI6MjA2NDc3MzE2MX0.7s7bOszi1QX6X4mAFTOOenXYcFaus-7kAVhDmSAMirU"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Tkinter Setup ---
root = tk.Tk()
root.title("BuiswAIz")
root.geometry("1920x720")
root.configure(bg="#FFFFFF")

# Header
header = tk.Frame(root, bg="white")
header.pack(fill=tk.X)
tk.Label(header, text="BuisWaiz", bg="white", font=("Segoe UI", 20, "bold"), fg="#04B4FC").pack(side=tk.LEFT, padx=10, pady=15)
divider = tk.Frame(root, bg="#CED4DA", height=1.5)
divider.pack(fill=tk.X)

# Sidebar
sidebar = tk.Frame(root, bg="#F4F5FC", width=250)
sidebar.pack(side=tk.LEFT, fill=tk.Y)

def sidebarButton(text, command=None):
    return tk.Button(sidebar, text=text, anchor='w', bg="#F4F5FC", fg="#333", 
                     font=("Montserrat", 10, "bold"), bd=0, padx=50, pady=10, 
                     highlightthickness=0, activebackground="#E0E0E0", 
                     command=command)

def on_sidebar_click(name):
    if name == "Inventory":
        populateData()
    else:
        print(f"{name} clicked — future implementation") 

# Add sidebar buttons with actions
for name in ["Dashboard", "Inventory", "Sales", "Expense", "Assistant"]:
    btn = sidebarButton(name, command=lambda n=name: on_sidebar_click(n))
    btn.pack(fill=tk.X)

# Main Content
main = tk.Frame(root, bg="white")
main.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

top = tk.Frame(main, bg="#F4F5FC")
top.pack(fill=tk.X, padx=20, pady=30)

tk.Button(top, text="Add New Product", bg="#04B4FC", fg="white", font=("Montserrat", 10 ,"bold"),
          padx=10, pady=5, command=add_product.open_add_product_window).pack(side=tk.RIGHT, padx=(10,0))
tk.Label(top, text="Inventory", bg="#F4F5FC", font=("Montserrat", 15, "bold"), fg="#000000").pack(side=tk.LEFT, padx=10, pady=15)
tk.Entry(top, font=("Montserrat", 10), width=40, fg="#E0E0E0").pack(side=tk.RIGHT)


title_label = tk.Label(main, text="Product List", bg="#FFFFFF", font=("Segoe UI", 14, "bold"), anchor='w')
title_label.pack(fill=tk.X, padx=20)

# Tree Columns
columns = ("productid", "description", "price", "cost", "currentstock", "reorderpoint", "age", "supplier")

# Treeview Styling
style = ttk.Style()
style.configure("Treeview", font=("Segoe UI", 9), rowheight=40)
style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

tree = ttk.Treeview(main, columns=columns, show="headings", height=12)
tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

# Treeview Headings
col_names = {
    "productid": "Code",
    "description": "Description",
    "price": "Price",
    "cost": "Cost",
    "currentstock": "Quantity",
    "reorderpoint": "Reorder",
    "age": "Age",
    "supplier": "Supplier",
}

for col in columns:
    tree.heading(col, text=col_names.get(col, col))
    tree.column(col, width=140, anchor="center")

# --- Populate Data ---
def populateData():
    try:
        products = supabase.table("products").select("*").execute().data
        suppliers = supabase.table("suppliers").select("supplierid,suppliername").execute().data
        supplier_map = {s["supplierid"]: s["suppliername"] for s in suppliers}

        for row in products:
            values = (
                row.get("productid", ""),
                row.get("description", ""),
                f"₱{row.get('price', 0):,.2f}",
                f"₱{row.get('cost', 0):,.2f}",
                row.get("currentstock", ""),
                row.get("reorderpoint", ""),
                f"{row.get('age', '')} months",
                supplier_map.get(row.get("supplierid"), row.get("supplierid")),
            )
            tree.insert("", "end", values=values)

    except Exception as e:
        print("Data load error:", e)
        messagebox.showerror("Error", f"Could not load data:\n{e}")

populateData()

root.mainloop()
