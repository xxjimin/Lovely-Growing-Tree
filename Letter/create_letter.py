import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hll import get_connection

def create_letter_by_username(username, content, author_name):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # `username`으로 해당 `tree_id` 찾기
            sql = """
            SELECT t.tree_id
            FROM Trees t
            JOIN Users u ON t.user_id = u.user_id
            WHERE u.username = %s
            """
            cursor.execute(sql, (username,))
            tree = cursor.fetchone()

            if tree:
                tree_id = tree['tree_id']
                
                # `Letters` 테이블에 데이터 삽입
                insert_sql = "INSERT INTO Letters (tree_id, content, author_name, username) VALUES (%s, %s, %s, %s)"
                cursor.execute(insert_sql, (tree_id, content, author_name, username))
                connection.commit()
                print(f"Letter added successfully to Tree with ID {tree_id} by {author_name}!")
            else:
                print(f"No tree found for username '{username}'")
    except Exception as e:
        print(f"Error adding letter: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    username = input("Enter Username: ")
    content = input("Enter Letter Content: ")
    author_name = input("Enter Author Name: ")
    create_letter_by_username(username, content, author_name)
