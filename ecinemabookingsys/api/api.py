import time
from flask import Flask
from routes.movies import movies_bp
from routes.showtimes import showtimes_bp
from db import get_db, validate_login
from flask import request, jsonify

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


if __name__ == '__main__':
    app.run(port=5001, debug=True)