USE LogisticsDB
CREATE TABLE ShipmentLabels (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,

    CN_Number VARCHAR(50),
    From_Loc TEXT,
    To_Loc TEXT,
    Ship_to_Postal_Code VARCHAR(20),

    Carrier_Info VARCHAR(255),
    PRO_Number VARCHAR(100),
    BL_Number VARCHAR(100),
    LOT_Number VARCHAR(100),

    Fty_PO VARCHAR(100),
    Style_Code VARCHAR(100),
    Season VARCHAR(50),
    Size_Val VARCHAR(50),

    PO_Doc_Dt DATE,
    AFS_Cat VARCHAR(50),
    Ship_To_Code VARCHAR(50),

    Quantity VARCHAR(50),

    Cust_PO VARCHAR(100),
    Cust_SKU VARCHAR(100),
    Dept_Info VARCHAR(100),
    CSL_Info VARCHAR(100),

    Size_Qty_Label TEXT,
    SSCC_Number VARCHAR(100),

    import_date DATETIME DEFAULT CURRENT_TIMESTAMP,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_cn (CN_Number),
    INDEX idx_sscc (SSCC_Number),
    INDEX idx_import_date (import_date),

    UNIQUE KEY uq_sscc (SSCC_Number)
);