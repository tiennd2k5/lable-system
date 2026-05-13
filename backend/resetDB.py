import mysql.connector

def clear_database():
    try:
        db = mysql.connector.connect(
            host="localhost",
            port=3307,
            user="root",
            password="Mst_0314120650",
            database="LogisticsDB"
        )
        cursor = db.cursor()
        
        # Lệnh xóa sạch bảng
        sql = "TRUNCATE TABLE ShipmentLabels"
        cursor.execute(sql)
        
        db.commit()
        print("[DATABASE] Đã xóa toàn bộ dữ liệu mẫu thành công!")
        
        cursor.close()
        db.close()
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    confirm = input("Bạn có chắc chắn muốn xóa sạch DB? (y/n): ")
    if confirm.lower() == 'y':
        clear_database()