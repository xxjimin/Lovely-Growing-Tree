import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hll import get_connection

def list_trees_by_username(username):
    """사용자의 트리 목록 출력"""
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

def list_ornaments_by_tree_id(tree_id):
    """트리 ID로 오너먼트 목록 출력"""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
            SELECT o.ornament_id, o.position_x, o.position_y, l.content AS letter_content
            FROM Ornaments o
            JOIN Letters l ON o.letter_id = l.letter_id
            WHERE o.tree_id = %s
            """
            cursor.execute(sql, (tree_id,))
            ornaments = cursor.fetchall()

            if not ornaments:
                print(f"No ornaments found for Tree ID {tree_id}.")
                return []

            print(f"\nOrnaments for Tree ID {tree_id}:")
            for ornament in ornaments:
                print(f"Ornament ID: {ornament['ornament_id']}, Position: ({ornament['position_x']}, {ornament['position_y']}), Letter Content: {ornament['letter_content']}")

            return ornaments
    except Exception as e:
        print(f"Error fetching ornaments: {e}")
        return []
    finally:
        connection.close()

if __name__ == "__main__":
    username = input("Enter your username: ")
    trees = list_trees_by_username(username)

    if trees:
        try:
            tree_id = int(input("\nEnter the Tree ID to view its ornaments: "))
            # 선택된 Tree ID가 유효한지 확인
            valid_tree_ids = [tree['tree_id'] for tree in trees]
            if tree_id in valid_tree_ids:
                list_ornaments_by_tree_id(tree_id)
            else:
                print("Invalid Tree ID. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid Tree ID.")
