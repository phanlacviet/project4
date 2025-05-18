from connection import get_connection

def get_comments():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TVV_BinhLuan")
    comments = cursor.fetchall()
    cursor.close()
    conn.close()
    return comments

def create_comment(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO TVV_BinhLuan (MaBaiViet, MaNguoiDung, NoiDung)
        VALUES (?, ?, ?)
    """, (data['MaBaiViet'], data['MaNguoiDung'], data['NoiDung']))
    conn.commit()
    cursor.close()
    conn.close()

def get_comment_by_id(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TVV_BinhLuan WHERE MaBinhLuan = ?", (id,))
    comment = cursor.fetchone()
    cursor.close()
    conn.close()
    return comment

def update_comment(id, data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE TVV_BinhLuan
        SET MaBaiViet = ?, MaNguoiDung = ?, NoiDung = ?
        WHERE MaBinhLuan = ?
    """, (data['MaBaiViet'], data['MaNguoiDung'], data['NoiDung'], id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_comment(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM TVV_BinhLuan WHERE MaBinhLuan = ?", (id,))
    conn.commit()
    cursor.close()
    conn.close()