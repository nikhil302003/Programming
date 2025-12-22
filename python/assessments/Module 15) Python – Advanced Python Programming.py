import tkinter as tk
from tkinter import messagebox
import sqlite3
import re
from datetime import datetime


conn = sqlite3.connect("medicare.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users(
    username TEXT PRIMARY KEY,
    password TEXT,
    role TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS patients(
    pid INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    disease TEXT,
    status TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS appointments(
    aid INTEGER PRIMARY KEY AUTOINCREMENT,
    pid INTEGER,
    doctor TEXT,
    date TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS billing(
    bid INTEGER PRIMARY KEY AUTOINCREMENT,
    pid INTEGER,
    amount REAL,
    tax REAL,
    total REAL
)
""")

conn.commit()


cur.execute("INSERT OR IGNORE INTO users VALUES('admin','admin123','Admin')")
cur.execute("INSERT OR IGNORE INTO users VALUES('reception','rec123','Receptionist')")
cur.execute("INSERT OR IGNORE INTO users VALUES('doctor','doc123','Doctor')")
conn.commit()


class AccessDenied(Exception):
    pass

class Patient:
    def __init__(self, name, age, disease, status):
        self.name = name
        self.age = age
        self.disease = disease
        self.status = status

    def save(self):
        cur.execute(
            "INSERT INTO patients(name,age,disease,status) VALUES(?,?,?,?)",
            (self.name, self.age, self.disease, self.status)
        )
        conn.commit()


class Billing:
    def __init__(self, amount):
        self.amount = amount

    def calculate(self):
        tax = self.amount * 0.05
        total = self.amount + tax
        return tax, total

    def save_invoice(self, pid, amount, tax, total):
        cur.execute(
            "INSERT INTO billing(pid,amount,tax,total) VALUES(?,?,?,?)",
            (pid, amount, tax, total)
        )
        conn.commit()

        with open(f"invoices/invoice_{pid}.txt", "w") as f:
            f.write(f"Patient ID: {pid}\nAmount: {amount}\nTax: {tax}\nTotal: {total}")

def regex_search(pattern):
    cur.execute("SELECT * FROM patients")
    data = cur.fetchall()
    return [p for p in data if re.search(pattern, p[3], re.IGNORECASE)]


class MediTrackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MediTrack Login")
        self.login_screen()

    def login_screen(self):
        tk.Label(self.root, text="Username").pack()
        self.username = tk.Entry(self.root)
        self.username.pack()

        tk.Label(self.root, text="Password").pack()
        self.password = tk.Entry(self.root, show="*")
        self.password.pack()

        tk.Button(self.root, text="Login", command=self.login).pack()

    def login(self):
        user = self.username.get()
        pwd = self.password.get()

        cur.execute("SELECT role FROM users WHERE username=? AND password=?", (user, pwd))
        result = cur.fetchone()

        if result:
            self.role = result[0]
            self.dashboard()
        else:
            messagebox.showerror("Error", "Invalid Login")

    def dashboard(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("MediTrack Dashboard")

        tk.Label(self.root, text=f"Role: {self.role}").pack()

        if self.role in ["Admin", "Receptionist"]:
            tk.Button(self.root, text="Add Patient", command=self.add_patient).pack()

        tk.Button(self.root, text="Search Follow-up Patients", command=self.search_followup).pack()

    def add_patient(self):
        win = tk.Toplevel(self.root)
        win.title("Add Patient")

        name = tk.Entry(win)
        age = tk.Entry(win)
        disease = tk.Entry(win)
        status = tk.Entry(win)

        for lbl in ["Name", "Age", "Disease", "Status"]:
            tk.Label(win, text=lbl).pack()

        name.pack()
        age.pack()
        disease.pack()
        status.pack()

        def save():
            try:
                p = Patient(name.get(), int(age.get()), disease.get(), status.get())
                p.save()
                messagebox.showinfo("Success", "Patient Added")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(win, text="Save", command=save).pack()

    def search_followup(self):
        results = regex_search("Follow")
        msg = "\n".join([f"{r[1]} - {r[4]}" for r in results])
        messagebox.showinfo("Follow-up Patients", msg if msg else "No Records")


if __name__ == "__main__":
    root = tk.Tk()
    app = MediTrackApp(root)
    root.mainloop()