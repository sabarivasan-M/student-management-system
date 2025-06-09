# student-management-system


---

## 📘 `README.md`

```markdown
# 🎓 Student Management System  
*“A well-organized student is a well-prepared future.”*

---

## 🌟 Overview

This Python-based **Student Management System** is a full-featured desktop GUI application that helps manage student records with elegance. With a sleek **dark theme**, real-time **input validation**, and powerful **PDF & Excel export** functionality, this system transforms administrative tasks into a seamless experience.

Built using **Tkinter** for GUI, **MySQL** for backend storage, and powered by a graceful blend of structure and simplicity.

---

## ✨ Features

- 🔒 Input validation with meaningful alerts  
- 🌙 Dark-themed interface for eye comfort  
- 📄 Export student records as **PDF**  
- 📊 Backup records as **Excel (XLSX)**  
- 🔎 Smart search functionality by ID, Name, Email, or Phone  
- ✍️ Add, Update, Delete, and View student details  

---

## 🏗️ Technologies Used

- Python 3  
- Tkinter (GUI)  
- MySQL (Database)  
- Pymysql (Connector)  
- Openpyxl (Excel export)  
- ReportLab (PDF generation)  

---

## 📂 Project Structure

```

student-management-system/

├── student.py             # Main GUI script


├── requirements.txt       # Python dependencies


└── README.md              # Project documentation

````

---

## ⚙️ Setup Instructions

### 📥 Clone the Repository

```bash
git clone https://github.com/your-username/student-management-system.git
cd student-management-system
````

### 🧪 Install Dependencies

```bash
pip install -r requirements.txt
```

### 🗄️ MySQL Database Setup

Make sure you have a MySQL server running.

Create a database and table:

```sql
CREATE DATABASE stud1;
USE stud1;

CREATE TABLE student (
  address VARCHAR(100),
  gender VARCHAR(10),
  moahel VARCHAR(50),
  email VARCHAR(100),
  phone VARCHAR(15),
  name VARCHAR(50),
  id VARCHAR(20) PRIMARY KEY
);
```

> ✅ **Update your MySQL credentials** in `student.py` if different from:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'ms@2007',
    'database': 'stud1'
}
```

---

## 🧾 requirements.txt

```txt
tk
pymysql
reportlab
openpyxl
```

Install using:

```bash
pip install -r requirements.txt
```

---

## 🎮 Run the App

```bash
python student.py
```

---

## 🖼️ Screenshots (Optional)

> *(Add screenshots of your GUI here if you'd like to show the interface)*

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).

---

## ✍️ Author

**Sabarivasan**
*“Code is not just logic — it's the language of possibility.”*

Feel free to ⭐ star, fork, or contribute!

---

```

---

Would you like me to create `.gitignore` or a GitHub banner image to complete your repo’s presentation?  
Let me know, and I’ll help you upload everything beautifully 🌱
```
