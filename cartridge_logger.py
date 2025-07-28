import tkinter as tk
from tkinter import messagebox, filedialog
import csv
import os
from datetime import datetime
import getpass

# ---------- Mappings ----------
cartridge_dict = {
    1: "HP 44A",
    2: "Canon 737",
    3: "Brother TN-2420"
}

colleague_dict = {
    1: "Darius",
    2: "Swathika",
    3: "Deepthi"
}

cartridge_name_to_id = {v: k for k, v in cartridge_dict.items()}
colleague_name_to_id = {v: k for k, v in colleague_dict.items()}

# ---------- File ----------
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
CSV_FILE = os.path.join(desktop_path, "cartridge_consumption_log.csv")
HEADERS = ["Date", "UserID", "CartridgeID", "Quantity", "Remarks"]

# ---------- Save Function ----------
def save_entry():
    date = date_entry.get()
    user_name = user_var.get()
    cartridge_name = cartridge_var.get()
    quantity = quantity_entry.get()
    remarks = remarks_entry.get()

    if not (date and user_name and cartridge_name and quantity):
        messagebox.showwarning("Missing Info", "Please fill in all required fields.")
        return

    try:
        quantity = int(quantity)
    except ValueError:
        messagebox.showerror("Invalid Input", "Quantity must be a number.")
        return

    user_id = colleague_name_to_id.get(user_name)
    cartridge_id = cartridge_name_to_id.get(cartridge_name)

    new_row = [date, user_id, cartridge_id, quantity, remarks]

    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(HEADERS)
        writer.writerow(new_row)

    messagebox.showinfo("Saved", f"Entry saved to:\n{CSV_FILE}")
    clear_fields()

# ---------- Clear Function ----------
def clear_fields():
    date_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    remarks_entry.delete(0, tk.END)
    date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
    user_var.set(list(colleague_dict.values())[0])
    cartridge_var.set(list(cartridge_dict.values())[0])

# ---------- Export Function ----------
def export_csv():
    dest = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if dest:
        try:
            with open(CSV_FILE, "r", encoding="utf-8") as src, open(dest, "w", newline="", encoding="utf-8") as dst:
                dst.write(src.read())
            messagebox.showinfo("Exported", f"Data exported to {dest}")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed:\n{e}")

# ---------- GUI ----------
root = tk.Tk()
root.title("Cartridge Consumption Logger")
root.geometry("400x350")

tk.Label(root, text="Date (YYYY-MM-DD):").pack()
date_entry = tk.Entry(root)
date_entry.pack()
date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

tk.Label(root, text="User:").pack()
user_var = tk.StringVar(root)
user_var.set(list(colleague_dict.values())[0])
tk.OptionMenu(root, user_var, *colleague_dict.values()).pack()

tk.Label(root, text="Cartridge Type:").pack()
cartridge_var = tk.StringVar(root)
cartridge_var.set(list(cartridge_dict.values())[0])
tk.OptionMenu(root, cartridge_var, *cartridge_dict.values()).pack()

tk.Label(root, text="Quantity:").pack()
quantity_entry = tk.Entry(root)
quantity_entry.pack()

tk.Label(root, text="Remarks:").pack()
remarks_entry = tk.Entry(root)
remarks_entry.pack()

tk.Button(root, text="Save Entry", command=save_entry).pack(pady=5)
tk.Button(root, text="Export to CSV", command=export_csv).pack(pady=5)

root.mainloop()
