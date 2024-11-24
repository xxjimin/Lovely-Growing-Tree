import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hll import get_connection

def create_tree(tree_name, username):
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

            # Tree 생성
            sql = "INSERT INTO Trees (tree_name, user_id) VALUES (%s, %s)"
            cursor.execute(sql, (tree_name, user_id))
            connection.commit()
            print(f"Tree '{tree_name}' for user '{username}' has been created successfully!")
    except Exception as e:
        print(f"Error creating tree: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    tree_name = input("Enter Tree Name: ")
    username = input("Enter Username: ")
    create_tree(tree_name, username)
