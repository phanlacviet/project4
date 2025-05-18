from connection import get_connection

def get_shares():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TVV_ChiaSe")
    shares = cursor.fetchall()
    cursor.close()
    conn.close()
    return shares

def create_share(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO TVV_ChiaSe (MaBaiViet, MaNguoiDung, NguoiNhan)
        VALUES (?, ?, ?)
    """, (data['MaBaiViet'], data['MaNguoiDung'], data['NguoiNhan']))
    conn.commit()
    cursor.close()
    conn.close()

def get_share_by_id(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TVV_ChiaSe WHERE MaChiaSe = ?", (id,))
    share = cursor.fetchone()
    cursor.close()
    conn.close()
    return share

def update_share(id, data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE TVV_ChiaSe
        SET MaBaiViet = ?, MaNguoiDung = ?, NguoiNhan = ?
        WHERE MaChiaSe = ?
    """, (data['MaBaiViet'], data['MaNguoiDung'], data['NguoiNhan'], id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_share(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM TVV_ChiaSe WHERE MaChiaSe = ?", (id,))
    conn.commit()
    cursor.close()
    conn.close()