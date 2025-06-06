import tkinter as tk
from tkinter import ttk
import add_product


root = tk.Tk()
root.title("BuiswAIz")
root.geometry("1300x700")
root.configure(bg="#FFFFFF")

header = tk.Frame(root, bg="white")
header.pack(fill=tk.X)

tk.Label(
    header,
    text="BuisWaiz",
    bg="white",
    font=("Segoe UI", 20, "bold"),
    fg="#04B4FC"
).pack(side=tk.LEFT, padx=10, pady=15)

divider = tk.Frame(root, bg="#CED4DA", height=1.5)
divider.pack(fill=tk.X)

sidebar = tk.Frame(root, bg ="#F4F5FC", width=250)
sidebar.pack(side=tk.LEFT, fill=tk.Y)

def sidebarButton(text):
    return tk.Button(sidebar, text = text, anchor='w', bg = "#F4F5FC", fg="#333", 
                     font=("Montserrat", 10, "bold"), bd=0, padx=50, pady=10, 
                     highlightthickness=0, activebackground="#E0E0E0")



sidebarButton("Dashboard").pack(fill=tk.X)
sidebarButton("Inventoy").pack(fill=tk.X)
sidebarButton("Sales").pack(fill=tk.X)
sidebarButton("Expense").pack(fill=tk.X)
sidebarButton("Assistant").pack(fill=tk.X)


main = tk.Frame(root, bg="white")
main.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

top = tk.Frame(main, bg="#F4F5FC")
top.pack(fill=tk.X, padx=20, pady=50)

tk.Label(top, text="Inventory", bg="#F4F5FC", font=("Montserrat", 15, "bold"), fg="#000000").pack(side=tk.LEFT, padx=10, pady=15)


additemButton = tk.Button(top, text="Add New Product", bg="#04B4FC", fg="white", font=("Montserrat", 10 ,"bold"),padx=10, pady=5)
additemButton.pack (side=tk.RIGHT, padx=(10,0))

searchBar = tk.Entry(top, font=("Montserrat", 10), width=40, fg ="#E0E0E0")
searchBar.pack(side=tk.RIGHT)
searchBar.insert(0, "Search")

title_label = tk.Label(main, text="Product List", bg="#FFFFFF", font=("Segoe UI", 14, "bold"), anchor='w')
title_label.pack(fill=tk.X, padx=20)


columns = ("Name", "Code", "Size", "Gender", "Color", "Supplier", "Price", "Quantity", )
tree = ttk.Treeview(main, columns=columns, show="headings", height=20)
tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)


root.mainloop()