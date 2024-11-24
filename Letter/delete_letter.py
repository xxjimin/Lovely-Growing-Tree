import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hll import get_connection

def list_letters_by_username(username):
    """사용자의 모든 편지를 출력"""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # username으로 작성한 편지 목록 가져오기
            sql = "SELECT letter_id, content, created_at FROM Letters WHERE username = %s"
            cursor.execute(sql, (username,))
            letters = cursor.fetchall()
            
            if not letters:
                print(f"No letters found for username '{username}'.")
                return []

            print(f"\nLetters written by {username}:")
            for letter in letters:
                print(f"ID: {letter['letter_id']}, Content: {letter['content']}, Created At: {letter['created_at']}")

            return letters
    except Exception as e:
        print(f"Error fetching letters: {e}")
        return []
    finally:
        connection.close()

def delete_letter(letter_id):
    """편지 삭제"""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Letters WHERE letter_id = %s", (letter_id,))
            connection.commit()
            print(f"Letter with ID {letter_id} has been deleted!")
    except Exception as e:
        print(f"Error deleting letter: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    username = input("Enter your username: ")
    letters = list_letters_by_username(username)

    if letters:
        try:
            letter_id = int(input("\nEnter the Letter ID you want to delete: "))
            # 사용자가 입력한 letter_id가 목록에 존재하는지 확인
            valid_ids = [letter['letter_id'] for letter in letters]
            if letter_id in valid_ids:
                delete_letter(letter_id)
            else:
                print("Invalid Letter ID. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid Letter ID.")
