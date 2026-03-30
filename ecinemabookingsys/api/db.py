import pymysql
import bcrypt

def get_db():
    return pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="mysqlpass",
        database="cinemaebooking",
        cursorclass=pymysql.cursors.DictCursor
    )

#Validate Login Credentials. Parameters are email and password typed by the user.
def validate_login(username_email, provided_password):
    conn = get_db()
    user = None
    try:
        with conn.cursor() as cursor:
            #Look for user by username or email
            cursor.execute("SELECT * FROM User WHERE username = %s OR email = %s", (username_email, username_email))
            user = cursor.fetchone()
    finally:
        conn.close()

    #If the user exists, check the password
    if user:
        #The stored password in the database
        stored_hash = user['password']
        #Check to see if the password is bcrypt hashed
        if stored_hash.startswith('$2b$') or stored_hash.startswith('$2a$'):
            #Rehash provided_password (user typed password). If it matches the db-stored hashed password (stored_password)'s salt, credentials were correct.
            if bcrypt.checkpw(provided_password.encode('utf-8'), stored_hash.encode('utf-8')):
                return user
        elif stored_hash == provided_password:
            return user

    #If either do not work, return null.
    return None
    
#Check if user is currently logged in
def is_logged_in(user_id):
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("SELECT account_status FROM User WHERE user_id = %s", (user_id,))
        status = cursor.fetchone()
    conn.close()
    if status and status['account_status'] == "Active":
        return True
    else:
        return False