from flask import request, redirect, url_for, flash, render_template, session
import pyodbc
from connection import get_connection
import os

# Đảm bảo thư mục upload tồn tại
UPLOAD_FOLDER = 'static/Images'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Kiểm tra file hợp lệ
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'jpg'

# Hàm xử lý đăng ký
def register():
    if request.method == 'POST':
        ho_ten = request.form['HoTen']
        email = request.form['Email']
        ten_dang_nhap = request.form['TenDangNhap']
        mat_khau = request.form['MatKhau']
        avatar = request.form.get('Avatar', '')

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO TVV_NguoiDung (TenDangNhap, MatKhau, HoTen, Email, Avatar)
                VALUES (?, ?, ?, ?, ?)
            """, (ten_dang_nhap, mat_khau, ho_ten, email, avatar))
            conn.commit()
            flash('Đăng ký thành công! Vui lòng đăng nhập.')
            return redirect(url_for('login_route'))
        except pyodbc.IntegrityError:
            flash('Tên đăng nhập hoặc email đã tồn tại.')
            return redirect(url_for('register_route'))
        finally:
            cursor.close()
            conn.close()
    return render_template('Frontend/register.html')

# Hàm xử lý đăng nhập
def login():
    if request.method == 'POST':
        ten_dang_nhap = request.form['TenDangNhap']
        mat_khau = request.form['MatKhau']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM TVV_NguoiDung WHERE TenDangNhap = ? AND MatKhau = ?", (ten_dang_nhap, mat_khau))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session['user_id'] = user.MaNguoiDung
            session['user_name'] = user.HoTen
            flash('Đăng nhập thành công!')
            return redirect(url_for('home_route'))
        else:
            flash('Sai tài khoản hoặc mật khẩu')
            return redirect(url_for('login_route'))
    return render_template('Frontend/login.html')

# Hàm xử lý trang chủ
def home():
    return render_template('Frontend/trangchu.html')

# Hàm xử lý đăng xuất
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    flash('Đăng xuất thành công!')
    return redirect(url_for('login_route'))

# Hàm hiển thị form upload
def upload_form():
    return render_template('Frontend/test.html')

# Hàm xử lý upload file
def upload_file():
    if 'HinhAnh' not in request.files:
        flash('Không có file ảnh')
        return redirect(url_for('upload_form'))
    file = request.files['HinhAnh']
    if file.filename == '':
        flash('Chưa chọn file')
        return redirect(url_for('upload_form'))
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO TVV_BaiViet (MaNguoiDung, TieuDe, NoiDung, HinhAnh)
            VALUES (?, ?, ?, ?)
        """, (request.form['MaNguoiDung'], request.form['TieuDe'], request.form['NoiDung'], filename))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Đăng bài thành công')
        return redirect(url_for('upload_form'))
    else:
        flash('Ảnh không phải đuôi .jpg')
        return redirect(url_for('upload_form'))
    
# Hàm lấy số lượt like của một bài viết
def get_luot_like(idpost):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM TVV_YeuThich WHERE MaBaiViet = ?", (idpost,))
    luotlike = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return luotlike

# Hàm lấy số lượt bình luận của một bài viết
def get_luot_BL(idpost):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM TVV_BinhLuan WHERE MaBaiViet = ?", (idpost,))
    luotBL = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return luotBL

# Hàm lấy số lượt chia sẻ của một bài viết
def get_luot_chia_se(idpost):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM TVV_ChiaSe WHERE MaBaiViet = ?", (idpost,))
    luotchiase = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return luotchiase

# Hàm lấy danh sách bài viết
def get_baiviet():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TVV_BaiViet")
    posts = cursor.fetchall()
    cursor.close()
    conn.close()
    return posts

# Hàm xử lý chi tiết bài viết
def get_chitiet_baiviet(id):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Lấy thông tin bài viết
    cursor.execute("SELECT * FROM TVV_BaiViet WHERE MaBaiViet = ?", (id,))
    post = cursor.fetchone()
    
    # Tăng lượt xem
    cursor.execute("UPDATE TVV_BaiViet SET LuotXem = LuotXem + 1 WHERE MaBaiViet = ?", (id,))
    conn.commit()
    
    # Lấy đánh giá trung bình
    cursor.execute("SELECT AVG(CAST(Diem AS FLOAT)) FROM TVV_DanhGia WHERE MaBaiViet = ?", (id,))
    avg_rating_raw = cursor.fetchone()
    avg_rating = avg_rating_raw[0] if avg_rating_raw[0] is not None else 0  # Xử lý khi không có dữ liệu
    
    # Lấy danh sách bình luận
    cursor.execute("SELECT MaBinhLuan, MaBaiViet, MaNguoiDung, NoiDung, NgayBinhLuan FROM TVV_BinhLuan WHERE MaBaiViet = ? order by NgayBinhLuan DESC", (id,))
    comments_raw = cursor.fetchall()
    
    # Chuyển đổi danh sách bình luận thành danh sách từ điển
    comments = []
    for comment in comments_raw:
        cursor.execute("SELECT TenDangNhap, Avatar FROM TVV_NguoiDung WHERE MaNguoiDung = ?", (comment.MaNguoiDung,))
        user_info = cursor.fetchone()
        
        comment_dict = {
            'MaBinhLuan': comment.MaBinhLuan,
            'MaBaiViet': comment.MaBaiViet,
            'MaNguoiDung': comment.MaNguoiDung,
            'NoiDung': comment.NoiDung,
            'NgayBinhLuan': comment.NgayBinhLuan,
            'TenDangNhap': user_info.TenDangNhap if user_info else 'Unknown',
            'Avatar': user_info.Avatar if user_info else ''
        }
        comments.append(comment_dict)
    
    cursor.close()
    conn.close()
    
    return {
        'post': post,
        'avg_rating': avg_rating,
        'comments': comments
    }
def dang_binh_luan(ma_nguoi_dung, ma_bai_viet, noi_dung):
    conn = get_connection()  
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO TVV_BinhLuan (MaBaiViet, MaNguoiDung, NoiDung)
        VALUES (?, ?, ?)
    """, (ma_bai_viet, ma_nguoi_dung, noi_dung))
    conn.commit()
    cursor.close()
    conn.close()
def check_binh_luan(ma_bai_viet,ma_nguoi_dung):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT *FROM TVV_BinhLuan WHERE MaBaiViet=? and MaNguoiDung=?",ma_bai_viet,ma_nguoi_dung)
    checkBL = cursor.fetchone()
    cursor.close()
    conn.close()
    if checkBL:
        return 1  # Đã bình luận
    else:
        return 0 # chưa bình luận
def danh_gia(ma_bai_viet,ma_nguoi_dung,diem,noi_dung):
    conn = get_connection()  
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO TVV_DanhGia (MaBaiViet, MaNguoiDung, Diem, NoiDung)
        VALUES (?, ?, ?, ?)
    """, (ma_bai_viet, ma_nguoi_dung, diem, noi_dung))
    conn.commit()
    cursor.close()
    conn.close()
def check_danh_gia(ma_bai_viet,ma_nguoi_dung):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT *FROM TVV_DanhGia WHERE MaBaiViet=? and MaNguoiDung=?",ma_bai_viet,ma_nguoi_dung)
    checkDG = cursor.fetchone()
    cursor.close()
    conn.close()
    if checkDG:
        return 1  
    else:
        return 0 