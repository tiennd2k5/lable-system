import oracledb
def get_db_connection():
    try:
        connection = oracledb.connect(
            user="logistics_app",
            password="oracle",
            host="localhost",
            port=1522,
            service_name="FREEPDB1"
        )
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None
