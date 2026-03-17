import sqlite3

def check_users():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT fname, email, password FROM qrcus_registration")
        users = cursor.fetchall()
        print("Existing Users (fname, email, password):")
        for user in users:
            print(user)
    except sqlite3.OperationalError as e:
        print(f"Error: {e}")
    conn.close()

if __name__ == "__main__":
    check_users()
