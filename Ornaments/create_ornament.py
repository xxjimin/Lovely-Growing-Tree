import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hll import get_connection

def list_trees_by_username(username):
    """사용자(username)의 트리 목록을 출력"""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
            SELECT t.tree_id, t.tree_name
            FROM Trees t
            JOIN Users u ON t.user_id = u.user_id
            WHERE u.username = %s
            """
            cursor.execute(sql, (username,))
            trees = cursor.fetchall()

            if not trees:
                print(f"No trees found for username '{username}'.")
                return []

            print(f"\nTrees for user '{username}':")
            for tree in trees:
                print(f"Tree ID: {tree['tree_id']}, Tree Name: {tree['tree_name']}")

            return trees
    except Exception as e:
        print(f"Error fetching trees: {e}")
        return []
    finally:
        connection.close()

def list_letters_by_tree_id(tree_id):
    """트리(tree_id)에 연결된 편지 목록을 출력"""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT letter_id, content, author_name FROM Letters WHERE tree_id = %s"
            cursor.execute(sql, (tree_id,))
            letters = cursor.fetchall()

            if not letters:
                print(f"No letters found for Tree ID {tree_id}.")
                return []

            print(f"\nLetters for Tree ID {tree_id}:")
            for letter in letters:
                print(f"Letter ID: {letter['letter_id']}, Content: {letter['content']}, Author: {letter['author_name']}")

            return letters
    except Exception as e:
        print(f"Error fetching letters: {e}")
        return []
    finally:
        connection.close()

def create_ornament(tree_id, letter_id, position_x, position_y):
    """Ornament 추가"""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO Ornaments (tree_id, letter_id, position_x, position_y) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (tree_id, letter_id, position_x, position_y))
            connection.commit()
            print(f"Ornament has been added to Tree ID {tree_id} at position ({position_x}, {position_y})!")
    except Exception as e:
        print(f"Error adding ornament: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    username = input("Enter your username: ")
    trees = list_trees_by_username(username)

    if trees:
        try:
            tree_id = int(input("\nEnter the Tree ID to add an ornament: "))
            # 선택한 tree_id가 유효한지 확인
            valid_tree_ids = [tree['tree_id'] for tree in trees]
            if tree_id in valid_tree_ids:
                letters = list_letters_by_tree_id(tree_id)
                if letters:
                    letter_id = int(input("\nEnter the Letter ID to link as an ornament: "))
                    # 선택한 letter_id가 유효한지 확인
                    valid_letter_ids = [letter['letter_id'] for letter in letters]
                    if letter_id in valid_letter_ids:
                        position_x = float(input("Enter X Position: "))
                        position_y = float(input("Enter Y Position: "))
                        create_ornament(tree_id, letter_id, position_x, position_y)
                    else:
                        print("Invalid Letter ID. Please try again.")
                else:
                    print("No letters available for the selected tree.")
            else:
                print("Invalid Tree ID. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid ID.")
