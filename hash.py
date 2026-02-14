import mysql.connector
import bcrypt

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MelDiKEL?5655",
    database="bileklik_db"
)
cursor = db.cursor(dictionary=True)

# Buraya hashlemek istediğin kullanıcı id'sini gir
user_id_to_hash = 1

cursor.execute("SELECT password FROM users WHERE id=%s", (user_id_to_hash,))
user = cursor.fetchone()

if user:
    password = user["password"]
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    hashed_str = hashed.decode("utf-8")

    cursor.execute("UPDATE users SET password_hash=%s WHERE id=%s", (hashed_str, user_id_to_hash))
    db.commit()
    print(f"Kullanıcı ID {user_id_to_hash} hashlendi ve kaydedildi.")
else:
    print("Kullanıcı bulunamadı!")

cursor.close()
db.close()