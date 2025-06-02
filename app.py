from flask import Flask, request
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    c.execute("INSERT INTO users (username, password) VALUES ('admin', 'secret')")
    conn.commit()
    conn.close()

@app.route('/login', methods=['GET'])
def login():
    username = request.args.get('username')
    password = request.args.get('password')

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    # 🚨 VULNERABLE TO SQL INJECTION
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    result = c.execute(query).fetchone()

    if result:
        return "Login Successful!"
    else:
        return "Invalid Credentials"

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
