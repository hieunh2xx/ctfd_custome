from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Cấu hình kết nối MySQL
db_config = {
    'host': 'localhost',
    'user': 'dbuser',
    'password': '123', 
    'database': 'testdb'
}

@app.route('/', methods=['GET'])
def get_data():
    # conn = mysql.connector.connect(**db_config)
    # cursor = conn.cursor()
    # cursor.execute("SELECT * FROM sample_table;")
    # rows = cursor.fetchall()
    # cursor.close()
    # conn.close()
    return "test"

@app.route('/', methods=['POST'])
def add_data():
    new_data = request.json.get('data')
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sample_table (data) VALUES (%s);", (new_data,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Data added!"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1337)
