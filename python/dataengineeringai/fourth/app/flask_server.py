from flask import Flask, request, jsonify, g
from minio import Minio
from cryptography.fernet import Fernet
import json
import io
import psycopg2
import os
import uuid

app = Flask(__name__)

# Initialize MinIO Client
minio_client = Minio(
    "minio:9000",  # MinIO server URL
    access_key="admin",  
    secret_key="password",  
    secure=False  # Set to True if using HTTPS
)

# Initialize PostgreSQL connection
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"), 
    user=os.getenv("DB_USER"), 
    password=os.getenv("DB_PASSWORD"), 
    host=os.getenv("DB_HOST"), 
    port="5432"  
)
cur = conn.cursor()

# Create table for storing data. If you change tables here, remember to do so on the actual db aswell, as this just ensures that any given table exists, if the db happens to be empty. Failure to do so will result in db errors.
cur.execute('''
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    object_id TEXT NOT NULL,
    encryption_key TEXT NOT NULL
);
''')
conn.commit()

cur.close()

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            dbname=os.getenv("DB_NAME"), 
            user=os.getenv("DB_USER"), 
            password=os.getenv("DB_PASSWORD"), 
            host=os.getenv("DB_HOST"), 
            port="5432"
        )
    return g.db

# Ensure buckets exist in minio
if not minio_client.bucket_exists("even"):
    minio_client.make_bucket("even")
if not minio_client.bucket_exists("odd"):
    minio_client.make_bucket("odd")

#To prevent generator flooding server before its fully up (only because generator is running in container with the rest all at once by default)
@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "Flask service is up!"}), 200

def is_object_id_unique(object_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM messages WHERE object_id = %s", (object_id,))
    count = cur.fetchone()[0]
    cur.close()  # Close the cursor after use
    return count == 0

def encrypt_message(message):
    key = Fernet.generate_key()
    cipher = Fernet(key)
    encrypted_message = cipher.encrypt(message)
    return encrypted_message, key

@app.route('/obj', methods=['POST'])
def get_object():
    data = request.get_json()
    if data and 'object_id' in data:
        object_id = data['object_id']
        
        # Determine the bucket based on the prefix of object_id
        if object_id.startswith("even_"):
            bucket = "even"
        elif object_id.startswith("odd_"):
            bucket = "odd"
        else:
            return jsonify({"error": "Invalid object ID prefix."}), 400
        
        # Use the database connection from g
        conn = get_db()
        cur = conn.cursor()
        
        # Query the database for the associated encryption key
        cur.execute("SELECT encryption_key FROM messages WHERE object_id = %s", (object_id,))
        result = cur.fetchone()
        cur.close()

        if result:
            encryption_key = result[0].encode()
            
            try:
                # Retrieve the object from the determined bucket
                encrypted_data = minio_client.get_object(bucket, object_id)
                with encrypted_data:
                    encrypted_content = encrypted_data.read()
                
                # Decrypt the message
                cipher = Fernet(encryption_key)
                decrypted_message = cipher.decrypt(encrypted_content)
                
                return jsonify({"message": decrypted_message.decode('utf-8')}), 200

            except Exception as e:
                return jsonify({"error": "Object not found in the bucket."}), 404

        return jsonify({"error": "Object ID not found in database."}), 404

    return jsonify({"error": "Invalid data! 'object_id' key is required."}), 400

@app.route('/even', methods=['POST'])
def handle_even():
    data = request.get_json()
    if data and 'timestamp' in data:
        object_id = f"even_{data['timestamp']}_{uuid.uuid4()}"
        
        conn = get_db()
        cur = conn.cursor()

        while True:
            if is_object_id_unique(object_id):
                break
            object_id = f"even_{data['timestamp']}_{uuid.uuid4()}"

        json_data = json.dumps(data).encode('utf-8')
        encrypted_data, encryption_key = encrypt_message(json_data)

        # Save to MinIO bucket
        minio_client.put_object("even", object_id, io.BytesIO(encrypted_data), len(encrypted_data), metadata={
        "object_id": object_id,
        "owner": "Daniel"
    })

        # Store data in PostgreSQL
        cur.execute("INSERT INTO messages (object_id, encryption_key) VALUES (%s, %s)",
                    (object_id, encryption_key.decode()))
        conn.commit()

        cur.close()

        return jsonify({"message": "Data saved to EVEN bucket!"}), 201
    return jsonify({"error": "Invalid data! 'timestamp' key is required."}), 400


@app.route('/odd', methods=['POST'])
def handle_odd():
    data = request.get_json()
    if data and 'timestamp' in data:
        object_id = f"odd_{data['timestamp']}_{uuid.uuid4()}"
        
        conn = get_db()
        cur = conn.cursor()

        while True:
            if is_object_id_unique(object_id):
                break
            object_id = f"odd_{data['timestamp']}_{uuid.uuid4()}"

        json_data = json.dumps(data).encode('utf-8')
        encrypted_data, encryption_key = encrypt_message(json_data)

        # Save to MinIO bucket
        minio_client.put_object("odd", object_id, io.BytesIO(encrypted_data), len(encrypted_data), metadata={
        "object_id": object_id,
        "owner": "Daniel"
    })

        # Store data in PostgreSQL
        cur.execute("INSERT INTO messages (object_id, encryption_key) VALUES (%s, %s)",
                    (object_id, encryption_key.decode()))
        conn.commit()

        cur.close()  

        return jsonify({"message": "Data saved to ODD bucket!"}), 201
    return jsonify({"error": "Invalid data! 'timestamp' key is required."}), 400

@app.teardown_appcontext
def close_db_connection(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
