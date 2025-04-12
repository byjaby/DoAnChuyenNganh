from flask import Flask, render_template, session, redirect, url_for
from news import news_bp
from knowledge import knowledgeBase_bp
from news import get_latest_news
from auth import auth_bp
import secrets
import os

def load_secret_key():
    key_file = "secret_key.txt"
    if os.path.exists(key_file):
        with open(key_file, "r") as f:
            return f.read().strip()
    else:
        key = secrets.token_hex(16)
        with open(key_file, "w") as f:
            f.write(key)
        return key

app = Flask(__name__)
app.secret_key = load_secret_key()  # Gán key

app.register_blueprint(news_bp)
app.register_blueprint(knowledgeBase_bp)
app.register_blueprint(auth_bp)

@app.route("/")
def home():
    news_items, has_more_news = get_latest_news()
    # Lấy thông tin người dùng từ session
    user_info = {
        "user_id": session.get("user_id"),
        "role": session.get("role"),
        "full_name": session.get("full_name")
    }
    # Truyền thông tin người dùng vào template
    return render_template("TrangChu.html", news_items=news_items, has_more_news=has_more_news, user_info=user_info)

@app.route("/admin")
def admin_dashboard():
    return render_template("Admin.html")


if __name__ == "__main__":
    app.run()
