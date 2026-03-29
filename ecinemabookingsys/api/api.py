import time
from flask import Flask
from routes.movies import movies_bp
from routes.showtimes import showtimes_bp
from db import get_db

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

if __name__ == '__main__':
    app.run(port=5001, debug=True)
