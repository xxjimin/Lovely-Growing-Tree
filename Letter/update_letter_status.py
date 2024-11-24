import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hll import get_connection

def list_letters_by_username(username):
    """username으로 사용자의 편지 목록을 출력"""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT letter_id, content, status, created_at FROM Letters WHERE username = %s"
            cursor.execute(sql, (username,))
            letters = cursor.fetchall()

            if not letters:
                print(f"No letters found for username '{username}'.")
                return []

            print(f"\nLetters for user '{username}':")
            for letter in letters:
                print(f"ID: {letter['letter_id']}, Content: {letter['content']}, Status: {letter['status']}, Created At: {letter['created_at']}")

            return letters
    except Exception as e:
        print(f"Error fetching letters: {e}")
        return []
    finally:
        connection.close()

def update_letter_status(letter_id, new_status):
    """편지 상태를 업데이트"""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE Letters SET status = %s WHERE letter_id = %s"
            cursor.execute(sql, (new_status, letter_id))
            connection.commit()
            print(f"Letter ID {letter_id} status updated to '{new_status}'!")
    except Exception as e:
        print(f"Error updating letter status: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    username = input("Enter your username: ")
    letters = list_letters_by_username(username)

    if letters:
        try:
            letter_id = int(input("\nEnter the Letter ID to update: "))
            # 입력된 letter_id가 유효한지 확인
            valid_ids = [letter['letter_id'] for letter in letters]
            if letter_id in valid_ids:
                new_status = input("Enter New Status (active/read): ")
                if new_status in ['active', 'read']:
                    update_letter_status(letter_id, new_status)
                else:
                    print("Invalid status. Please enter 'active' or 'read'.")
            else:
                print("Invalid Letter ID. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid Letter ID.")
