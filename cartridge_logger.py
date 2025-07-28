import tkinter as tk
from tkinter import messagebox, filedialog
import csv
import os
from datetime import datetime
import getpass

# ---------- Mappings ----------
cartridge_dict = {
     106: "CARTUCHO BROTHER LC985",               
     107: "BROTHER Nº22220A",                     
     112: "CANON CARTUCHO BLACK 5450",            
     113: "CANON CARTUCHO Nº 550",                
     114: "CANON Nº 555",                         
     115: "CANON Nº 726",                         
     116: "CANON Nº5450",                         
     117: "CANON Nº550",                          
     121: "CARTRIDGE EPSON 27XL",                 
     138: "DILETTA DC-800 (PASSPORT PRINTER)",    
     144: "EPSON 27XL",                           
     145: "EPSON 16XL",                           
     146: "EPSON 34XL (K, M, Y, C)",              
     147: "EPSON 405XL",                          
     148: "EPSON T0711 BLACK",                    
     149: "EPSON T61/62/63/64",                   
     150: "EPSON T7021 (K, M, Y, C)",             
     151: "EPSON WF5219 (K, M, Y, C)",            
     152: "EPSON WF5620 (K, M, Y, C)",           
     166: "HP 2400",                              
     167: "HP 255A",                              
     168: "HP 53A",                               
     169: "HP 59X (K)",                           
     170: "HP 901 XL BLACK",                      
     171: "HP 901 XL COLOR",                      
     172: "HP 903 XL (K, M, Y, C)",               
     173: "HP 953XL (K, M, Y, C)",                
     174: "HP 963 XL",                            
     175: "HP C6345A",                            
     176: "HP LASERJET PRO 26A",                  
     177: "HP TONER LASERJET M402 HP 25",         
     180: "KYOCERA 5240 BLACK",                   
     181: "KYOCERA 5240 CYAN",                    
     182: "KYOCERA 5240 MAGENTA",                 
     183: "KYOCERA 5240 YELLOW",                  
     189: "LJ1006P BLACK",                        
     259: "TONER RICOH PG600 (K, M, Y, C)",       
     260: "TONER XEROX PHASER 6125 (K, M, Y, C)", 
     264: "XEROX TONER NEGRO",                    
     267: "HP 937 BLACK HIGH CAPACITY",           
     268: "HP 937 CMY HIGH CAPACITY",             
     272: "HP 937 K N/C",                         
     273: "HP 937 MCY N/C",                       
     274: "HP 903 BLACK",                         
     275: "HP 903 MCY"                           
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
