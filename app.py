from flask import Flask, jsonify, request
import mysql.connector
import bcrypt
from flask import render_template

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MelDiKEL?5655",
    database="bileklik_db"
)

@app.route('/api/user/<page_id>')
def show_user(page_id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE page_id = %s", (page_id,))
    user = cursor.fetchone()
    cursor.close()

    if user:
        return jsonify({
            "name": user.get("name") or "—",
            "blood_type": user.get("blood_type") or "—",
            "allergies": user.get("allergies") or "—",
            "emergency_phone": user.get("emergency_phone") or "—"
        })
    else:
        return jsonify({"error": "Kullanıcı bulunamadı"}), 404

@app.route('/api/user/<page_id>', methods=["POST"])
def update_user(page_id):
    try:
        data = request.json
        cursor = db.cursor()
        cursor.execute("""
            UPDATE users
            SET name=%s, blood_type=%s, allergies=%s, emergency_phone=%s
            WHERE page_id=%s
        """, (
            data.get("name"),
            data.get("blood_type"),
            data.get("allergies"),
            data.get("emergency_phone"),
            page_id
        ))
        db.commit()
        cursor.close()
        return jsonify({"success": True})
    except Exception as e:
        print("HATA:", e)
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/verify_password/<page_id>', methods=["POST"])
def verify_password(page_id):
    data = request.json
    input_password = data.get("password").encode("utf-8")

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT password_hash FROM users WHERE page_id = %s", (page_id,))
    user = cursor.fetchone()
    cursor.close()

    if not user:
        return jsonify({"success": False, "error": "Kullanıcı bulunamadı"}), 404

    stored_hash = user["password_hash"].encode("utf-8")
    if bcrypt.checkpw(input_password, stored_hash):
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Şifre yanlış"})
    
@app.route('/p/<page_id>')
def page(page_id):
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)