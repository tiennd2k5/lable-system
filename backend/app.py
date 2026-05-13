from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# ================= DATABASE =================

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3307,
        user="root",
        password="Mst_0314120650",
        database="LogisticsDB"
    )

# ================= API =================

@app.route('/upload-label', methods=['POST'])
def upload_label():

    try:
        data = request.json

        db = get_db_connection()
        cursor = db.cursor()

        cols = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))

        sql = f"""
        INSERT IGNORE INTO ShipmentLabels
        ({cols})
        VALUES ({placeholders})
        """

        cursor.execute(sql, tuple(data.values()))

        db.commit()

        cursor.close()
        db.close()

        return jsonify({
            "status": "success"
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# ================= MAIN =================

if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )