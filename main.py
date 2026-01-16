import tkinter as tk
from tkinter import messagebox, ttk
import database
from datetime import datetime

# Ranglar palitrasi
COLORS = {
    "primary": "#2c3e50", "secondary": "#34495e", "accent": "#3498db",
    "bg": "#ecf0f1", "text": "#2c3e50", "white": "#ffffff", "green": "#27ae60"
}

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kutubxona Avtomatlashtirish Tizimi")
        self.root.geometry("1000x650")
        self.root.configure(bg=COLORS["bg"])
        database.create_db()
        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=COLORS["white"], rowheight=30, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))

    def create_widgets(self):
        # YON PANEL (SIDEBAR)
        self.side_frame = tk.Frame(self.root, bg=COLORS["primary"], width=250)
        self.side_frame.pack(side="left", fill="y")
        
        tk.Label(self.side_frame, text="LIBRARY PRO", fg="white", bg=COLORS["primary"], 
                 font=("Segoe UI", 18, "bold"), pady=30).pack()

        self.create_nav_button("📚 Kitoblar", self.show_books)
        self.create_nav_button("👥 Foydalanuvchilar", self.show_users)
        self.create_nav_button("🔄 Kitob Berish/Qaytarish", self.show_borrow)

        # ASOSIY MAYDON
        self.main_frame = tk.Frame(self.root, bg=COLORS["bg"], padx=20, pady=20)
        self.main_frame.pack(side="right", fill="both", expand=True)
        self.show_books()

    def create_nav_button(self, text, command):
        btn = tk.Button(self.side_frame, text=text, command=command, bg=COLORS["secondary"], 
                        fg="white", bd=0, font=("Segoe UI", 12), pady=12, cursor="hand2")
        btn.pack(fill="x", padx=10, pady=5)

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # --- KITOBLAR BO'LIMI ---
    def show_books(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Kitoblar Ombori", font=("Segoe UI", 20, "bold"), bg=COLORS["bg"]).pack(anchor="w")
        
        table_frame = tk.Frame(self.main_frame)
        table_frame.pack(fill="both", expand=True, pady=10)

        cols = ("ID", "Nomi", "Muallif", "Janri", "Holati")
        tree = ttk.Treeview(table_frame, columns=cols, show="headings")
        for col in cols: tree.heading(col, text=col)
        
        for row in database.fetch_data("Books"):
            tree.insert("", "end", values=(row[0], row[1], row[2], row[4], row[5]))
        tree.pack(fill="both", expand=True)
        
        tk.Button(self.main_frame, text="+ Kitob Qo'shish", command=self.add_book_ui, 
                  bg=COLORS["green"], fg="white", font=("Segoe UI", 11, "bold"), pady=10).pack()

    def add_book_ui(self):
        win = tk.Toplevel()
        win.title("Yangi Kitob")
        win.geometry("300x400")
        
        labels = ["Nomi", "Muallif", "Yil", "Janr"]
        entries = {}
        for lab in labels:
            tk.Label(win, text=lab).pack()
            e = tk.Entry(win); e.pack(pady=5); entries[lab] = e
            
        def save():
            if entries["Nomi"].get():
                database.add_book(entries["Nomi"].get(), entries["Muallif"].get(), entries["Yil"].get(), entries["Janr"].get())
                win.destroy(); self.show_books()
            else:
                messagebox.showwarning("Xato", "Kitob nomini kiriting!")
        tk.Button(win, text="Saqlash", command=save, bg=COLORS["accent"], fg="white").pack(pady=20)

    # --- FOYDALANUVCHILAR BO'LIMI ---
    def show_users(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Foydalanuvchilar", font=("Segoe UI", 20, "bold"), bg=COLORS["bg"]).pack(anchor="w")
        
        table_frame = tk.Frame(self.main_frame)
        table_frame.pack(fill="both", expand=True, pady=10)

        cols = ("ID", "Ismi", "Telefon")
        tree = ttk.Treeview(table_frame, columns=cols, show="headings")
        for col in cols: tree.heading(col, text=col)
        
        for row in database.fetch_data("Users"):
            tree.insert("", "end", values=(row[0], row[1], row[2]))
        tree.pack(fill="both", expand=True)

        tk.Button(self.main_frame, text="+ Foydalanuvchi Qo'shish", command=self.add_user_ui, 
                  bg=COLORS["green"], fg="white", font=("Segoe UI", 11, "bold"), pady=10).pack()

    def add_user_ui(self):
        win = tk.Toplevel()
        win.title("Yangi Foydalanuvchi")
        tk.Label(win, text="Ismi:").pack(); name_e = tk.Entry(win); name_e.pack()
        tk.Label(win, text="Tel:").pack(); phone_e = tk.Entry(win); phone_e.pack()
        
        def save():
            if name_e.get():
                database.add_user(name_e.get(), phone_e.get())
                win.destroy(); self.show_users()
            else:
                messagebox.showwarning("Xato", "Ismni kiriting!")
        tk.Button(win, text="Saqlash", command=save, bg=COLORS["accent"], fg="white").pack(pady=10)

    # --- QARZ BERISH VA QAYTARISH ---
    def show_borrow(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Kitob Operatsiyalari", font=("Segoe UI", 20, "bold"), bg=COLORS["bg"]).pack(anchor="w")

        # Berish qismi
        f1 = tk.LabelFrame(self.main_frame, text="Kitob Berish (ID orqali)", padx=10, pady=10)
        f1.pack(fill="x", pady=10)
        tk.Label(f1, text="Kitob ID:").grid(row=0, column=0); b_id = tk.Entry(f1); b_id.grid(row=0, column=1)
        tk.Label(f1, text="User ID:").grid(row=0, column=2); u_id = tk.Entry(f1); u_id.grid(row=0, column=3)
        
        def give():
            if b_id.get() and u_id.get():
                database.borrow_book(b_id.get(), u_id.get(), datetime.now().strftime("%Y-%m-%d"))
                messagebox.showinfo("OK", "Kitob berildi!"); self.show_books()
            else:
                messagebox.showerror("Xato", "ID raqamlarini kiriting!")
        tk.Button(f1, text="Tasdiqlash", command=give, bg="orange", fg="white").grid(row=0, column=4, padx=10)

        # Qaytarish qismi
        f2 = tk.LabelFrame(self.main_frame, text="Kitobni Qaytarib olish", padx=10, pady=10)
        f2.pack(fill="x", pady=10)
        tk.Label(f2, text="Kitob ID:").grid(row=0, column=0); ret_id = tk.Entry(f2); ret_id.grid(row=0, column=1)
        
        def ret():
            if ret_id.get():
                database.return_book_db(ret_id.get())
                messagebox.showinfo("OK", "Kitob qaytarib olindi!"); self.show_books()
            else:
                messagebox.showerror("Xato", "Kitob ID-sini kiriting!")
        tk.Button(f2, text="Qaytarish", command=ret, bg="lightblue").grid(row=0, column=2, padx=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()