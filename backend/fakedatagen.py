import random
from datetime import datetime, timedelta

import oracledb
from faker import Faker

fake = Faker()

# =========================
# ORACLE CONNECTION
# =========================
connection = oracledb.connect(
    user="logistics",
    password="oracle",
    host="localhost",
    port=1522,
    service_name="FREEPDB1"
)

cursor = connection.cursor()

# =========================
# SAMPLE DATA POOLS
# =========================
carriers = [
    "FedEx Freight",
    "UPS Supply Chain",
    "DHL Logistics",
    "XPO Logistics",
    "Maersk"
]

seasons = ["Spring", "Summer", "Fall", "Winter"]
sizes = ["XS", "S", "M", "L", "XL", "XXL"]

afs_categories = [
    "APPAREL",
    "FOOTWEAR",
    "ACCESSORIES"
]

departments = [
    "MEN",
    "WOMEN",
    "KIDS",
    "SPORT"
]

# =========================
# INSERT QUERY
# =========================
insert_query = """
INSERT INTO Company_Shipment_Master (
    CN_Number,
    From_Loc,
    To_Loc,
    Ship_to_Postal_Code,
    Carrier_Info,
    PRO_Number,
    BL_Number,
    LOT_Number,
    Fty_PO,
    Style_Code,
    Season,
    Size_Val,
    PO_Doc_Dt,
    AFS_Cat,
    Ship_To_Code,
    Quantity,
    Cust_PO,
    Cust_SKU,
    Dept_Info,
    CSL_Info,
    Size_Qty_Label,
    SSCC_Number
)
VALUES (
    :1, :2, :3, :4, :5, :6, :7, :8,
    :9, :10, :11, :12, :13, :14, :15,
    :16, :17, :18, :19, :20, :21, :22
)
"""

# =========================
# GENERATE 100 ROWS
# =========================
for i in range(100):

    size = random.choice(sizes)
    quantity = random.randint(10, 500)

    row = (
        f"CN{100000 + i}",
        fake.city(),
        fake.city(),
        fake.postcode(),

        random.choice(carriers),

        f"PRO{random.randint(100000, 999999)}",
        f"BL{random.randint(100000, 999999)}",
        f"LOT{random.randint(1000, 9999)}",

        f"FPO{random.randint(10000, 99999)}",
        f"STYLE-{random.randint(100, 999)}",

        random.choice(seasons),
        size,

        fake.date_between(
            start_date="-2y",
            end_date="today"
        ),

        random.choice(afs_categories),

        f"SHIP-{random.randint(100, 999)}",

        quantity,

        f"CPO{random.randint(10000, 99999)}",
        f"SKU-{random.randint(10000, 99999)}",

        random.choice(departments),

        fake.company(),

        f"{size}:{quantity}",

        f"SSCC{random.randint(100000000, 999999999)}"
    )

    cursor.execute(insert_query, row)

# =========================
# COMMIT + CLOSE
# =========================
connection.commit()

print("Inserted 100 fake shipment rows successfully.")

cursor.close()
connection.close()