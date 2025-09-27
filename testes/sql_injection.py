# api_vulneravel.py
from flask import Flask, request, jsonify
import sqlite3
import json

app = Flask(__name__)

@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    
    query = f"SELECT * FROM users WHERE id = {user_id}"
    print(f"Query: {query}")
    
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return jsonify({"id": user[0], "username": user[1]})
    else:
        return jsonify({"error": "Usuário não encontrado"}), 404

@app.route('/api/search', methods=['POST'])
def search_users():
    data = request.json
    search_term = data.get('search', '')
    
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    
    query = f"SELECT * FROM users WHERE username LIKE '%{search_term}%' OR password LIKE '%{search_term}%'"
    print(f"Query: {query}")
    
    cursor.execute(query)
    users = cursor.fetchall()
    conn.close()
    
    return jsonify([{"id": u[0], "username": u[1]} for u in users])

@app.route('/api/delete', methods=['DELETE'])
def delete_user():
    user_id = request.args.get('id', '')
    
    if not user_id:
        return jsonify({"error": "ID necessário"}), 400
    
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    
    query = f"DELETE FROM users WHERE id = {user_id}"
    print(f"Query perigosa: {query}")
    
    cursor.execute(query)
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Operação concluída"})

if __name__ == '__main__':
    app.run(debug=True, port=5001)