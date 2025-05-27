from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

# Database connection settings
DB_SETTINGS = {
    'host': 'database',
    'database': 'devopsdb',
    'user': 'devopsuser',
    'password': 'devopspassword'
}

@app.route('/api/message', methods=['POST'])
def post_message():
    data = request.get_json()
    content = data.get('content', '')

    try:
        conn = psycopg2.connect(**DB_SETTINGS)
        cur = conn.cursor()
        cur.execute("INSERT INTO messages (content) VALUES (%s)", (content,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'status': 'Message added'})
    except Exception as e:
        return jsonify({'message': f'Error inserting into database: {str(e)}'})

@app.route('/api/message', methods=['GET'])
def get_message():
    try:
        conn = psycopg2.connect(**DB_SETTINGS)
        cur = conn.cursor()
        cur.execute("SELECT content FROM messages ORDER BY id DESC LIMIT 1;")
        row = cur.fetchone()
        cur.close()
        conn.close()

        if row:
            return jsonify({'message': row[0]})
        else:
            return jsonify({'message': 'No messages found'})
    except Exception as e:
        return jsonify({'message': f'Error connecting to database: {str(e)}'})

# 👇 This is crucial — it tells Flask to run the app!
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)





