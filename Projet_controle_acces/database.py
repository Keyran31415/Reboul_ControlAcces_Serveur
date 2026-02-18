import pymysql

def get_connection():
    try:
        connection = pymysql.connect(
            host="mysql-key314.alwaysdata.net",
            user="key314_controle_acces",
            password="Key31415",
            database="key314_controle_acces",
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.MySQLError as e:
        print("Erreur MySQL :", e)
        return None