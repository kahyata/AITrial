import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import sqlite3
import os

# Define the path to the SQLite database
db_path = r'C:\Users\User\Desktop\Database projects\sqlite\sqlite-tools-win-x64-3460000\Sacco\src\sacco.db'

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Function to load CSV data
def load_csv():
    filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not filepath:
        return
    
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(filepath)
        
        # Clear the existing treeview
        for item in tree.get_children():
            tree.delete(item)
        
        # Update the treeview columns and data
        tree["columns"] = list(df.columns)
        tree.heading("#0", text="Index")
        for col in df.columns:
            tree.heading(col, text=col.upper(), anchor="center")
            tree.column(col, anchor="center", width=100)
        
        # Insert data into the treeview
        for index, row in df.iterrows():
            tree.insert("", tk.END, text=index, values=list(row))
    
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load CSV file: {e}")

# Function to update table selection
def select_table():
    global selected_table
    selected_table = table_var.get()
    if not selected_table:
        messagebox.showwarning("Warning", "Please select a table.")
        return

    # Open the table entry window
    open_table_entry_window()

# Function to open a new window for table entry
def open_table_entry_window():
    global entry_window, entry_frame
    
    # Create a new top-level window
    entry_window = tk.Toplevel(root)
    entry_window.title(f"Enter Data into {selected_table}")
    entry_window.geometry("500x400")
    entry_window.configure(bg="#f0f0f0")
    
    # Frame for input fields
    entry_frame = tk.Frame(entry_window, bg="#ffffff", padx=10, pady=10)
    entry_frame.pack(expand=True, fill=tk.BOTH)
    
    # Generate input fields based on the selected table's columns
    columns = get_table_columns(selected_table)
    input_fields.clear()  # Clear previous fields
    
    for col in columns:
        lbl = tk.Label(entry_frame, text=col, bg="#ffffff")
        lbl.grid(row=len(input_fields), column=0, padx=5, pady=5, sticky=tk.W)
        entry = tk.Entry(entry_frame, width=40)
        entry.grid(row=len(input_fields), column=1, padx=5, pady=5)
        input_fields[col] = entry
    
    # Add Submit and Exit buttons
    submit_btn = tk.Button(entry_frame, text="Submit Data", command=submit_data, bg="#007bff", fg="#ffffff", font=("Arial", 12, "bold"))
    submit_btn.grid(row=len(input_fields), column=0, columnspan=2, pady=10)

    exit_btn = tk.Button(entry_frame, text="Exit", command=close_entry_window, bg="#dc3545", fg="#ffffff", font=("Arial", 12, "bold"))
    exit_btn.grid(row=len(input_fields)+1, column=0, columnspan=2, pady=10)

# Function to get table columns from the database
def get_table_columns(table_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [row[1] for row in cursor.fetchall()]
    return columns

# Function to submit data to the selected table
def submit_data():
    if not selected_table:
        messagebox.showwarning("Warning", "No table selected.")
        return
    
    try:
        # Retrieve data from input fields
        data = [input_fields[col].get() for col in get_table_columns(selected_table)]
        placeholders = ', '.join(['?' for _ in data])
        sql = f"INSERT INTO {selected_table} VALUES ({placeholders})"
        cursor.execute(sql, data)
        conn.commit()
        messagebox.showinfo("Success", "Data submitted successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to submit data: {e}")

# Function to close the table entry window
def close_entry_window():
    global entry_window
    entry_window.destroy()
    entry_window = None

# Function to exit and return to the selection menu
def exit_selection():
    global selected_table
    selected_table = None
    tree.delete(*tree.get_children())
    submit_button.config(state=tk.DISABLED)
    if entry_window:
        entry_window.destroy()

# Create main window
root = tk.Tk()
root.title("CSV Viewer")
root.geometry("900x600")
root.configure(bg="#f0f0f0")

# Frame for the buttons and selection
button_frame = tk.Frame(root, bg="#ffffff", padx=10, pady=10)
button_frame.pack(fill=tk.X)

# Label and dropdown for table selection
select_label = tk.Label(button_frame, text="Select Table:", bg="#ffffff", font=("Arial", 12, "bold"))
select_label.pack(side=tk.LEFT, padx=5)

table_var = tk.StringVar()
table_menu = tk.OptionMenu(button_frame, table_var, *[
    'Businesses', 'Transactions', 'Accounts', 'Invoices', 'Expenses', 'Revenue',
    'Assets', 'Liabilities', 'FinancialSummary', 'Receipts'
])
table_menu.pack(side=tk.LEFT, padx=5)

# Select button
select_button = tk.Button(button_frame, text="Select", command=select_table, bg="#28a745", fg="#ffffff", font=("Arial", 12, "bold"))
select_button.pack(side=tk.LEFT, padx=5)

# Load button
load_button = tk.Button(button_frame, text="Load CSV", command=load_csv, bg="#17a2b8", fg="#ffffff", font=("Arial", 12, "bold"))
load_button.pack(side=tk.LEFT, padx=5)

# Submit button
submit_button = tk.Button(button_frame, text="Submit Data", command=submit_data, bg="#007bff", fg="#ffffff", font=("Arial", 12, "bold"), state=tk.DISABLED)
submit_button.pack(side=tk.LEFT, padx=5)

# Exit button
exit_button = tk.Button(button_frame, text="Exit", command=exit_selection, bg="#dc3545", fg="#ffffff", font=("Arial", 12, "bold"))
exit_button.pack(side=tk.LEFT, padx=5)

# Treeview to display CSV data
tree = ttk.Treeview(root, show="headings")
tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

# Scrollbars for the treeview
vsb = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
vsb.pack(side='right', fill='y')
tree.configure(yscrollcommand=vsb.set)

hsb = ttk.Scrollbar(root, orient="horizontal", command=tree.xview)
hsb.pack(side='bottom', fill='x')
tree.configure(xscrollcommand=hsb.set)

# Style configuration
style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 12, "bold"), foreground="#007bff")  # Blue colored and bold headings
style.configure("Treeview", font=("Arial", 10), rowheight=30)  # Set row height for better readability

# Initialize selected table variable
selected_table = None
entry_window = None
input_fields = {}

# Start the Tkinter event loop
root.mainloop()

# Close the connection
conn.close()
