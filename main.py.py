import tkinter as tk
import mysql.connector
from tkinter import messagebox, ttk
from datetime import date

#  DATABASE CONNECTION 
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # change according to your mysql user
        password="SQLroot@123",
        database="blood_camp_db"
    )

#  ROOT WINDOW SETUP 
root = tk.Tk()
root.title("Blood Donation Camp Coordination System")

# Maximize window (Use 'zoomed' for Windows. Added fallback for Mac/Linux)
try:
    root.state('zoomed') 
except tk.TclError:
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}")

# STYLING (TABS & TABLES)
style = ttk.Style()
style.theme_use('default')

# Make the Tabs bigger
style.configure("TNotebook.Tab", font=("Arial", 16, "bold"), padding=[30, 15])

# Make the Treeview (Tables) bigger to match the screen
style.configure("Treeview", rowheight=30, font=("Arial", 12))
style.configure("Treeview.Heading", font=("Arial", 14, "bold"))

# Standard font for all labels and entries
APP_FONT = ("Arial", 14)

notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True, padx=20, pady=20)


#  TAB 1: DONOR REGISTRATION
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Donor Registration")

tk.Label(tab1, text="Name:", font=APP_FONT).grid(row=0, column=0, padx=20, pady=15, sticky="e")
tk.Label(tab1, text="Age:", font=APP_FONT).grid(row=1, column=0, padx=20, pady=15, sticky="e")
tk.Label(tab1, text="Blood Group:", font=APP_FONT).grid(row=2, column=0, padx=20, pady=15, sticky="e")
tk.Label(tab1, text="Contact:", font=APP_FONT).grid(row=3, column=0, padx=20, pady=15, sticky="e")
tk.Label(tab1, text="City:", font=APP_FONT).grid(row=4, column=0, padx=20, pady=15, sticky="e")

ename = tk.Entry(tab1, font=APP_FONT)
ename.grid(row=0, column=1, padx=20, pady=15)
eage = tk.Entry(tab1, font=APP_FONT)
eage.grid(row=1, column=1, padx=20, pady=15)
ebg = ttk.Combobox(tab1, values=["A+","B+","A-","B-","AB+","AB-","O+","O-"], font=APP_FONT, state="readonly")
ebg.grid(row=2, column=1, padx=20, pady=15)
econtact = tk.Entry(tab1, font=APP_FONT)
econtact.grid(row=3, column=1, padx=20, pady=15)
ecity = tk.Entry(tab1, font=APP_FONT)
ecity.grid(row=4, column=1, padx=20, pady=15)

def add_donor():
    try:
        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO donors(name,age,blood_group,phone_no,city,last_donation) VALUES (%s,%s,%s,%s,%s,%s)", 
                    (ename.get(), eage.get(), ebg.get(), econtact.get(), ecity.get(), date.today()))
        db.commit()
        messagebox.showinfo("Success", "Donor added!!")
        show_donors() # Refresh treeview
    except Exception as ex:
        messagebox.showerror("Error", str(ex))

tk.Button(tab1, text="Add Donor", command=add_donor, bg="red", fg="white", font=("Arial", 14, "bold"), width=20, height=2).grid(row=5, column=0, columnspan=2, pady=30)

tab1.grid_columnconfigure(2, weight=1)

tree_donor = ttk.Treeview(tab1, columns=("ID","Name","Age","Blood Group","Contact","City"), show="headings")

for col in ("ID","Name","Age","Blood Group","Contact","City"):
    tree_donor.heading(col, text=col)
    tree_donor.column(col, width=130, anchor="center") 

tree_donor.grid(row=0, column=2, rowspan=6, padx=40, sticky="nsew")
def show_donors():
    try:
        for i in tree_donor.get_children():
            tree_donor.delete(i)
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT id, name, age, blood_group, phone_no, city FROM donors")
        for row in cur.fetchall():
            tree_donor.insert("", "end", values=row)
    except Exception as ex:
        print("Show Donor Error:", ex)

show_donors()


#  TAB 2: CAMP MANAGEMENT 
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Camp Management")

tk.Label(tab2, text="Camp Name:", font=APP_FONT).grid(row=0, column=0, padx=20, pady=15, sticky="e")
tk.Label(tab2, text="Location:", font=APP_FONT).grid(row=1, column=0, padx=20, pady=15, sticky="e")
tk.Label(tab2, text="Date (YYYY-MM-DD):", font=APP_FONT).grid(row=2, column=0, padx=20, pady=15, sticky="e")
tk.Label(tab2, text="Organizer:", font=APP_FONT).grid(row=3, column=0, padx=20, pady=15, sticky="e") 

cname = tk.Entry(tab2, font=APP_FONT)
cname.grid(row=0, column=1, padx=20, pady=15)
c_loc = tk.Entry(tab2, font=APP_FONT)
c_loc.grid(row=1, column=1, padx=20, pady=15)
cdate = tk.Entry(tab2, font=APP_FONT)
cdate.grid(row=2, column=1, padx=20, pady=15)
corg = tk.Entry(tab2, font=APP_FONT)
corg.grid(row=3, column=1, padx=20, pady=15)

def add_camp():
    try:
        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO camps (camp_name, location, camp_date, organizer) values(%s,%s,%s,%s)",
                    (cname.get(), c_loc.get(), cdate.get(), corg.get()))
        db.commit()
        messagebox.showinfo("Success", "Camp created!")
    except Exception as ex:
        messagebox.showerror("Error", str(ex))

tk.Button(tab2, text="Create camp", command=add_camp, bg="darkblue", fg="white", font=("Arial", 14, "bold"), width=20, height=2).grid(row=4, column=0, columnspan=2, pady=30)


# TAB 3: INVENTORY
tab3 = ttk.Frame(notebook)
notebook.add(tab3, text="Blood Inventory")

tk.Label(tab3, text="Blood group:", font=APP_FONT).grid(row=0, column=0, padx=20, pady=15, sticky="e")
tk.Label(tab3, text="Units:", font=APP_FONT).grid(row=1, column=0, padx=20, pady=15, sticky="e")
tk.Label(tab3, text="Camp ID:", font=APP_FONT).grid(row=2, column=0, padx=20, pady=15, sticky="e")

ibg = ttk.Combobox(tab3, values=["A+","B+","A-","B-","AB+","AB-","O+","O-"], font=APP_FONT, state="readonly")
ibg.grid(row=0, column=1, padx=20, pady=15)
iunit = tk.Entry(tab3, font=APP_FONT)
iunit.grid(row=1, column=1, padx=20, pady=15)
icamp_id = tk.Entry(tab3, font=APP_FONT)
icamp_id.grid(row=2, column=1, padx=20, pady=15)

def add_inventory():
    try:
        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO inventory(blood_group, units, camp_id) values (%s,%s,%s)", 
                    (ibg.get(), iunit.get(), icamp_id.get()))
        db.commit()
        messagebox.showinfo("Success", "Inventory updated!!")
        show_inventory()
    except Exception as ex:
        messagebox.showerror("Error", str(ex))

tk.Button(tab3, text="Add stock", command=add_inventory, bg="purple", fg="white", font=("Arial", 14, "bold"), width=20, height=2).grid(row=3, column=0, columnspan=2, pady=30)

tree_inv = ttk.Treeview(tab3, columns=("BG", "Total Units"), show='headings')
for col in ("BG", "Total Units"): 
    tree_inv.heading(col, text=col)
tree_inv.grid(row=0, column=2, rowspan=4, padx=40, sticky="nsew")

def show_inventory():
    try:
        for i in tree_inv.get_children():
            tree_inv.delete(i)
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT blood_group, SUM(units) FROM inventory GROUP BY blood_group")
        for row in cur.fetchall():
            tree_inv.insert("", "end", values=row)
    except Exception as ex:
        print("Show Inventory Error:", ex)

show_inventory()


#  TAB 4: PATIENT REQUEST 
tab4 = ttk.Frame(notebook)
notebook.add(tab4, text="Patient Request")

tk.Label(tab4, text="Patient name:", font=APP_FONT).grid(row=0, column=0, padx=20, pady=15, sticky="e")
tk.Label(tab4, text="Needed blood group:", font=APP_FONT).grid(row=1, column=0, padx=20, pady=15, sticky="e")
tk.Label(tab4, text="Units Needed:", font=APP_FONT).grid(row=2, column=0, padx=20, pady=15, sticky="e")

r_name = tk.Entry(tab4, font=APP_FONT)
r_name.grid(row=0, column=1, padx=20, pady=15)

r_bg = ttk.Combobox(tab4, values=["A+","B+","A-","B-","AB+","AB-","O+","O-"], font=APP_FONT, state="readonly")
r_bg.grid(row=1, column=1, padx=20, pady=15)

r_units = tk.Entry(tab4, font=APP_FONT)
r_units.grid(row=2, column=1, padx=20, pady=15)

def check_and_request():
    try:
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT SUM(units) FROM inventory WHERE blood_group=%s", (r_bg.get(),))
        result = cur.fetchone()[0]
        total = int(result) if result else 0
        
        req_units = int(r_units.get())
        
        if total >= req_units:
            cur.execute("INSERT INTO requests(patient_name, blood_group, units_needed, hospital, status) values (%s,%s,%s,%s,%s)",
                        (r_name.get(), r_bg.get(), req_units, "General Hospital", "Approved"))
            # Deduct the stock
            cur.execute("UPDATE inventory SET units = units - %s WHERE blood_group=%s LIMIT 1", (req_units, r_bg.get()))
            db.commit()
            messagebox.showinfo("Approved", f"Blood available! Total stock was {total} units.")
        else:
            messagebox.showwarning("Not available", f"Only {total} units are available for {r_bg.get()}")
            
        show_inventory()
    except Exception as ex:
        messagebox.showerror("Error", str(ex))

tk.Button(tab4, text="Check availability", command=check_and_request, bg="green", fg="white", font=("Arial", 14, "bold"), width=20, height=2).grid(row=3, column=0, columnspan=2, pady=30)

#RUN APP 
root.mainloop()
