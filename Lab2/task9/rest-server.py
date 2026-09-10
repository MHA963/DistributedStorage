import base64
import sqlite3
from flask import Flask, g, make_response, request, send_file
import os
import uuid
# from helper import write_file  # or keep write_file in the same file


def get_db():
    # Connect to the sqlite DB at 'files.db' and store the connection in 'g.db'
    # Re-use the connection if it already exists
    if 'db' not in g:
        g.db = sqlite3.connect(
            'files.db',
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # Enable casting Row objects to Python dictionaries
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    # Close the DB connection and remove it from the 'g' object
    db = g.pop('db', None)
    if db is not None:
        db.close()

def write_file(data):
    # Create blob storage directory if not exists
    os.makedirs("blob_storage", exist_ok=True)

    # Generate random blob name
    blob_name = str(uuid.uuid4()) + ".dat"
    file_path = os.path.join("blob_storage", blob_name)

    # Write file bytes to blob storage
    with open(file_path, "wb") as f:
        f.write(data)

    return blob_name


app = Flask(__name__)
app.teardown_appcontext(close_db)

# Temporary debug endpoint in rest-server.py
@app.route('/debug/db-check', methods=['GET'])
def test_db_connection():
    db = get_db()
    # Execute a simple count query to ensure table accessibility
    cursor = db.execute("SELECT COUNT(*) FROM file")
    count = cursor.fetchone()[0]
    return make_response({"status": "connected", "table": "file", "row_count": count})

@app.route('/files', methods=['POST'])
def add_files():
    payload = request.get_json()
    
    filename = payload.get('filename')
    content_type = payload.get('content_type')
    file_data = base64.b64decode(payload.get('contents_b64'))
    size = len(file_data)
    
    blob_name = write_file(file_data)
    
    db = get_db()
    cursor = db.execute(
        "INSERT INTO file (filename, size, content_type, blob_name) VALUES (?, ?, ?, ?)",
        (filename, size, content_type, blob_name)
    )
    db.commit()
    
    return make_response({"id": cursor.lastrowid}, 201)
    

    
# 3. Launch the server on localhost:9000
if __name__ == '__main__':
    app.run(host="localhost", port=9000)