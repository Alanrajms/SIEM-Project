from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from detector import detect_threat
import threading
import time

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///logs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Log(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(500))
    level = db.Column(db.String(20))

with app.app_context():
    db.create_all()

LOG_FILE = "sample_logs/live_logs.txt"



def process_logs():
    processed = set()

    while True:
        with app.app_context():   # IMPORTANT FIX

            with open(LOG_FILE, "r") as file:
                lines = file.readlines()

                for line in lines:
                    if line not in processed:
                        processed.add(line)

                        level = "INFO"

                        if detect_threat(line):
                            level = "ALERT"

                        log = Log(
                            message=line.strip(),
                            level=level
                        )

                        db.session.add(log)
                        db.session.commit()

        time.sleep(2)

@app.route('/')

def dashboard():

    logs = Log.query.order_by(Log.id.desc()).all()

    alerts = Log.query.filter_by(level="ALERT").count()

    return render_template(
        "dashboard.html",
        logs=logs,
        alerts=alerts
    )

@app.route('/api/logs')

def api_logs():

    logs = Log.query.order_by(Log.id.desc()).all()

    data = []

    for log in logs:

        data.append({
            "message": log.message,
            "level": log.level
        })

    return jsonify(data)

if __name__ == "__main__":

    t1 = threading.Thread(target=process_logs)
    t1.start()

    app.run(debug=True)