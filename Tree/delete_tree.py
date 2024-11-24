import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hll import get_connection

def delete_tree_by_username(username, tree_name):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # username을 통해 user_id 가져오기
            cursor.execute("SELECT user_id FROM Users WHERE username = %s", (username,))
            user = cursor.fetchone()

            if not user:
                print(f"User with username '{username}' does not exist.")
                return

            user_id = user['user_id']

            # 해당 user_id와 tree_name에 해당하는 트리 삭제
            cursor.execute("DELETE FROM Ornaments WHERE tree_id IN (SELECT tree_id FROM Trees WHERE user_id = %s AND tree_name = %s)", (user_id, tree_name))
            cursor.execute("DELETE FROM Letters WHERE tree_id IN (SELECT tree_id FROM Trees WHERE user_id = %s AND tree_name = %s)", (user_id, tree_name))
            cursor.execute("DELETE FROM Trees WHERE user_id = %s AND tree_name = %s", (user_id, tree_name))

            connection.commit()
            print(f"Tree '{tree_name}' for user '{username}' has been deleted successfully!")
    except Exception as e:
        print(f"Error deleting tree: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    username = input("Enter Username: ")
    tree_name = input("Enter Tree Name to delete: ")
    delete_tree_by_username(username, tree_name)
