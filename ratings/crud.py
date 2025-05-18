from connection import get_connection

def get_ratings():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TVV_DanhGia")
    ratings = cursor.fetchall()
    cursor.close()
    conn.close()
    return ratings

def create_rating(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO TVV_DanhGia (MaBaiViet, MaNguoiDung, Diem, NoiDung)
        VALUES (?, ?, ?, ?)
    """, (data['MaBaiViet'], data['MaNguoiDung'], data['Diem'], data['NoiDung']))
    conn.commit()
    cursor.close()
    conn.close()

def get_rating_by_id(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TVV_DanhGia WHERE MaDanhGia = ?", (id,))
    rating = cursor.fetchone()
    cursor.close()
    conn.close()
    return rating

def update_rating(id, data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE TVV_DanhGia
        SET MaBaiViet = ?, MaNguoiDung = ?, Diem = ?, NoiDung = ?
        WHERE MaDanhGia = ?
    """, (data['MaBaiViet'], data['MaNguoiDung'], data['Diem'], data['NoiDung'], id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_rating(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM TVV_DanhGia WHERE MaDanhGia = ?", (id,))
    conn.commit()
    cursor.close()
    conn.close()