from flask import Flask, request, jsonify

from database import get_db_connection

app = Flask(__name__)

# ================= API =================

@app.route('/upload-label', methods=['POST'])
def upload_label():

    try:

        data = request.json

        if not data:
            return jsonify({
                "status": "error",
                "message": "No JSON data received"
            }), 400

        db = get_db_connection()

        if db is None:
            return jsonify({
                "status": "error",
                "message": "Database connection failed"
            }), 500

        cursor = db.cursor()

        # Oracle placeholders
        cols = ", ".join(data.keys())

        placeholders = ", ".join(
            [f":{i+1}" for i in range(len(data))]
        )

        sql = f"""
        INSERT INTO ShipmentLabels
        ({cols})
        VALUES ({placeholders})
        """

        cursor.execute(
            sql,
            tuple(data.values())
        )

        db.commit()

        cursor.close()
        db.close()

        return jsonify({
            "status": "success",
            "message": "Data inserted into Oracle"
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