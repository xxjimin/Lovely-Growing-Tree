import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hll import get_connection

def delete_user_by_username(username):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # 사용자 ID 가져오기
            cursor.execute("SELECT user_id FROM Users WHERE username = %s", (username,))
            user = cursor.fetchone()

            if not user:
                print(f"User '{username}' does not exist.")
                return

            user_id = user['user_id']

            # 연결된 데이터 삭제
            cursor.execute("DELETE FROM Ornaments WHERE tree_id IN (SELECT tree_id FROM Trees WHERE user_id = %s)", (user_id,))
            cursor.execute("DELETE FROM Letters WHERE tree_id IN (SELECT tree_id FROM Trees WHERE user_id = %s)", (user_id,))
            cursor.execute("DELETE FROM Trees WHERE user_id = %s", (user_id,))

            # 사용자 삭제
            cursor.execute("DELETE FROM Users WHERE user_id = %s", (user_id,))
            connection.commit()
            print(f"User '{username}' and related data have been deleted successfully!")
    except Exception as e:
        print(f"Error deleting user: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    username = input("Enter the username to delete: ")
    delete_user_by_username(username)
