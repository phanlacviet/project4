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
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'gif', 'jfif'}

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
    ma_nguoi_dung = session['user_id']
    return render_template('Frontend/dangbaiviet.html', ma_nguoi_dung=ma_nguoi_dung)

# Hàm xử lý upload file
def upload_file():
    if 'HinhAnh' not in request.files:
        flash('Không có file ảnh')
        return redirect(url_for('upload_form'))
    file = request.files['HinhAnh']
    if file.filename == '':
        flash('Chưa chọn file')
        return redirect(url_for('upload_form'))
    phan_loai = request.form.get('PhanLoai')
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO TVV_BaiViet (MaNguoiDung, TieuDe, NoiDung, HinhAnh, MaPhanLoai)
            VALUES (?, ?, ?, ?,?)
        """, (request.form['MaNguoiDung'], request.form['TieuDe'], request.form['NoiDung'], filename, phan_loai))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Đăng bài thành công')
        return redirect(url_for('ThongTinCaNhan'))
    else:
        flash('Ảnh không phải đuôi .jpg')
        return redirect(url_for('ThongTinCaNhan'))
    
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
    
    # 1. Lấy thông tin bài viết
    cursor.execute("SELECT * FROM TVV_BaiViet WHERE MaBaiViet = ?", (id,))
    post = cursor.fetchone()
    
    # 2. Tăng lượt xem
    cursor.execute("UPDATE TVV_BaiViet SET LuotXem = LuotXem + 1 WHERE MaBaiViet = ?", (id,))
    conn.commit()
    
    # 3. Lấy đánh giá trung bình
    cursor.execute("SELECT AVG(CAST(Diem AS FLOAT)) FROM TVV_DanhGia WHERE MaBaiViet = ?", (id,))
    avg_rating_raw = cursor.fetchone()
    avg_rating = avg_rating_raw[0] or 0
    
    # 4. Lấy danh sách bình luận gốc
    cursor.execute("""
        SELECT MaBinhLuan, MaNguoiDung, NoiDung, NgayBinhLuan 
        FROM TVV_BinhLuan 
        WHERE MaBaiViet = ? 
        ORDER BY NgayBinhLuan DESC
    """, (id,))
    comments_raw = cursor.fetchall()
    
    # 5. Chuyển thành dict và thu thập all MaBinhLuan
    comments = []
    parent_ids = []
    for c in comments_raw:
        parent_ids.append(c.MaBinhLuan)
        comments.append({
            'MaBinhLuan': c.MaBinhLuan,
            'MaNguoiDung': c.MaNguoiDung,
            'NoiDung': c.NoiDung,
            'NgayBinhLuan': c.NgayBinhLuan,
            'TenDangNhap': None,  
            'Avatar': None,        
            'Replies': []
        })
    
    # 6. Điền thông tin người comment gốc
    for comment in comments:
        cursor.execute("SELECT TenDangNhap, Avatar FROM TVV_NguoiDung WHERE MaNguoiDung = ?",
                       (comment['MaNguoiDung'],))
        ui = cursor.fetchone()
        if ui:
            comment['TenDangNhap'] = ui.TenDangNhap
            comment['Avatar'] = ui.Avatar
    
    # 7. Lấy tất cả replies cho những MaBinhLuan trên
    if parent_ids:
        placeholders = ','.join('?' * len(parent_ids))
        sql = f"""
            SELECT MaBinhLuanBac2, MaBinhLuan, MaNguoiDung, TenDangNhap, NoiDung, NgayBinhLuan
            FROM TVV_BinhLuan_Bac2
            WHERE MaBinhLuan IN ({placeholders})
            ORDER BY NgayBinhLuan ASC
        """
        cursor.execute(sql, parent_ids)
        replies_raw = cursor.fetchall()
        reply_map = {}
        for r in replies_raw:
            reply_map.setdefault(r.MaBinhLuan, []).append({
                'MaBinhLuanBac2': r.MaBinhLuanBac2,
                'MaNguoiDung':   r.MaNguoiDung,
                'TenDangNhap':   r.TenDangNhap,
                'NoiDung':       r.NoiDung,
                'NgayBinhLuan':  r.NgayBinhLuan
            })
        for comment in comments:
            comment['Replies'] = reply_map.get(comment['MaBinhLuan'], [])
    
    cursor.close()
    conn.close()
    
    return {
        'post': post,
        'avg_rating': avg_rating,
        'comments': comments
    }

def add_reply(ma_binhluan, ma_nguoi_dung, noi_dung):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT TenDangNhap FROM TVV_NguoiDung WHERE MaNguoiDung = ?", (ma_nguoi_dung,))
    ten = cursor.fetchone().TenDangNhap
    cursor.execute("""
        INSERT INTO TVV_BinhLuan_Bac2 (MaBinhLuan, MaNguoiDung, TenDangNhap, NoiDung)
        VALUES (?, ?, ?, ?)
    """, (ma_binhluan, ma_nguoi_dung, ten, noi_dung))
    conn.commit()
    cursor.close()
    conn.close()

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
def timkiem(TieuDe):
    conn = get_connection()
    cursor = conn.cursor()
    search_term = f'%{TieuDe}%'
    cursor.execute("SELECT * FROM TVV_BaiViet WHERE TieuDe LIKE ?", (search_term,))
    ketquaTK = cursor.fetchall()
    cursor.close()
    conn.close()
    return ketquaTK
def check_thich(ma_bai_viet, ma_nguoi_dung):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TVV_YeuThich WHERE MaBaiViet = ? AND MaNguoiDung = ?", (ma_bai_viet, ma_nguoi_dung))
    check = cursor.fetchone()
    cursor.close()
    conn.close()
    return 1 if check else 0

def check_chia_se(ma_bai_viet, ma_nguoi_dung):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TVV_ChiaSe WHERE MaBaiViet = ? AND MaNguoiDung = ?", (ma_bai_viet, ma_nguoi_dung))
    check = cursor.fetchone()
    cursor.close()
    conn.close()
    return 1 if check else 0

def like_post(ma_nguoi_dung, ma_bai_viet):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO TVV_YeuThich (MaNguoiDung, MaBaiViet) VALUES (?, ?)", (ma_nguoi_dung, ma_bai_viet))
    conn.commit()
    cursor.close()
    conn.close()

def unlike_post(ma_nguoi_dung, ma_bai_viet):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM TVV_YeuThich WHERE MaNguoiDung = ? AND MaBaiViet = ?", (ma_nguoi_dung, ma_bai_viet))
    conn.commit()
    cursor.close()
    conn.close()

def share_post(ma_nguoi_dung, ma_bai_viet):
    conn = get_connection()
    cursor = conn.cursor()
    nguoi_nhan = session.get('user_name', 'Unknown')  # Lấy tên người dùng từ session
    cursor.execute("INSERT INTO TVV_ChiaSe (MaBaiViet, MaNguoiDung, NguoiNhan) VALUES (?, ?, ?)", (ma_bai_viet, ma_nguoi_dung, nguoi_nhan))
    conn.commit()
    cursor.close()
    conn.close()

def unshare_post(ma_nguoi_dung, ma_bai_viet):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM TVV_ChiaSe WHERE MaBaiViet = ? AND MaNguoiDung = ?", (ma_bai_viet, ma_nguoi_dung))
    conn.commit()
    cursor.close()
    conn.close()

def userPosts(ma_nguoi_dung):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT *FROM TVV_BaiViet WHERE MaNguoiDung = ?", (ma_nguoi_dung))
    userPosts = cursor.fetchall()
    cursor.close()
    conn.close()
    return userPosts

def userPostShare(ma_nguoi_dung):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MaBaiViet FROM TVV_Chiase WHERE MaNguoiDung = ?", (ma_nguoi_dung))
    mabaiviet = cursor.fetchall()
    ids = [str(row[0]) for row in mabaiviet]
    placeholders = ','.join('?' * len(ids))
    query = f"SELECT * FROM TVV_BaiViet WHERE MaBaiViet IN ({placeholders})"
    cursor.execute(query, ids)
    baiviet_details = cursor.fetchall()
    conn.close()
    return baiviet_details

def userPostlike(ma_nguoi_dung):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.*
        FROM TVV_YeuThich y
        JOIN TVV_BaiViet b ON y.MaBaiViet = b.MaBaiViet
        WHERE y.MaNguoiDung = ?
    """, (ma_nguoi_dung,))
    baiviet_details = cursor.fetchall()
    conn.close()
    return baiviet_details

def userInfo(ma_nguoi_dung):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT *FROM TVV_NguoiDung WHERE MaNguoiDung = ?", (ma_nguoi_dung))
    userInfo = cursor.fetchall()
    cursor.close()
    conn.close()
    return userInfo
def updateUserPost(ma_bai_viet,ma_nguoi_dung,data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE TVV_BaiViet
        SET TieuDe = ?, NoiDung = ?, HinhAnh = ?
        WHERE MaBaiViet = ? AND MaNguoiDung = ?
    """, (data['MaNguoiDung'], data['TieuDe'], data['NoiDung'], data['HinhAnh'], ma_bai_viet, ma_nguoi_dung))
    conn.commit()
    cursor.close()
    conn.close()
def updateUserInfo(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("Update TVV_NguoiDung SET MatKhau = ?, HoTen = ?, Email = ?, Avatar = ? WHERE MaNguoiDung = ?"
                   ,(data['MatKhau'], data['HoTen'], data['Email'], data['Avatar'], data['MaNguoiDung']))
    conn.commit()
    cursor.close()
    conn.close()
def get_post_by_id(ma_bai_viet):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TVV_BaiViet WHERE MaBaiViet = ?", (ma_bai_viet,))
    post = cursor.fetchone()
    cursor.close()
    conn.close()
    return post

def update_user_post(ma_bai_viet, ma_nguoi_dung, data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE TVV_BaiViet
        SET TieuDe = ?, NoiDung = ?, HinhAnh = ?
        WHERE MaBaiViet = ? AND MaNguoiDung = ?
    """, (data['TieuDe'], data['NoiDung'], data['HinhAnh'], ma_bai_viet, ma_nguoi_dung))
    conn.commit()
    cursor.close()
    conn.close()

def delete_user_post(ma_bai_viet):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM TVV_BaiViet WHERE MaBaiViet = ?", (ma_bai_viet,))
    conn.commit()
    cursor.close()
    conn.close()
def ThongBao(ma_nguoi_dung,tieu_de,noi_dung):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("Insert into TVV_ThongBao(MaNguoiDung,TieuDe,NoiDung) values (?,?,?)", (ma_nguoi_dung,tieu_de,noi_dung))
    conn.commit()
    cursor.close()
    conn.close()
def get_thong_tin_bai_viet(ma_bai_viet):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MaNguoiDung, TieuDe FROM TVV_BaiViet WHERE MaBaiViet = ?", (ma_bai_viet,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result
def lay_mon_an_theo_danh_muc(danhmuc):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("Select *from TVV_BaiViet Where MaPhanLoai = ?",(danhmuc,))
    danhsach = cursor.fetchall()
    cursor.close()
    conn.close()
    return danhsach
def get_ten_dang_nhap(ma_nguoi_dung):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT TenDangNhap FROM TVV_NguoiDung WHERE MaNguoiDung = ?", (ma_nguoi_dung,))
    result = cursor.fetchone()
    conn.close()
    return result.TenDangNhap if result else 'Không rõ'
def getAllThongBao(ma_nguoi_dung):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT *FROM TVV_ThongBao WHERE MaNguoiDung = ?", (ma_nguoi_dung,))
    danhsachthongbao = cursor.fetchall()
    conn.close()
    return danhsachthongbao