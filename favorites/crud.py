from connection import get_connection

def get_favorites():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TVV_YeuThich")
    favorites = cursor.fetchall()
    cursor.close()
    conn.close()
    return favorites

def create_favorite(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO TVV_YeuThich (MaNguoiDung, MaBaiViet)
        VALUES (?, ?)
    """, (data['MaNguoiDung'], data['MaBaiViet']))
    conn.commit()
    cursor.close()
    conn.close()

def get_favorite_by_id(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TVV_YeuThich WHERE MaYeuThich = ?", (id,))
    favorite = cursor.fetchone()
    cursor.close()
    conn.close()
    return favorite

def update_favorite(id, data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE TVV_YeuThich
        SET MaNguoiDung = ?, MaBaiViet = ?
        WHERE MaYeuThich = ?
    """, (data['MaNguoiDung'], data['MaBaiViet'], id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_favorite(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM TVV_YeuThich WHERE MaYeuThich = ?", (id,))
    conn.commit()
    cursor.close()
    conn.close()