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
            FROM tree_tree t
            JOIN tree_user u ON t.user_id = u.user_id
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
    """트리(tree_id)에 연결된 오너먼트 목록을 출력"""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
            SELECT o.ornament_id, o.position_x, o.position_y, l.content AS letter_content
            FROM tree_ornament o
            JOIN tree_letter l ON o.letter_id = l.letter_id
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

def delete_ornament(ornament_id):
    """오너먼트 삭제"""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM tree_ornament WHERE ornament_id = %s", (ornament_id,))
            connection.commit()
            print(f"Ornament with ID {ornament_id} has been deleted!")
    except Exception as e:
        print(f"Error deleting ornament: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    username = input("Enter your username: ")
    trees = list_trees_by_username(username)

    if trees:
        try:
            tree_id = int(input("\nEnter the Tree ID to view its ornaments: "))
            # 선택한 tree_id가 유효한지 확인
            valid_tree_ids = [tree['tree_id'] for tree in trees]
            if tree_id in valid_tree_ids:
                ornaments = list_ornaments_by_tree_id(tree_id)
                if ornaments:
                    ornament_id = int(input("\nEnter the Ornament ID to delete: "))
                    # 입력한 ornament_id가 유효한지 확인
                    valid_ornament_ids = [ornament['ornament_id'] for ornament in ornaments]
                    if ornament_id in valid_ornament_ids:
                        delete_ornament(ornament_id)
                    else:
                        print("Invalid Ornament ID. Please try again.")
                else:
                    print("No ornaments available for the selected tree.")
            else:
                print("Invalid Tree ID. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid ID.")
