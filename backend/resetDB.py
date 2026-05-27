import oracledb

from database import get_db_connection

# ================= RESET DATABASE =================

def reset_database():

    try:

        db = get_db_connection()

        cursor = db.cursor()

        print("[INFO] Clearing ShipmentLabels table...")

        # delete all rows
        cursor.execute("""
            DELETE FROM ShipmentLabels
        """)

        db.commit()

        print("[SUCCESS] Table data deleted.")

        cursor.close()
        db.close()

    except Exception as e:

        print("[ERROR]", e)

# ================= MAIN =================

if __name__ == "__main__":

    reset_database()