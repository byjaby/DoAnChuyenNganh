# knowledge_base.py
from flask import Blueprint, request, render_template, redirect, jsonify
from database import SessionLocal
from sqlalchemy import text
from models import KnowledgeBase
from math import ceil

knowledgeBase_bp = Blueprint("knowledgeBase", __name__, url_prefix="/admin/knowledgeBase")

@knowledgeBase_bp.route("/")
def knowledge_list():
    db = SessionLocal()
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 5
        offset = (page - 1) * per_page

        total_articles = db.execute(text("SELECT COUNT(*) FROM knowledge_base")).scalar()
        total_pages = ceil(total_articles / per_page)

        result = db.execute(text("""
            SELECT kb.knowledge_id, kb.title, kb.content, kb.created_at, u.full_name AS admin_name
            FROM knowledge_base kb
            JOIN users u ON kb.admin_id = u.user_id
            ORDER BY kb.created_at DESC
            LIMIT :limit OFFSET :offset
        """), {'limit': per_page, 'offset': offset}).mappings().all()

        knowledge = list(result)
        return render_template("admin/knowledgeBase.html", knowledge=knowledge, page=page, total_pages=total_pages)
    except Exception as e:
        print(f"[ERROR] admin/knowledgeBase: {e}")
        return "Internal Server Error", 500
    finally:
        db.close()


@knowledgeBase_bp.route("/add", methods=["POST"])
def api_add_knowledge():
    db = SessionLocal()
    data = request.get_json()
    try:
        new_knowledge = KnowledgeBase(
            title=data["title"],
            content=data["content"],
            admin_id=1  # Replace with dynamic ID if available
        )
        db.add(new_knowledge)
        db.commit()
        return jsonify({"message": "Knowledge base article added successfully"}), 200
    except Exception as e:
        print(f"[ERROR] /admin/knowledgeBase/add: {e}")
        db.rollback()
        return jsonify({"error": "Failed to add knowledge base article"}), 500
    finally:
        db.close()


@knowledgeBase_bp.route("/edit", methods=["POST"])
def edit_knowledge():
    db = SessionLocal()
    try:
        knowledge_id = request.form.get("knowledge_id")
        title = request.form.get("title")
        content = request.form.get("content")

        db.execute(text("""
            UPDATE knowledge_base SET title = :title, content = :content
            WHERE knowledge_id = :knowledge_id
        """), {
            'title': title,
            'content': content,
            'knowledge_id': knowledge_id
        })
        db.commit()
        return redirect("/admin/knowledgeBase")
    except Exception as e:
        print(f"[ERROR] Edit knowledge base: {e}")
        db.rollback()
        return redirect("/admin/knowledgeBase")
    finally:
        db.close()


@knowledgeBase_bp.route("/delete", methods=["POST"])
def delete_knowledge():
    knowledge_id = request.form.get("knowledge_id")
    db = SessionLocal()
    try:
        db.execute(text("DELETE FROM knowledge_base WHERE knowledge_id = :knowledge_id"), {'knowledge_id': knowledge_id})
        db.commit()
        return redirect("/admin/knowledgeBase")
    except Exception as e:
        print(f"[ERROR] delete_knowledge: {e}")
        db.rollback()
        return "Đã xảy ra lỗi khi xóa bài viết.", 500
    finally:
        db.close()
