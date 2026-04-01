import time
from flask import Flask, jsonify, session
from dotenv import load_dotenv
from flask_cors import CORS
import os

load_dotenv()

from routes.movies import movies_bp
from routes.showtimes import showtimes_bp
from routes.register import register_bp  
from routes.login import login_bp
from routes.profile import profile_bp
from routes.forgotpassword import forgotpassword_bp
from db import get_db

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_DOMAIN'] = None

CORS(app, 
     supports_credentials=True, 
     origins=["http://localhost:5173"],
     allow_headers=["Content-Type"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

app.register_blueprint(movies_bp)
app.register_blueprint(showtimes_bp)
app.register_blueprint(register_bp)
app.register_blueprint(login_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(forgotpassword_bp)

@app.route('/api/debug-session')
def debug_session():
    return jsonify(dict(session))

@app.route('/api/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/api/ping')
def ping():
    conn = get_db()
    conn.close()
    return {'status': 'connected'}

if __name__ == '__main__':
    app.run(port=5001, debug=True)