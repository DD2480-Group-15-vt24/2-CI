import sqlite3


def create_database():
    conn = sqlite3.connect("ci.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE history (id INTEGER PRIMARY KEY,commit_hash TEXT, date TEXT, logs TEXT)"
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()
