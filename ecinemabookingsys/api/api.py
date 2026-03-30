import time
from flask import Flask
from routes.movies import movies_bp
from routes.showtimes import showtimes_bp
from db import get_db, validate_login
from flask import request, jsonify
from db import get_db, validate_login, registration, activate_user, update_password

app = Flask(__name__)

app.register_blueprint(movies_bp)
app.register_blueprint(showtimes_bp)

@app.route('/api/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/api/ping')
def ping():
    conn = get_db()
    conn.close()
    return {'status': 'connected'}


@app.route('/api/login', methods=['POST'])
def login():
    #Get data from frontend
    data = request.json
    email = data.get('email')
    password = data.get('password')

    #Call validate_login notebook function
    user = validate_login(email, password)

    #Login was successful. Send code 200 (OK)
    if user:
        return jsonify({
            "mesage": "Login successful",
            "user": {
                "id": user['user_id'],
                "username": user['username'],
                "role": user['role']
        }
        }), 200 #jsonify
    
    #Otherwise if User is null, send code 401 (Unauthorized)
    return jsonify({"message": "Invalid email or password"}), 401

@app.route('/api/register', methods=['POST'])
def register():
    #Get the data from the frontend
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    phone = data.get('phone')

    #Check if user already exists in database
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM user WHERE username = %s OR email = %s", (username, email))
        if cursor.fetchone():
            conn.close()
            return jsonify({"message": "This username or email is already in use!"}), 400
    conn.close()

    #Call the db.py registration function with this information (from frontend)
    result = registration(username, email, password, first_name, last_name, phone)

    if result == "User Registered Successfully":
        #MOCK SEND EMAIL
        confirm_url = "http://5173/MockEmailConfirm"
        print(f"Confirmation Email Sent to {email}!")
        print(f"Welcome, {first_name}! Click here to activate your account: {confirm_url}")

        return jsonify({
            "message": "Registration Successful! Click here to confirm your email: " + confirm_url
        }), 201

    return jsonify({"message": "Registration failed. Please try again."}), 500

@app.route('/api/confirm', methods=['POST'])
def confirm_email():
    data = request.json
    email = data.get('email')
    
    # Call db function and mark account as Active
    success = activate_user(email)
    
    if success:
        return jsonify({"message": "Account activated successfully!"}), 200
    
    return jsonify({"message": "Activation failed."}), 400

@app.route('/api/forgot-password', methods=['POST'])
def forgot_pass():
    email = request.json.get('email')
    # Mock link
    print(f"Password is being reset for {email}")
    return jsonify({"message": "Link sent to terminal!"})

@app.route('/api/reset-password', methods=['POST'])
def reset_pass():
    data = request.json
    # Call a new db function to update the password
    update_password(data['email'], data['newPassword'])
    return jsonify({"message": "Password updated"})


if __name__ == '__main__':
    app.run(port=5001, debug=True)
