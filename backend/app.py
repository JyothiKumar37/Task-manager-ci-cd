import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import time
import psycopg2

app = Flask(__name__)
CORS(app)

db_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/tasksdb")
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "defaultsecret")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Wait for Postgres to be ready
while True:
    try:
        conn = psycopg2.connect(db_url)
        conn.close()
        print("Database is ready!")
        break
    except psycopg2.OperationalError as e:
        print(f"Waiting for database... ({e})")
        time.sleep(2)

class Task(db.Model):
    __tablename__ = "task"  # Explicit table name
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False)

# Create tables inside app context
with app.app_context():
    db.create_all()

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{'id': t.id, 'title': t.title, 'status': t.status} for t in tasks])

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    if not data or 'title' not in data or 'status' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    new_task = Task(title=data['title'], status=data['status'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task added successfully'}), 201

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

