import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hll import get_connection

def list_trees_by_username(username):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # `user_id`를 `username`으로 찾고 해당 `user_id`로 트리 목록 조회
            sql = """
            SELECT t.tree_id, t.tree_name, t.created_at
            FROM Trees t
            JOIN Users u ON t.user_id = u.user_id
            WHERE u.username = %s
            """
            cursor.execute(sql, (username,))
            trees = cursor.fetchall()
            print(f"Tree List for {username}:")
            for tree in trees:
                print(f"ID: {tree['tree_id']}, Name: {tree['tree_name']}, Created At: {tree['created_at']}")
    except Exception as e:
        print(f"Error fetching trees: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    username = input("Enter Username: ")
    list_trees_by_username(username)
