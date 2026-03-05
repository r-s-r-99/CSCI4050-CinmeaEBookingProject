import pymysql

def get_db():
    return pymysql.connect(
        host="127.0.0.1",
        port=33306,
        user="root",
        password="mysqlpass",
        database="cinemaebooking",
        cursorclass=pymysql.cursors.DictCursor
    )
