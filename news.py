# news.py
from flask import Blueprint, request, render_template, redirect, jsonify
from database import SessionLocal
from sqlalchemy import text
from models import News
from math import ceil

news_bp = Blueprint("news", __name__, url_prefix="/news")

def get_latest_news(limit=6):
    db = SessionLocal()
    all_news = db.query(News).order_by(News.created_at.desc()).all()
    db.close()

    news_data = [
        {
            "title": n.title,
            "content": n.content,
            "date": n.created_at.strftime("%d/%m/%Y")
        }
        for n in all_news
    ]
    return news_data[:limit], len(news_data) > limit  # Trả về tin và cờ "còn tin"

@news_bp.route("/")
def news_list():
    db = SessionLocal()
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 5
        offset = (page - 1) * per_page

        total_news = db.execute(text("SELECT COUNT(*) FROM news")).scalar()
        total_pages = ceil(total_news / per_page)

        result = db.execute(text("""
            SELECT news.news_id, news.title, news.content, news.created_at, users.full_name AS admin_name
            FROM news
            JOIN users ON news.admin_id = users.user_id
            ORDER BY news.created_at DESC
            LIMIT :limit OFFSET :offset
        """), {'limit': per_page, 'offset': offset}).mappings().all()

        news = list(result)
        return render_template("news.html", news=news, page=page, total_pages=total_pages)
    except Exception as e:
        print(f"[ERROR] /news: {e}")
        return "Internal Server Error", 500
    finally:
        db.close()

@news_bp.route("/add", methods=["POST"])
def api_add_news():
    db = SessionLocal()
    data = request.get_json()
    try:
        new_news = News(
            title=data["title"],
            content=data["content"],
            admin_id=1
        )
        db.add(new_news)
        db.commit()
        return jsonify({"message": "News added successfully"}), 200
    except Exception as e:
        print(f"[ERROR] /add-news: {e}")
        db.rollback()
        return jsonify({"error": "Failed to add news"}), 500
    finally:
        db.close()

@news_bp.route("/edit", methods=["POST"])
def edit_news():
    db = SessionLocal()
    try:
        news_id = request.form.get("news_id")
        title = request.form.get("title")
        content = request.form.get("content")

        db.execute(text("""
            UPDATE news SET title = :title, content = :content
            WHERE news_id = :news_id
        """), {
            'title': title,
            'content': content,
            'news_id': news_id
        })
        db.commit()
        return redirect("/news")
    except Exception as e:
        print(f"[ERROR] Edit news: {e}")
        db.rollback()
        return redirect("/news")
    finally:
        db.close()

@news_bp.route("/delete", methods=["POST"])
def delete_news_post():
    news_id = request.form.get("news_id")
    db = SessionLocal()
    try:
        db.execute(text("DELETE FROM news WHERE news_id = :news_id"), {'news_id': news_id})
        db.commit()
        return redirect("/news")
    except Exception as e:
        print(f"[ERROR] delete_news_post: {e}")
        db.rollback()
        return "Đã xảy ra lỗi khi xóa tin tức.", 500
    finally:
        db.close()

@news_bp.route("/tintuc")
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
    return render_template("AllNews.html", news_items=news_data)