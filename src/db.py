import datetime
import sqlite3


def create_database():
    conn = sqlite3.connect("ci.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY,commit_hash TEXT, date TEXT, logs TEXT)")
    conn.commit()
    conn.close()


# Function to add row of history to the SQLite database
def insert_row(commit_hash, logs):
    conn = sqlite3.connect("ci.db")
    cursor = conn.cursor()
    date = datetime.now().strftime("%Y-%M-%D %H:%M:%S")
    cursor.execute("INSERT INTO history (commit_hash, date, logs) VALUES (?, ?, ?)",
        (commit_hash, date, logs),
    )
    conn.commit()
    conn.close()
    
if __name__ == "__main__":
    create_database()
