from connection import get_connection

def get_posts():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TVV_BaiViet")
    posts = cursor.fetchall()
    cursor.close()
    conn.close()
    return posts

def create_post(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO TVV_BaiViet (MaNguoiDung, TieuDe, NoiDung, HinhAnh)
        VALUES (?, ?, ?, ?)
    """, (data['MaNguoiDung'], data['TieuDe'], data['NoiDung'], data['HinhAnh']))
    conn.commit()
    cursor.close()
    conn.close()

def get_post_by_id(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TVV_BaiViet WHERE MaBaiViet = ?", (id,))
    post = cursor.fetchone()
    cursor.close()
    conn.close()
    return post

def update_post(id, data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE TVV_BaiViet
        SET MaNguoiDung = ?, TieuDe = ?, NoiDung = ?, HinhAnh = ?
        WHERE MaBaiViet = ?
    """, (data['MaNguoiDung'], data['TieuDe'], data['NoiDung'], data['HinhAnh'], id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_post(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM TVV_BaiViet WHERE MaBaiViet = ?", (id,))
    conn.commit()
    cursor.close()
    conn.close()