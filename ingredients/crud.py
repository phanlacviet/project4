from connection import get_connection

def get_ingredients():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TVV_NguyenLieu")
    ingredients = cursor.fetchall()
    cursor.close()
    conn.close()
    return ingredients

def create_ingredient(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO TVV_NguyenLieu (MaBaiViet, TenNguyenLieu, SoLuong)
        VALUES (?, ?, ?)
    """, (data['MaBaiViet'], data['TenNguyenLieu'], data['SoLuong']))
    conn.commit()
    cursor.close()
    conn.close()

def get_ingredient_by_id(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TVV_NguyenLieu WHERE MaNguyenLieu = ?", (id,))
    ingredient = cursor.fetchone()
    cursor.close()
    conn.close()
    return ingredient

def update_ingredient(id, data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE TVV_NguyenLieu
        SET MaBaiViet = ?, TenNguyenLieu = ?, SoLuong = ?
        WHERE MaNguyenLieu = ?
    """, (data['MaBaiViet'], data['TenNguyenLieu'], data['SoLuong'], id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_ingredient(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM TVV_NguyenLieu WHERE MaNguyenLieu = ?", (id,))
    conn.commit()
    cursor.close()
    conn.close()