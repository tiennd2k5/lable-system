import os
import re
import mysql.connector
import pdfplumber
import requests

# ================== DATABASE ==================
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3307,
        user="root",
        password="Mst_0314120650",
        database="LogisticsDB"
    )

# ================== API CLIENT ==================
def send_to_api(data):
    try:
        response = requests.post(
            "http://127.0.0.1:5000/upload-label",
            json=data
        )
        print(f"\n[API] Response: {response.json()}")
        return response
    except Exception as e:
        print(f"\n[API] Lỗi kết nối API: {e}")

# ================== PDF READER ==================
def read_pdf_data(pdf_path):
    items = []
    text_full = ""
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        # Lấy dạng từ kèm tọa độ
        words = page.extract_words()
        for word in words:
            items.append({
                'text': word['text'].strip(),
                'x_min': word['x0'], 
                'y': word['top'] 
            })
        # Lấy toàn bộ văn bản thô
        text_full = page.extract_text()
    return items, text_full

# ================== PARSER ==================
import re

def parse_label(structured_items, raw_text):
    data = {k: '' for k in ['CN_Number', 'From_Loc', 'To_Loc', 'Ship_to_Postal_Code', 'Carrier_Info', 
                             'PRO_Number', 'BL_Number', 'LOT_Number', 'Fty_PO', 'Style_Code', 
                             'Season', 'Size_Val', 'PO_Doc_Dt', 'AFS_Cat', 'Ship_To_Code', 
                             'Quantity', 'Cust_PO', 'Cust_SKU', 'Dept_Info', 'CSL_Info', 
                             'Size_Qty_Label', 'SSCC_Number']}

    # --- HÀM HỖ TRỢ 1: Lấy text cùng dòng sau một nhãn tiêu đề cụ thể ---
    def get_row_value(label_name, y_threshold=4):
        # Tìm item chứa nhãn tiêu đề (ví dụ: "PRO:")
        label_item = None
        for item in structured_items:
            if label_name.lower() in item['text'].lower():
                label_item = item
                break
        
        if not label_item: return ""
        
        row_parts = []
        for item in structured_items:
            # Thay x_max bằng x_min của nhãn tiêu đề
            if abs(item['y'] - label_item['y']) <= y_threshold and item['x_min'] > label_item['x_min']:
                # Loại bỏ trường hợp item trùng với chính nhãn tiêu đề hoặc là nhãn khác
                clean_txt = item['text'].replace(label_name, "").strip()
                if clean_txt and not clean_txt.endswith(':'):
                    row_parts.append({'text': clean_txt, 'x': item['x_min']})
        
        row_parts.sort(key=lambda x: x['x'])
        return " ".join([p['text'] for p in row_parts]).strip()

    # --- HÀM HỖ TRỢ 2: Lấy dữ liệu theo Regex nhưng chỉ lấy kết quả đầu tiên thỏa mãn ---
    def grab_clean(pattern, clean_all_space=True):
        m = re.search(pattern, raw_text, re.I)
        if m:
            val = m.group(1).strip()
            # Tách lấy phần đầu tiên trước khi gặp nhãn tiếp theo (nếu có dấu :)
            val = val.split(':')[0]
            # Xóa tên nhãn nếu lỡ dính vào cuối chuỗi
            val = re.sub(r'\s+[A-Za-z/]+$', '', val).strip()
            return re.sub(r'\s+', '', val) if clean_all_space else val
        return ""

    # 1. TRÍCH XUẤT CÁC TRƯỜNG CÙNG DÒNG (Dựa trên tọa độ - Chính xác nhất)
    data['Carrier_Info'] = get_row_value("Carrier:")
    data['PRO_Number']   = get_row_value("PRO:")
    data['BL_Number']    = get_row_value("B/L:")
    data['Cust_PO']      = get_row_value("Cust PO:")
    data['Cust_SKU']     = get_row_value("Cust SKU:")
    data['Dept_Info']    = get_row_value("Dept:")
    data['CSL_Info']     = get_row_value("CSL:")

    # 2. XỬ LÝ TO_LOC & FROM_LOC (Theo vùng và dòng)
    to_items = [i for i in structured_items if 105 <= i['y'] <= 150 and i['x_min'] > 120]
    if to_items:
        to_items.sort(key=lambda x: (x['y'], x['x_min']))
        lines = []
        current_line = []
        last_y = to_items[0]['y']
        for item in to_items:
            txt = re.sub(r'^(To):', '', item['text'], flags=re.I).strip()
            if not txt: continue
            if abs(item['y'] - last_y) > 3:
                lines.append(" ".join(current_line))
                current_line = []
            current_line.append(txt)
            last_y = item['y']
        lines.append(" ".join(current_line))
        # Ghép số trong dòng (1 0 4 2 -> 1042) nhưng giữ khoảng cách dòng
        data['To_Loc'] = " ".join([re.sub(r'(?<=\d)\s+(?=\d)', '', ln) for ln in lines if ln.strip()]).strip()

    data['From_Loc'] = " ".join([re.sub(r'^(From):', '', i['text'], flags=re.I).strip() 
                                for i in structured_items if 105 <= i['y'] <= 150 and i['x_min'] < 120 
                                if re.sub(r'^(From):', '', i['text'], flags=re.I).strip()])

    # 3. XỬ LÝ LOT_NUMBER (340 4/4)
    lot_val = get_row_value("LOT:")
    if lot_val:
        # Xóa khoảng trắng dư thừa trong phân số (4 / 4 -> 4/4)
        lot_val = re.sub(r'\s*/\s*', '/', lot_val)
        # Ghép số mã lô (3 4 0 -> 340)
        lot_val = re.sub(r'(?<=\d)\s+(?=\d)', '', lot_val)
        # Đảm bảo có khoảng cách giữa mã và phân số
        m_lot = re.search(r'(\d+)\s*(\d+/\d+)', lot_val)
        data['LOT_Number'] = f"{m_lot.group(1)} {m_lot.group(2)}" if m_lot else lot_val

    # 4. XỬ LÝ SIZE_QTY_LABEL (Chỉ lấy vùng trống dưới chữ Size/Qty)
    sq_title = next((i for i in structured_items if "Size/Qty" in i['text']), None)
    if sq_title:
        sq_content = []
        for item in structured_items:
            # GIẢI PHÁP: Thu hẹp vùng y từ +80 xuống +50 để không chạm tới nhãn SSCC ở dưới
            if sq_title['y'] + 5 < item['y'] < sq_title['y'] + 50:
                # Giới hạn x để chỉ lấy nội dung trong cột của Size/Qty
                if abs(item['x_min'] - sq_title['x_min']) < 80:
                    # Loại bỏ chữ SSCC nếu nó lỡ nằm trong vùng quét
                    if "SSCC" not in item['text'].upper():
                        sq_content.append(item)
        
        sq_content.sort(key=lambda x: (x['y'], x['x_min']))
        data['Size_Qty_Label'] = " ".join([p['text'] for p in sq_content]).strip()

    # 5. CÁC TRƯỜNG THÔNG TIN KHÁC
    data['Fty_PO'] = grab_clean(r'Fty\s*PO:\s*([\d\s\-]+)')
    data['Style_Code'] = grab_clean(r'Style:\s*([A-Z0-9\-]+)', False)
    data['Season'] = grab_clean(r'Season:\s*([A-Z0-9]+)', False)
    data['Size_Val'] = grab_clean(r'Size:\s*([\d\s.]+)')
    data['AFS_Cat'] = grab_clean(r'AFS\s*Cat:\s*([\d\s]+)')
    data['Ship_To_Code'] = grab_clean(r'Ship\s*To:\s*([\d\s]+)')
    data['Quantity'] = grab_clean(r'Qty:\s*([\d\s]+)')
    
    # CN_Number
    cn_p = sorted([i for i in structured_items if 60 <= i['y'] <= 65], key=lambda x: x['x_min'])
    data['CN_Number'] = "".join([re.sub(r'\D', '', p['text']) for p in cn_p])

    # Postal Code (M1M 3H8)
    postal = re.search(r'([A-Z]\d[A-Z])\s*(\d[A-Z]\d)', raw_text)
    if postal: data['Ship_to_Postal_Code'] = f"{postal.group(1)} {postal.group(2)}"

    # Date (YYYY-MM-DD)
    dt = grab_clean(r'PO\s*Doc\s*Dt:\s*([\d\s]+)')
    if len(dt) >= 8: data['PO_Doc_Dt'] = f"{dt[:4]}-{dt[4:6]}-{dt[6:8]}"

    # SSCC
    sscc_m = re.search(r'\(00\)\s*([\d\s]+)', raw_text)
    if sscc_m: data['SSCC_Number'] = "(00)" + re.sub(r'\s+', '', sscc_m.group(1))

    return data

# ================== SAVE DATABASE ==================
def save_to_db(data):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cols = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        sql = f"INSERT IGNORE INTO ShipmentLabels ({cols}) VALUES ({placeholders})"
        cursor.execute(sql, tuple(data.values()))
        db.commit()
        cursor.close()
        db.close()
        print("\n[Hệ thống] Đã lưu vào MySQL.")
    except Exception as e:
        print(f"Lỗi database: {e}")

# ================== MAIN ==================
pdf_path = r"./pdf/20260203152424.pdf"

if __name__ == "__main__":
    if not os.path.exists(pdf_path):
        print(f"Không tìm thấy file: {pdf_path}")
    else:
        items, raw_text = read_pdf_data(pdf_path)
        
        # # IN DEBUG TỌA ĐỘ (Để bạn soi lỗi C/N)
        # print(f"{'TEXT':<20} | {'X':<8} | {'Y':<8}")
        # print("-" * 40)
        # for item in items:
        #     # Tập trung in vùng có khả năng chứa C/N (y thấp)
        #     if item['y'] < 250:
        #         print(f"{item['text']:<20} | {item['x_min']:<8.1f} | {item['y']:<8.1f}")
        
        parsed_data = parse_label(items, raw_text)

        print("\n====== KẾT QUẢ TRÍCH XUẤT ======")
        for k, v in parsed_data.items():
            print(f"{k:20}: {v}")

        # save_to_db(parsed_data)
        send_to_api(parsed_data)

