from flask import Flask, render_template, request, redirect, url_for, session
from users.crud import get_users, create_user, get_user_by_id, update_user, delete_user
from posts.crud import get_posts, create_post, get_post_by_id, update_post, delete_post
from comments.crud import get_comments, create_comment, get_comment_by_id, update_comment, delete_comment
from shares.crud import get_shares, create_share, get_share_by_id, update_share, delete_share
from ingredients.crud import get_ingredients, create_ingredient, get_ingredient_by_id, update_ingredient, delete_ingredient
from favorites.crud import get_favorites, create_favorite, get_favorite_by_id, update_favorite, delete_favorite
from ratings.crud import get_ratings, create_rating, get_rating_by_id, update_rating, delete_rating
from Frontend import (register, login, home, logout, upload_form, upload_file, get_baiviet, check_binh_luan, 
                     get_luot_like, get_luot_BL, get_luot_chia_se, get_chitiet_baiviet,dang_binh_luan)
from Frontend import danh_gia,check_danh_gia
import os
import pyodbc

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Khóa bí mật cho flash messages
app.config['UPLOAD_FOLDER'] = 'static/Images'  # Thư mục lưu file upload

# Đảm bảo thư mục upload tồn tại
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Hàm kiểm tra file hợp lệ
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'jpg'

# Hàm kết nối cơ sở dữ liệu
def get_connection():
    conn_str = (
        "Driver={SQL Server};"
        "Server=DESKTOP-Q6N4J46\\SQLEXPRESS;"  
        "Database=TVV_TTCD2_CongThucNauAn2;"
        "Trusted_Connection=yes"
    )
    return pyodbc.connect(conn_str)

# Users Routes
@app.route('/users', methods=['GET'])
def list_users():
    users = get_users()
    return render_template('users/index.html', users=users)

@app.route('/users/create', methods=['GET'])
def create_user_form():
    return render_template('users/create.html')

@app.route('/users/create', methods=['POST'])
def create_user_submit():
    data = {
        'TenDangNhap': request.form['TenDangNhap'],
        'MatKhau': request.form['MatKhau'],
        'HoTen': request.form['HoTen'],
        'Email': request.form['Email'],
        'Avatar': request.form['Avatar']
    }
    create_user(data)
    return redirect(url_for('list_users'))

@app.route('/users/update/<int:user_id>', methods=['GET'])
def update_user_form(user_id):
    user = get_user_by_id(user_id)
    return render_template('users/update.html', user=user)

@app.route('/users/update/<int:user_id>', methods=['POST'])
def update_user_submit(user_id):
    data = {
        'TenDangNhap': request.form['TenDangNhap'],
        'MatKhau': request.form['MatKhau'],
        'HoTen': request.form['HoTen'],
        'Email': request.form['Email'],
        'Avatar': request.form['Avatar']
    }
    update_user(user_id, data)
    return redirect(url_for('list_users'))

@app.route('/users/delete/<int:user_id>', methods=['POST'])
def delete_user_submit(user_id):
    delete_user(user_id)
    return redirect(url_for('list_users'))

# Posts Routes
@app.route('/posts', methods=['GET'])
def list_posts():
    posts = get_posts()
    return render_template('posts/index.html', posts=posts)

@app.route('/posts/create', methods=['GET'])
def create_post_form():
    return render_template('posts/create.html')

@app.route('/posts/create', methods=['POST'])
def create_post_submit():
    data = {
        'MaNguoiDung': request.form['MaNguoiDung'],
        'TieuDe': request.form['TieuDe'],
        'NoiDung': request.form['NoiDung'],
        'HinhAnh': request.form['HinhAnh']
    }
    create_post(data)
    return redirect(url_for('list_posts'))

@app.route('/posts/update/<int:post_id>', methods=['GET'])
def update_post_form(post_id):
    post = get_post_by_id(post_id)
    return render_template('posts/update.html', post=post)

@app.route('/posts/update/<int:post_id>', methods=['POST'])
def update_post_submit(post_id):
    data = {
        'MaNguoiDung': request.form['MaNguoiDung'],
        'TieuDe': request.form['TieuDe'],
        'NoiDung': request.form['NoiDung'],
        'HinhAnh': request.form['HinhAnh']
    }
    update_post(post_id, data)
    return redirect(url_for('list_posts'))

@app.route('/posts/delete/<int:post_id>', methods=['POST'])
def delete_post_submit(post_id):
    delete_post(post_id)
    return redirect(url_for('list_posts'))

# Comments Routes
@app.route('/comments', methods=['GET'])
def list_comments():
    comments = get_comments()
    return render_template('comments/index.html', comments=comments)

@app.route('/comments/create', methods=['GET'])
def create_comment_form():
    return render_template('comments/create.html')

@app.route('/comments/create', methods=['POST'])
def create_comment_submit():
    data = {
        'MaBaiViet': request.form['MaBaiViet'],
        'MaNguoiDung': request.form['MaNguoiDung'],
        'NoiDung': request.form['NoiDung']
    }
    create_comment(data)
    return redirect(url_for('list_comments'))

@app.route('/comments/update/<int:comment_id>', methods=['GET'])
def update_comment_form(comment_id):
    comment = get_comment_by_id(comment_id)
    return render_template('comments/update.html', comment=comment)

@app.route('/comments/update/<int:comment_id>', methods=['POST'])
def update_comment_submit(comment_id):
    data = {
        'MaBaiViet': request.form['MaBaiViet'],
        'MaNguoiDung': request.form['MaNguoiDung'],
        'NoiDung': request.form['NoiDung']
    }
    update_comment(comment_id, data)
    return redirect(url_for('list_comments'))

@app.route('/comments/delete/<int:comment_id>', methods=['POST'])
def delete_comment_submit(comment_id):
    delete_comment(comment_id)
    return redirect(url_for('list_comments'))

# Shares Routes
@app.route('/shares', methods=['GET'])
def list_shares():
    shares = get_shares()
    return render_template('shares/index.html', shares=shares)

@app.route('/shares/create', methods=['GET'])
def create_share_form():
    return render_template('shares/create.html')

@app.route('/shares/create', methods=['POST'])
def create_share_submit():
    data = {
        'MaBaiViet': request.form['MaBaiViet'],
        'MaNguoiDung': request.form['MaNguoiDung'],
        'NguoiNhan': request.form['NguoiNhan']
    }
    create_share(data)
    return redirect(url_for('list_shares'))

@app.route('/shares/update/<int:share_id>', methods=['GET'])
def update_share_form(share_id):
    share = get_share_by_id(share_id)
    return render_template('shares/update.html', share=share)

@app.route('/shares/update/<int:share_id>', methods=['POST'])
def update_share_submit(share_id):
    data = {
        'MaBaiViet': request.form['MaBaiViet'],
        'MaNguoiDung': request.form['MaNguoiDung'],
        'NguoiNhan': request.form['NguoiNhan']
    }
    update_share(share_id, data)
    return redirect(url_for('list_shares'))

@app.route('/shares/delete/<int:share_id>', methods=['POST'])
def delete_share_submit(share_id):
    delete_share(share_id)
    return redirect(url_for('list_shares'))

# Ingredients Routes
@app.route('/ingredients', methods=['GET'])
def list_ingredients():
    ingredients = get_ingredients()
    return render_template('ingredients/index.html', ingredients=ingredients)

@app.route('/ingredients/create', methods=['GET'])
def create_ingredient_form():
    return render_template('ingredients/create.html')

@app.route('/ingredients/create', methods=['POST'])
def create_ingredient_submit():
    data = {
        'MaBaiViet': request.form['MaBaiViet'],
        'TenNguyenLieu': request.form['TenNguyenLieu'],
        'SoLuong': request.form['SoLuong']
    }
    create_ingredient(data)
    return redirect(url_for('list_ingredients'))

@app.route('/ingredients/update/<int:ingredient_id>', methods=['GET'])
def update_ingredient_form(ingredient_id):
    ingredient = get_ingredient_by_id(ingredient_id)
    return render_template('ingredients/update.html', ingredient=ingredient)

@app.route('/ingredients/update/<int:ingredient_id>', methods=['POST'])
def update_ingredient_submit(ingredient_id):
    data = {
        'MaBaiViet': request.form['MaBaiViet'],
        'TenNguyenLieu': request.form['TenNguyenLieu'],
        'SoLuong': request.form['SoLuong']
    }
    update_ingredient(ingredient_id, data)
    return redirect(url_for('list_ingredients'))

@app.route('/ingredients/delete/<int:ingredient_id>', methods=['POST'])
def delete_ingredient_submit(ingredient_id):
    delete_ingredient(ingredient_id)
    return redirect(url_for('list_ingredients'))

# Favorites Routes
@app.route('/favorites', methods=['GET'])
def list_favorites():
    favorites = get_favorites()
    return render_template('favorites/index.html', favorites=favorites)

@app.route('/favorites/create', methods=['GET'])
def create_favorite_form():
    return render_template('favorites/create.html')

@app.route('/favorites/create', methods=['POST'])
def create_favorite_submit():
    data = {
        'MaNguoiDung': request.form['MaNguoiDung'],
        'MaBaiViet': request.form['MaBaiViet']
    }
    create_favorite(data)
    return redirect(url_for('list_favorites'))

@app.route('/favorites/update/<int:favorite_id>', methods=['GET'])
def update_favorite_form(favorite_id):
    favorite = get_favorite_by_id(favorite_id)
    return render_template('favorites/update.html', favorite=favorite)

@app.route('/favorites/update/<int:favorite_id>', methods=['POST'])
def update_favorite_submit(favorite_id):
    data = {
        'MaNguoiDung': request.form['MaNguoiDung'],
        'MaBaiViet': request.form['MaBaiViet']
    }
    update_favorite(favorite_id, data)
    return redirect(url_for('list_favorites'))

@app.route('/favorites/delete/<int:favorite_id>', methods=['POST'])
def delete_favorite_submit(favorite_id):
    delete_favorite(favorite_id)
    return redirect(url_for('list_favorites'))

# Ratings Routes
@app.route('/ratings', methods=['GET'])
def list_ratings():
    ratings = get_ratings()
    return render_template('ratings/index.html', ratings=ratings)

@app.route('/ratings/create', methods=['GET'])
def create_rating_form():
    return render_template('ratings/create.html')

@app.route('/ratings/create', methods=['POST'])
def create_rating_submit():
    data = {
        'MaBaiViet': request.form['MaBaiViet'],
        'MaNguoiDung': request.form['MaNguoiDung'],
        'Diem': request.form['Diem'],
        'NoiDung': request.form['NoiDung']
    }
    create_rating(data)
    return redirect(url_for('list_ratings'))

@app.route('/ratings/update/<int:rating_id>', methods=['GET'])
def update_rating_form(rating_id):
    rating = get_rating_by_id(rating_id)
    return render_template('ratings/update.html', rating=rating)

@app.route('/ratings/update/<int:rating_id>', methods=['POST'])
def update_rating_submit(rating_id):
    data = {
        'MaBaiViet': request.form['MaBaiViet'],
        'MaNguoiDung': request.form['MaNguoiDung'],
        'Diem': request.form['Diem'],
        'NoiDung': request.form['NoiDung']
    }
    update_rating(rating_id, data)
    return redirect(url_for('list_ratings'))

@app.route('/ratings/delete/<int:rating_id>', methods=['POST'])
def delete_rating_submit(rating_id):
    delete_rating(rating_id)
    return redirect(url_for('list_ratings'))

# Frontend Routes
@app.route('/register', methods=['GET', 'POST'])
def register_route():
    return register()

@app.route('/login', methods=['GET', 'POST'])
def login_route():
    return login()

@app.route('/home')
def home_route():
    return home()

@app.route('/logout')
def logout_route():
    return logout()

@app.route('/upload_form')
def upload_form_route():
    return upload_form()

@app.route('/upload', methods=['POST'])
def upload_file_route():
    return upload_file()

# Route hiển thị danh sách bài viết
@app.route('/danhsachbaiviet')
def danhsachbaiviet_route():
    posts = get_baiviet()
    # Tạo danh sách bài viết kèm thông tin bổ sung
    posts_with_info = []
    for post in posts:
        luot_like = get_luot_like(post.MaBaiViet)
        luot_BL = get_luot_BL(post.MaBaiViet)
        luot_chia_se = get_luot_chia_se(post.MaBaiViet)
        posts_with_info.append({
            'MaBaiViet': post.MaBaiViet,
            'TieuDe': post.TieuDe,
            'NoiDung': post.NoiDung,
            'HinhAnh': post.HinhAnh,
            'LuotXem': post.LuotXem,
            'LuotLike': luot_like,
            'LuotBL': luot_BL,
            'LuotChiaSe': luot_chia_se
        })
    return render_template('Frontend/danhsachbaiviet.html', posts=posts_with_info)

# Route hiển thị chi tiết bài viết
@app.route('/chitietbaiviet/<int:id>')
def chitietbaiviet_route(id):
    data = get_chitiet_baiviet(id)
    ma_nguoi_dung = session.get('user_id')  # Lấy mã người dùng từ session
    da_binh_luan = 0
    da_danh_gia = 0
    if ma_nguoi_dung:
        da_binh_luan = check_binh_luan(id, ma_nguoi_dung)
        da_danh_gia = check_danh_gia(id,ma_nguoi_dung)
    return render_template('Frontend/chitietbaiviet.html', post=data['post'], avg_rating=data['avg_rating'], comments=data['comments'],da_binh_luan=da_binh_luan,da_danh_gia=da_danh_gia)

@app.route('/dangbinhluan/', methods=['POST'])
def dangbinhluan_route():
    
    ma_nguoi_dung = session['user_id']
    ma_bai_viet = request.form['MaBaiViet']
    noi_dung = request.form['NoiDung']
    dang_binh_luan(ma_nguoi_dung, ma_bai_viet, noi_dung)
    return redirect(url_for('chitietbaiviet_route', id=ma_bai_viet))

@app.route('/danhgia/', methods=['POST'])
def danh_gia_route():
    ma_nguoi_dung = session['user_id']
    ma_bai_viet = request.form['MaBaiViet']
    diem = request.form['Diem']
    noiDung =  request.form['NoiDung']
    danh_gia(ma_nguoi_dung,ma_bai_viet,diem,noiDung)
    return redirect(url_for('chitietbaiviet_route', id=ma_bai_viet))


if __name__ == '__main__':
    app.run(debug=True)