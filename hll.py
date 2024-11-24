import pymysql

def get_connection():
    """MySQL 데이터베이스 연결"""
    return pymysql.connect(
        host="localhost",
        user="root",
        password="rla981226",  # 본인의 MySQL 비밀번호
        database="Lovely_Growing_Tree",  # 데이터베이스 이름
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )
