CREATE TABLE ShipmentLabels (

    id NUMBER GENERATED ALWAYS AS IDENTITY
    PRIMARY KEY,

    CN_Number VARCHAR2(50),
    From_Loc VARCHAR2(500),
    To_Loc VARCHAR2(500),
    Ship_to_Postal_Code VARCHAR2(20),

    Carrier_Info VARCHAR2(255),
    PRO_Number VARCHAR2(100),
    BL_Number VARCHAR2(100),
    LOT_Number VARCHAR2(100),

    Fty_PO VARCHAR2(100),
    Style_Code VARCHAR2(100),
    Season VARCHAR2(50),
    Size_Val VARCHAR2(50),

    PO_Doc_Dt VARCHAR2(20),
    AFS_Cat VARCHAR2(50),
    Ship_To_Code VARCHAR2(50),

    Quantity VARCHAR2(50),

    Cust_PO VARCHAR2(100),
    Cust_SKU VARCHAR2(100),
    Dept_Info VARCHAR2(100),
    CSL_Info VARCHAR2(100),

    Size_Qty_Label VARCHAR2(1000),
    SSCC_Number VARCHAR2(100),
    
    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRINTED NUMBER(1) DEFAULT 0,
    REMAIN NUMBER(1) DEFAULT 1,
    PRINT_COUNT NUMBER DEFAULT 0,
    ALLOW_REPRINT NUMBER(1) DEFAULT 0,
    LAST_PRINT_AT      TIMESTAMP,
    
    CONSTRAINT uq_sscc UNIQUE (SSCC_Number)
);


-- Optional history/search indexes
CREATE INDEX idx_local_cn
ON ShipmentLabels (CN_Number);

CREATE INDEX idx_local_created
ON ShipmentLabels (created_at);

--SELECT USER FROM dual;

--SELECT owner, table_name
--FROM all_tables
--WHERE table_name = 'SHIPMENTLABELS';

DROP TABLE SHIPMENTLABELS;