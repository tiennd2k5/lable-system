CREATE TABLE Company_Shipment_Master (

    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    CN_Number              VARCHAR2(50),
    From_Loc               VARCHAR2(500),
    To_Loc                 VARCHAR2(500),
    Ship_to_Postal_Code    VARCHAR2(20),

    Carrier_Info           VARCHAR2(255),
    PRO_Number             VARCHAR2(100),
    BL_Number              VARCHAR2(100),
    LOT_Number             VARCHAR2(100),

    Fty_PO                 VARCHAR2(100),
    Style_Code             VARCHAR2(100),
    Season                 VARCHAR2(50),
    Size_Val               VARCHAR2(50),

    PO_Doc_Dt              DATE,
    AFS_Cat                VARCHAR2(50),
    Ship_To_Code           VARCHAR2(50),

    Quantity               NUMBER,

    Cust_PO                VARCHAR2(100),
    Cust_SKU               VARCHAR2(100),
    Dept_Info              VARCHAR2(100),
    CSL_Info               VARCHAR2(100),

    Size_Qty_Label         VARCHAR2(1000),

    SSCC_Number            VARCHAR2(100) NOT NULL,

    created_at             TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Common mapping fields
CREATE INDEX idx_company_cn
ON Company_Shipment_Master (CN_Number);

CREATE INDEX idx_company_pro
ON Company_Shipment_Master (PRO_Number);

CREATE INDEX idx_company_bl
ON Company_Shipment_Master (BL_Number);

CREATE INDEX idx_company_lot
ON Company_Shipment_Master (LOT_Number);

-- Product/business mapping
CREATE INDEX idx_company_style
ON Company_Shipment_Master (Style_Code);

CREATE INDEX idx_company_fty_po
ON Company_Shipment_Master (Fty_PO);

CREATE INDEX idx_company_cust_sku
ON Company_Shipment_Master (Cust_SKU);

CREATE INDEX idx_company_ship_to
ON Company_Shipment_Master (Ship_To_Code);

CREATE INDEX idx_company_postal
ON Company_Shipment_Master (Ship_to_Postal_Code);