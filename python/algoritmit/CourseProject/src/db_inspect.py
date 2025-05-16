"""
File : db_inspect.py
Author : Daniel Kortesmaa
Description : Inspects the contents of the db.
"""

import sqlite3

def query_database():
    conn = sqlite3.connect('data/db/chatbot_training_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM training_data ORDER BY rowid")
    data = cursor.fetchall()
    conn.close()
    return data

data = query_database()

# Print the retrieved data.. could also write to file
for row in data:
    print(row)