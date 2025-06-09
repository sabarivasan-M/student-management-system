# Student Management System with Dark Theme, Validation, PDF & Excel Export

try:
    from tkinter import *
    from tkinter import ttk, messagebox
except ImportError:
    raise ImportError("Tkinter is not available. Please make sure it is installed and supported in your environment.")

import pymysql
from reportlab.pdfgen import canvas
from openpyxl import Workbook
import re

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'ms@2007',
    'database': 'stud1'
}

class Student:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1350x690+1+1')
        self.root.title('Student Management System')
        self.root.configure(background="#2E2E2E")
        self.root.resizable(False, False)

        title = Label(self.root, text='Student Management System', bg='#1C1C1C', font=('monospace', 14), fg='#00FF00')
        title.pack(fill=X)

        self.id_var = StringVar()
        self.name_var = StringVar()
        self.email_var = StringVar()
        self.phone_var = StringVar()
        self.moahel_var = StringVar()
        self.gender_var = StringVar()
        self.address_var = StringVar()
        self.dell_var = StringVar()
        self.se_var = StringVar()
        self.se_by = StringVar()

        manage_frame = Frame(self.root, bg='#333333')
        manage_frame.place(x=1137, y=30, width=210, height=460)

        self.add_label_entry(manage_frame, 'Student ID', self.id_var, fg='#FFD700')
        self.add_label_entry(manage_frame, 'Student Name', self.name_var, fg='#FFD700')
        self.add_label_entry(manage_frame, 'Student Email', self.email_var, fg='#FFD700')
        self.add_label_entry(manage_frame, 'Student Phone', self.phone_var, fg='#FFD700')

        self.add_label_combobox(manage_frame, 'Educational Level', self.moahel_var, ['Elementary', 'Preparatory', 'Secondary'])
        self.add_label_combobox(manage_frame, 'Student Gender', self.gender_var, ['male', 'female'])
        self.add_label_entry(manage_frame, 'Student Address', self.address_var, fg='#FFD700')
        self.add_label_entry(manage_frame, 'Delete By Name', self.dell_var, fg='#FF0000')

        btn_frame = Frame(self.root, bg='#333333')
        btn_frame.place(x=1137, y=500, width=210, height=185)

        title1 = Label(btn_frame, text='Control Buttons', font=('Deco', 14), fg='#00FFFF', bg='#1C1C1C')
        title1.pack(fill=X)

        Button(btn_frame, text='Add', bg='#4CAF50', fg='white', command=self.add_student).pack(pady=5, fill=X)
        Button(btn_frame, text='Delete', bg='#f44336', fg='white', command=self.delete).pack(pady=5, fill=X)
        Button(btn_frame, text='Update', bg='#2196F3', fg='white', command=self.update).pack(pady=5, fill=X)
        Button(btn_frame, text='Clear', bg='#FF9800', fg='white', command=self.clear).pack(pady=5, fill=X)
        Button(btn_frame, text='Export PDF', bg='#9C27B0', fg='white', command=self.export_pdf).pack(pady=5, fill=X)
        Button(btn_frame, text='Export Excel', bg='#795548', fg='white', command=self.export_to_excel).pack(pady=5, fill=X)
        Button(btn_frame, text='Exit', bg='#607D8B', fg='white', command=root.quit).pack(pady=5, fill=X)

        search_Frame = Frame(self.root, bg='#333333')
        search_Frame.place(x=1, y=30, width=1134, height=50)

        Label(search_Frame, text='Searching Bar', bg='#333333', fg='#00FF00').place(x=1034, y=12)
        combo_search = ttk.Combobox(search_Frame, textvariable=self.se_by)
        combo_search['value'] = ('id', 'name', 'email', 'phone')
        combo_search.place(x=880, y=12)

        Entry(search_Frame, textvariable=self.se_var, bd='2').place(x=750, y=12)
        Button(search_Frame, text='search', bg='white', command=self.search).place(x=630, y=12, width=100, height=25)

        Dietals_Frame = Frame(self.root, bg='white')
        Dietals_Frame.place(x=1, y=82, width=1134, height=605)

        scroll_x = Scrollbar(Dietals_Frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(Dietals_Frame, orient=VERTICAL)

        self.student_table = ttk.Treeview(Dietals_Frame,
            columns=('address', 'gender', 'certi', 'email', 'phone', 'name', 'id'),
            xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        self.student_table.place(x=18, y=1, width=1130, height=587)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=LEFT, fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        for col in ('address', 'gender', 'certi', 'email', 'phone', 'name', 'id'):
            self.student_table.heading(col, text=col.replace('_', ' ').title())
            self.student_table.column(col, width=100)

        self.student_table['show'] = 'headings'
        self.student_table.bind("<ButtonRelease-1>", self.get_cursor)
        self.fetch_all()

    def add_label_entry(self, frame, text, var, fg='black'):
        Label(frame, text=text, bg='#333333', fg=fg).pack()
        Entry(frame, textvariable=var, bd=2).pack()

    def add_label_combobox(self, frame, text, var, values):
        Label(frame, text=text, bg='#333333', fg='white').pack()
        combo = ttk.Combobox(frame, textvariable=var)
        combo['value'] = values
        combo.pack()

    def validate_inputs(self):
        if not all([self.id_var.get(), self.name_var.get(), self.email_var.get(), self.phone_var.get()]):
            messagebox.showerror("Input Error", "Please fill in all required fields.")
            return False
        if not self.phone_var.get().isdigit() or len(self.phone_var.get()) != 10:
            messagebox.showerror("Phone Error", "Enter a valid 10-digit phone number.")
            return False
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email_var.get()):
            messagebox.showerror("Email Error", "Enter a valid email address.")
            return False
        return True

    def add_student(self):
        if not self.validate_inputs():
            return
        con = pymysql.connect(**DB_CONFIG)
        cur = con.cursor()
        cur.execute("insert into student values(%s,%s,%s,%s,%s,%s,%s)",
                    (self.address_var.get(), self.gender_var.get(), self.moahel_var.get(),
                     self.email_var.get(), self.phone_var.get(), self.name_var.get(), self.id_var.get()))
        con.commit()
        con.close()
        self.fetch_all()
        self.clear()
        messagebox.showinfo("Success", "Student record added successfully!")

    def fetch_all(self):
        con = pymysql.connect(**DB_CONFIG)
        cur = con.cursor()
        cur.execute('select * from student')
        rows = cur.fetchall()
        self.student_table.delete(*self.student_table.get_children())
        for row in rows:
            self.student_table.insert("", END, values=row)
        con.close()

    def delete(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to delete?"):
            con = pymysql.connect(**DB_CONFIG)
            cur = con.cursor()
            cur.execute('delete from student where name=%s', self.dell_var.get())
            con.commit()
            con.close()
            self.fetch_all()

    def clear(self):
        for var in [self.id_var, self.name_var, self.email_var, self.phone_var, self.address_var, self.moahel_var, self.gender_var]:
            var.set('')

    def get_cursor(self, ev):
        row = self.student_table.item(self.student_table.focus())['values']
        if row:
            self.id_var.set(row[6])
            self.name_var.set(row[5])
            self.phone_var.set(row[4])
            self.email_var.set(row[3])
            self.moahel_var.set(row[2])
            self.gender_var.set(row[1])
            self.address_var.set(row[0])

    def update(self):
        if not self.validate_inputs():
            return
        con = pymysql.connect(**DB_CONFIG)
        cur = con.cursor()
        cur.execute("update student set address=%s, gender=%s, moahel=%s, email=%s, phone=%s, name=%s where id=%s ",
                    (self.address_var.get(), self.gender_var.get(), self.moahel_var.get(),
                     self.email_var.get(), self.phone_var.get(), self.name_var.get(), self.id_var.get()))
        con.commit()
        con.close()
        self.fetch_all()
        self.clear()
        messagebox.showinfo("Success", "Record updated successfully!")

    def search(self):
        con = pymysql.connect(**DB_CONFIG)
        cur = con.cursor()
        cur.execute(f"select * from student where {self.se_by.get()} LIKE '%{self.se_var.get()}%'")
        rows = cur.fetchall()
        self.student_table.delete(*self.student_table.get_children())
        for row in rows:
            self.student_table.insert("", END, values=row)
        con.close()

    def export_pdf(self):
        c = canvas.Canvas("Student_Report.pdf")
        c.drawString(100, 800, "Student Report")
        y = 780
        for row in self.student_table.get_children():
            data = self.student_table.item(row)['values']
            c.drawString(100, y, ", ".join(map(str, data)))
            y -= 20
        c.save()
        messagebox.showinfo("Exported", "PDF has been created.")

    def export_to_excel(self):
        wb = Workbook()
        ws = wb.active
        ws.append(['Address', 'Gender', 'Education', 'Email', 'Phone', 'Name', 'ID'])
        for row in self.student_table.get_children():
            data = self.student_table.item(row)['values']
            ws.append(data)
        wb.save("Student_Backup.xlsx")
        messagebox.showinfo("Exported", "Backup saved to Excel.")


root = Tk()
ob = Student(root)
root.mainloop()
