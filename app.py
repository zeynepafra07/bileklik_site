from flask import Flask
import mysql.connector
from flask import jsonify, request

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MelDiKEL?5655",
    database="bileklik_db"
)

cursor = db.cursor(dictionary=True)

@app.route('/p/<page_id>')
def show_user(page_id):
    cursor.execute("SELECT * FROM users WHERE page_id = %s", (page_id,))
    user = cursor.fetchone()

    if user:
        return jsonify({
            "name": user.get("name") or "—",
            "blood_type": user.get("blood_type") or "—",
            "alergies": user.get("alergies") or "—",
            "cell_no": user.get("cell_no") or "—"
        })
    else:
       return jsonify({"error": "Kullanıcı bulunamadı"}), 404

@app.route('/api/user/<page_id>', methods=["POST"])
def update_user(page_id):
    data = request.json

    cursor.execute("""
        UPDATE users 
        SET name=%s, blood_type=%s, alergies=%s, cell_no=%s
        WHERE page_id=%s
    """, (
        data.get("name"),
        data.get("blood_type"),
        data.get("alergies"),
        data.get("cell_no"),
        page_id
    ))

    db.commit()
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True)