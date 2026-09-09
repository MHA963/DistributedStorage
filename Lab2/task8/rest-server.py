import base64
import sqlite3
from flask import Flask, g, make_response, request, send_file
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

    
# 3. Launch the server on localhost:9000
if __name__ == '__main__':
    app.run(host="localhost", port=9000)