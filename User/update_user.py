import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hll import get_connection

def update_username_by_username(old_username, new_username):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # 기존 username을 통해 user_id를 조회
            cursor.execute("SELECT user_id FROM Users WHERE username = %s", (old_username,))
            user = cursor.fetchone()

            if not user:
                print(f"User with username '{old_username}' does not exist.")
                return

            # user_id를 통해 username 업데이트
            cursor.execute("UPDATE Users SET username = %s WHERE user_id = %s", (new_username, user['user_id']))
            connection.commit()

            print(f"Username for user '{old_username}' has been updated to '{new_username}'!")
    except Exception as e:
        print(f"Error updating username: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    old_username = input("Enter the current username to update: ")
    new_username = input("Enter new username: ")
    update_username_by_username(old_username, new_username)
