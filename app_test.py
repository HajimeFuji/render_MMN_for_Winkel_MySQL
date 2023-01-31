import mysql.connector

cnx = None

try:
    cnx = mysql.connector.connect(
        user='HajimeFujii',  # ユーザー名
        password='04fujkan11',  # パスワード
        host='localhost'  # ホスト名(IPアドレス）
    )

    sql = ("DROP DATABASE test")
    cursor.execute(sql)

    cursor.execute("SHOW DATABASES")
    print(cursor.fetchall())

    cursor.close()

except Exception as e:
    print(f"Error Occurred: {e}")

finally:
    if cnx is not None and cnx.is_connected():
        cnx.close()