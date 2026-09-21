import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import time
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import urllib.parse

app = Flask(__name__)
CORS(app)

db_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/tasksdb")
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "defaultsecret")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def ensure_database_exists(url):
    parsed = urllib.parse.urlsplit(url)
    target_db = parsed.path.lstrip('/') or 'tasksdb'
    if target_db == 'postgres':
        return

    try:
        conn = psycopg2.connect(url)
        conn.close()
    except psycopg2.OperationalError as e:
        err_msg = str(e)
        if "does not exist" in err_msg:
            print(f"Database '{target_db}' does not exist on server. Creating database automatically...")
            user = parsed.username or 'postgres'
            password = parsed.password or ''
            host = parsed.hostname or 'localhost'
            port = parsed.port or 5432
            
            main_conn = psycopg2.connect(
                dbname='postgres',
                user=user,
                password=password,
                host=host,
                port=port
            )
            main_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = main_conn.cursor()
            cursor.execute(f'CREATE DATABASE "{target_db}";')
            cursor.close()
            main_conn.close()
            print(f"Database '{target_db}' created successfully!")
        else:
            raise e

# Wait for Postgres to be ready and ensure database exists
while True:
    try:
        ensure_database_exists(db_url)
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

