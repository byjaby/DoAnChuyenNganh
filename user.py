from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import User
from database import SessionLocal
from werkzeug.security import generate_password_hash

user_bp = Blueprint("user", __name__, url_prefix="/user")


@user_bp.route("/")
def list_users():
    db = SessionLocal()
    users = db.query(User).order_by(User.created_at.desc()).all()
    db.close()
    return render_template("user.html", users=users)


@user_bp.route("/add", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        full_name = request.form["full_name"]
        email = request.form["email"]
        role = request.form["role"]

        db = SessionLocal()
        new_user = User(
            username=username,
            password_hash=generate_password_hash(password),
            full_name=full_name,
            email=email,
            role=role
        )
        db.add(new_user)
        db.commit()
        db.close()
        flash("Thêm người dùng thành công!")
        return redirect(url_for("user.list_users"))

    return render_template("user.html", user=None)


@user_bp.route("/edit/<int:user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    db = SessionLocal()
    user = db.query(User).filter_by(user_id=user_id).first()

    if request.method == "POST":
        user.username = request.form["username"]
        user.full_name = request.form["full_name"]
        user.email = request.form["email"]
        user.role = request.form["role"]
        db.commit()
        db.close()
        flash("Cập nhật thành công!")
        return redirect(url_for("user.list_users"))

    db.close()
    return render_template("user_edit.html", user=user)


@user_bp.route("/delete/<int:user_id>")
def delete_user(user_id):
    db = SessionLocal()
    user = db.query(User).filter_by(user_id=user_id).first()
    if user:
        db.delete(user)
        db.commit()
    db.close()
    flash("Xoá người dùng thành công!")
    return redirect(url_for("user.list_users"))
