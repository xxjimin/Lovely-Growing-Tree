import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hll import get_connection



def create_user(username, password):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO Users (username, password) VALUES (%s, %s)"
            cursor.execute(sql, (username, password))
            connection.commit()
            print(f"User '{username}' has been created successfully!")
    except Exception as e:
        print(f"Error creating user: {e}")
    finally:
        connection.close()

# 실행 예시
if __name__ == "__main__":
    username = input("Enter username: ")
    password = input("Enter password: ")
    create_user(username, password)
