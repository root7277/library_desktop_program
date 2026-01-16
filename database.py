import sqlite3

def connect_db():
    return sqlite3.connect("library.db")

def create_db():
    conn = connect_db()
    cursor = conn.cursor()
    # Kitoblar jadvali
    cursor.execute('''CREATE TABLE IF NOT EXISTS Books (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT, author TEXT, year TEXT, genre TEXT, status TEXT DEFAULT 'Mavjud')''')
    # Foydalanuvchilar jadvali
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT, phone TEXT)''')
    # Qarz berish jadvali
    cursor.execute('''CREATE TABLE IF NOT EXISTS Borrow (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        book_id INTEGER, user_id INTEGER, date TEXT, returned INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

def add_book(name, author, year, genre):
    conn = connect_db()
    conn.execute("INSERT INTO Books (name, author, year, genre) VALUES (?, ?, ?, ?)", (name, author, year, genre))
    conn.commit()
    conn.close()

def add_user(name, phone):
    conn = connect_db()
    conn.execute("INSERT INTO Users (name, phone) VALUES (?, ?)", (name, phone))
    conn.commit()
    conn.close()

def borrow_book(book_id, user_id, date):
    conn = connect_db()
    conn.execute("INSERT INTO Borrow (book_id, user_id, date) VALUES (?, ?, ?)", (book_id, user_id, date))
    conn.execute("UPDATE Books SET status='Qarzda' WHERE id=?", (book_id,))
    conn.commit()
    conn.close()

def return_book_db(book_id):
    conn = connect_db()
    conn.execute("UPDATE Borrow SET returned=1 WHERE book_id=? AND returned=0", (book_id,))
    conn.execute("UPDATE Books SET status='Mavjud' WHERE id=?", (book_id,))
    conn.commit()
    conn.close()

def fetch_data(table):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    conn.close()
    return rows