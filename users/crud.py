from connection import get_connection

def get_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TVV_NguoiDung")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users

def create_user(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO TVV_NguoiDung (TenDangNhap, MatKhau, HoTen, Email, NgayDangKy, Avatar)
        VALUES (?, ?, ?, ?, GETDATE(), ?)
    """, (data['TenDangNhap'], data['MatKhau'], data['HoTen'], data['Email'], data['Avatar']))
    conn.commit()
    cursor.close()
    conn.close()

def get_user_by_id(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TVV_NguoiDung WHERE MaNguoiDung = ?", (id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def update_user(id, data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE TVV_NguoiDung
        SET TenDangNhap = ?, MatKhau = ?, HoTen = ?, Email = ?, Avatar = ?
        WHERE MaNguoiDung = ?
    """, (data['TenDangNhap'], data['MatKhau'], data['HoTen'], data['Email'], data['Avatar'], id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_user(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM TVV_NguoiDung WHERE MaNguoiDung = ?", (id,))
    conn.commit()
    cursor.close()
    conn.close()