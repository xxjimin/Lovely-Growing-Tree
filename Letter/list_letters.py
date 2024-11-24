import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hll import get_connection

def list_letters_by_username(username):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # username으로 트리 정보 가져오기
            tree_query = """
            SELECT t.tree_id, t.tree_name
            FROM Trees t
            JOIN Users u ON t.user_id = u.user_id
            WHERE u.username = %s
            """
            cursor.execute(tree_query, (username,))
            trees = cursor.fetchall()

            if not trees:
                print(f"No trees found for username '{username}'.")
                return

            # 트리 목록 출력
            print(f"\nTrees for user '{username}':")
            for tree in trees:
                print(f"Tree ID: {tree['tree_id']}, Tree Name: {tree['tree_name']}")

            # 트리를 선택하도록 요청
            tree_id = int(input("\nEnter the Tree ID to list its letters: "))

            # 선택된 트리의 편지 목록 가져오기
            letter_query = "SELECT * FROM Letters WHERE tree_id = %s"
            cursor.execute(letter_query, (tree_id,))
            letters = cursor.fetchall()

            if not letters:
                print(f"No letters found for Tree ID {tree_id}.")
                return

            # 편지 목록 출력
            print(f"\nLetters for Tree ID {tree_id}:")
            for letter in letters:
                print(f"ID: {letter['letter_id']}, Content: {letter['content']}, Author: {letter['author_name']}, Status: {letter['status']}")
    except Exception as e:
        print(f"Error fetching letters: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    username = input("Enter your username: ")
    list_letters_by_username(username)
