import sqlite3

# Connect to the database
conn = sqlite3.connect('database.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# SQL statements to delete all records from each table
cursor.execute('DELETE FROM image')
cursor.execute('DELETE FROM journal')
cursor.execute('DELETE FROM goals')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("All records deleted successfully.")