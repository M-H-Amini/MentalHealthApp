import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('database.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# SQL statement to create the 'image' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS image (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    image_path TEXT,
    sentiment TEXT,
    attention TEXT
)
''')

# SQL statement to create the 'journal' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS journal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    entry TEXT
)
''')

# SQL statement to create the 'goals' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    goal TEXT
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and tables created successfully.")