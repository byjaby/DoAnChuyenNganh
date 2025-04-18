from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from models import User
from database import SessionLocal

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET"])
def login_get():
    return render_template("UserLogin.html")

@auth_bp.route("/login", methods=["POST"], endpoint="login_post")
def login_post():
    db = SessionLocal()
    username_or_email = request.form.get("email")
    password = request.form.get("password")

    # Tìm kiếm người dùng trong cơ sở dữ liệu
    user = db.query(User).filter(
        (User.username == username_or_email) | (User.email == username_or_email)
    ).first()

    if user and user.password_hash == password:
        if user.role == "nhan_vien":  # Kiểm tra nếu vai trò là nhan_vien
            session["user_id"] = user.user_id
            session["role"] = user.role
            session["full_name"] = user.full_name
            flash("Đăng nhập thành công!", "success")  # Thêm thông báo thành công
            return redirect(url_for("home"))
        else:
            flash("Bạn không có quyền truy cập vào hệ thống này.", "error")  # Thêm thông báo lỗi về quyền truy cập
            return redirect(url_for("auth.login_get"))
    else:
        flash("Thông tin đăng nhập không chính xác.", "error")  # Thêm thông báo lỗi
        return redirect(url_for("auth.login_get"))

@auth_bp.route("/logout")
def logout():
    session.clear()  # Clear session on logout
    return redirect(url_for("home"))  # Redirect to home page after logout

