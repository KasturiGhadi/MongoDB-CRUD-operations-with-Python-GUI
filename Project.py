import tkinter as tk
from tkinter import ttk, messagebox
from pymongo import MongoClient
from bson.objectid import ObjectId

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["productdb_433"]
collection = db["products_433"]

# Window Setup
root = tk.Tk()
root.title("NGD Mini-Project - MongoDB CRUD")
root.geometry("800x600")
root.config(bg="#f0f4f7")
root.config(bg="#c5cae9")

# Title
tk.Label(root, text="433 Kasturi Ghadi -- MongoDB CRUD Operation Using Python-GUI", font=("Arial", 16, "bold"), bg="#283593", fg="white", padx=10, pady=10).pack(fill="x")

# NGD Frame
ngd_frame = tk.LabelFrame(root, text="Product Details", font=("Arial", 14, "bold"), bg="#f0f4f7", fg="black", padx=10, pady=10)
ngd_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Input variables
pid_var = tk.StringVar()
name_var = tk.StringVar()
category_var = tk.StringVar()
brand_var = tk.StringVar()
price_var = tk.StringVar()
stock_var = tk.StringVar()

# Input Fields
fields = [
    ("Product ID", pid_var),
    ("Product Name", name_var),
    ("Category", category_var),
    ("Brand", brand_var),
    ("Price", price_var),
    ("Stock Quantity", stock_var)
]

for i, (label, var) in enumerate(fields):
    tk.Label(ngd_frame, text=label, bg="#f0f4f7", font=("Arial", 12)).grid(row=i, column=0, sticky="w", padx=10, pady=5)
    tk.Entry(ngd_frame, textvariable=var, width=30).grid(row=i, column=1, padx=10, pady=5)

# Button Frame
btn_frame = tk.Frame(ngd_frame, bg="#f0f4f7")
btn_frame.grid(row=6, column=0, columnspan=2, pady=10)

tk.Button(btn_frame, text="Insert", command=lambda: insert_product(), width=15, bg="#4CAF50", fg="white", font=("Arial", 11)).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Display Data", command=lambda: refresh_products(), width=15, bg="#2196F3", fg="white", font=("Arial", 11)).grid(row=0, column=1, padx=10)
tk.Button(btn_frame, text="Update", command=lambda: update_product(), width=15, bg="#FFC107", fg="black", font=("Arial", 11)).grid(row=0, column=2, padx=10)
tk.Button(btn_frame, text="Delete", command=lambda: delete_product(), width=15, bg="#F44336", fg="white", font=("Arial", 11)).grid(row=0, column=3, padx=10)

# Treeview
tree_frame = tk.Frame(ngd_frame)
tree_frame.grid(row=7, column=0, columnspan=2, pady=10)

columns = ("Product ID", "Name", "Category", "Brand", "Price", "Stock")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=100)
tree.pack(fill="both", expand=True)

def refresh_products():
    tree.delete(*tree.get_children())
    for product in collection.find():
        tree.insert("", tk.END, iid=str(product["_id"]), values=(
            product.get("product_id", ""),
            product["name"],
            product["category"],
            product["brand"],
            product["price"],
            product["stock"]
        ))

def insert_product():
    try:
        price = float(price_var.get())
        stock = int(stock_var.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Price must be a number and Stock must be an integer.")
        return

    if all([pid_var.get(), name_var.get(), category_var.get(), brand_var.get()]):
        collection.insert_one({
            "product_id": pid_var.get(),
            "name": name_var.get(),
            "category": category_var.get(),
            "brand": brand_var.get(),
            "price": price,
            "stock": stock
        })
        clear_fields()
    else:
        messagebox.showwarning("Missing Info", "Please fill all fields.")

def update_product():
    selected = tree.selection()
    if selected:
        product_id = selected[0]
        try:
            price = float(price_var.get())
            stock = int(stock_var.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Price must be a number and Stock must be an integer.")
            return

        if all([pid_var.get(), name_var.get(), category_var.get(), brand_var.get()]):
            collection.update_one(
                {"_id": ObjectId(product_id)},
                {"$set": {
                    "product_id": pid_var.get(),
                    "name": name_var.get(),
                    "category": category_var.get(),
                    "brand": brand_var.get(),
                    "price": price,
                    "stock": stock
                }}
            )
            clear_fields()
        else:
            messagebox.showwarning("Missing Info", "Please fill all fields.")
    else:
        messagebox.showwarning("No Selection", "Select a product to update.")

def delete_product():
    selected = tree.selection()
    if selected:
        collection.delete_one({"_id": ObjectId(selected[0])})
        clear_fields()
        refresh_products()
    else:
        messagebox.showwarning("No Selection", "Select a product to delete.")

def on_select(event):
    selected = tree.selection()
    if selected:
        product = tree.item(selected[0])["values"]
        pid_var.set(product[0])
        name_var.set(product[1])
        category_var.set(product[2])
        brand_var.set(product[3])
        price_var.set(product[4])
        stock_var.set(product[5])

def clear_fields():
    for var in [pid_var, name_var, category_var, brand_var, price_var, stock_var]:
        var.set("")

tree.bind("<<TreeviewSelect>>", on_select)

root.mainloop()
