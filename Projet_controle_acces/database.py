import pymysql

def get_connection():
    try:
        connection = pymysql.connect(
            host="mysql-key314.alwaysdata.net",
            user="key314_securite_nn",
            password="Key31415",
            database="key314_securite_nn",
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.MySQLError as e:
        print("Erreur MySQL :", e)
        return None
