import tkinter as tk
from tkinter import ttk, messagebox
from supabase import create_client, Client

SUPABASE_URL = "https://qyeegnjmzfyyhecbjomm.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF5ZWVnbmptemZ5eWhlY2Jqb21tIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDkxOTcxNjEsImV4cCI6MjA2NDc3MzE2MX0.7s7bOszi1QX6X4mAFTOOenXYcFaus-7kAVhDmSAMirU"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def open_add_product_window():
    popup = tk.Toplevel()
    popup.title("Add New Product")
    popup.geometry("600x700")
    popup.configure(bg="white")

    tk.Label(popup, text="Add New Product", font=("Segoe UI", 18, "bold"), bg="white").pack(pady=20)

    container = tk.Frame(popup, bg="white")
    container.pack(fill=tk.BOTH, expand=True, padx=30)

    fields = {
        "productname": "Product Name",
        "description": "Description",
        "price": "Price",
        "cost": "Cost",
        "currentstock": "Current Stock",
        "reorderpoint": "Reorder Point",
        "age": "Age (months)"
    }

    entries = {}
    for key, label in fields.items():
        field_frame = tk.Frame(container, bg="white")
        field_frame.pack(fill=tk.X, pady=5)
        tk.Label(field_frame, text=label, width=18, anchor="w", bg="white").pack(side=tk.LEFT)
        entry = tk.Entry(field_frame)
        entry.pack(fill=tk.X, expand=True)
        entries[key] = entry

    # Supplier dropdown
    supplier_frame = tk.Frame(container, bg="white")
    supplier_frame.pack(fill=tk.X, pady=5)
    tk.Label(supplier_frame, text="Supplier", width=18, anchor="w", bg="white").pack(side=tk.LEFT)

    try:
        supplier_response = supabase.table("suppliers").select("supplierid,suppliername").execute()
        suppliers = supplier_response.data or []
    except Exception as e:
        suppliers = []
        messagebox.showerror("Error", f"Failed to load suppliers: {e}")

    supplier_names = [s["suppliername"] for s in suppliers]
    supplier_map = {s["suppliername"]: s["supplierid"] for s in suppliers}

    supplier_var = tk.StringVar()
    supplier_dropdown = ttk.Combobox(supplier_frame, textvariable=supplier_var, values=supplier_names, state="readonly")
    supplier_dropdown.pack(fill=tk.X, expand=True)

    def save_product():
        try:
            data = {field: entry.get().strip() for field, entry in entries.items()}
            selected_supplier = supplier_var.get()
            if not selected_supplier:
                messagebox.showerror("Missing Field", "Please select a supplier.")
                return

            data["supplierid"] = supplier_map[selected_supplier]

            # Type conversion
            for field in ["price", "cost"]:
                try:
                    data[field] = float(data[field])
                except ValueError:
                    data[field] = 0.0

            for field in ["currentstock", "reorderpoint", "age"]:
                try:
                    data[field] = int(data[field])
                except ValueError:
                    messagebox.showerror("Invalid Input", f"{field} must be an integer.")
                    return

            # Insert to Supabase
            response = supabase.table("products").insert(data).execute()

            if response.data:
                messagebox.showinfo("Success", "Product saved successfully.")
                popup.destroy()
            else:
                messagebox.showerror("Insert Failed", "Insert failed. No data returned.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")

    tk.Button(container, text="Save Product", bg="#04B4FC", fg="white",
              font=("Segoe UI", 10, "bold"), command=save_product).pack(pady=20, fill=tk.X)

    popup.transient()
    popup.grab_set()
    popup.focus_set()
