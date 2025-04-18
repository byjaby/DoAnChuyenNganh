from flask import Flask, render_template, session, redirect, url_for
from models import KnowledgeBase, News
from news import news_bp
from knowledge import knowledgeBase_bp
from news import get_latest_news
from auth import auth_bp
from user import user_bp
from database import SessionLocal
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
app.register_blueprint(user_bp)

@app.route("/")
def home():
    news_items, has_more_news = get_latest_news()
    user_info = {
        "user_id": session.get("user_id"),
        "role": session.get("role"),
        "full_name": session.get("full_name")
    }
    # Truyền thông tin người dùng vào template
    return render_template("TrangChu.html", news_items=news_items, has_more_news=has_more_news, user_info=user_info)

@app.route("/kienthuc")
def all_KnowledgeBase():
    db = SessionLocal()
    KnowledgeBase_list = (
        db.query(KnowledgeBase)
        .order_by(KnowledgeBase.created_at.desc())
        .all()
    )
    db.close()
    KnowledgeBase_data = [
        {
            "title": n.title,
            "content": n.content,
            "date": n.created_at.strftime("%d/%m/%Y")
        }
        for n in KnowledgeBase_list
    ]
    user_info = {
        "user_id": session.get("user_id"),
        "role": session.get("role"),
        "full_name": session.get("full_name")
    }
    return render_template("AllKnowledge.html", knowledge_items=KnowledgeBase_data, user_info=user_info)

@app.route("/tintuc")
def all_news():
    db = SessionLocal()
    news_list = (
        db.query(News)
        .order_by(News.created_at.desc())
        .all()
    )
    db.close()
    news_data = [
        {
            "title": n.title,
            "content": n.content,
            "date": n.created_at.strftime("%d/%m/%Y")
        }
        for n in news_list
    ]
    user_info = {
        "user_id": session.get("user_id"),
        "role": session.get("role"),
        "full_name": session.get("full_name")
    }
    return render_template("AllNews.html", news_items=news_data, user_info=user_info)

@app.route("/dashboard")
def admin_dashboard():
    return render_template("admin/Dashboard.html")

if __name__ == "__main__":
    app.run()
