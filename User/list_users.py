import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hll import get_connection

def list_users():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Users")
            users = cursor.fetchall()
            print("User List:")
            for user in users:
                print(f"ID: {user['user_id']}, Name: {user['username']}, Created At: {user['created_at']}")
    except Exception as e:
        print(f"Error fetching users: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    list_users()
