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

#Store registration information in the database with active/inactive status
def registration(username, email, password, first_name, last_name, phone_number):
    conn = get_db()
    try:
        # Hash the entered password using bcrypt
        hashedPW = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        with conn.cursor() as cursor:
            # The account status defaults to inactive until the user confirms their email.
            sql = "INSERT INTO User (username, email, password, first_name, last_name, phone_number, account_status) VALUES (%s, %s, %s, %s, %s, %s, 'Inactive')"
            cursor.execute(sql, (username, email, hashedPW, first_name, last_name, phone_number))
        
        conn.commit()
        return "User Registered Successfully"
    except Exception as e:
        print(f"Error: {e}")
        return "Error"
    finally:
        conn.close()
    
def activate_user(email):
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            # Update the status from Inactive to Active
            sql = "UPDATE User SET account_status = 'Active' WHERE email = %s"
            cursor.execute(sql, (email,))
        conn.commit()
        return True
    except Exception as e:
        print(f" Error: {e}")
        return False
    finally:
        conn.close()

def update_password(email, new_password):
    conn = get_db()
    hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    with conn.cursor() as cursor:
        cursor.execute("UPDATE User SET password = %s WHERE email = %s", (hashed, email))
    conn.commit()
    conn.close()