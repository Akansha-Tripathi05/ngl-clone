from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from config import Config
from models import db, Message
import os

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Public submission page
    @app.route("/", methods=["GET"])
    def submit_page():
        # page will attempt username detection via JS
        return render_template("submit.html")

    @app.route("/submit", methods=["POST"])
    def submit_message():
        data = request.form
        content = data.get("message", "").strip()
        username = data.get("username") or data.get("u") or None
        if not content:
            return jsonify({"status":"error","message":"Message cannot be empty"}), 400
        msg = Message(
            username=username,
            content=content,
            user_agent=request.headers.get("User-Agent"),
            ip_address=request.remote_addr
        )
        db.session.add(msg)
        db.session.commit()
        # nice JSON response to allow AJAX friendliness
        return jsonify({"status":"ok","id": msg.id, "created_at": msg.created_at.isoformat()})

    # Admin login
    @app.route("/admin/login", methods=["GET","POST"])
    def admin_login():
        if request.method == "POST":
            pw = request.form.get("password","")
            if pw == app.config["ADMIN_PASSWORD"]:
                session["admin_logged_in"] = True
                return redirect(url_for("admin_panel"))
            else:
                flash("Incorrect password","danger")
        return render_template("admin_login.html")

    # Admin logout
    @app.route("/admin/logout")
    def admin_logout():
        session.pop("admin_logged_in", None)
        return redirect(url_for("admin_login"))

    # Admin panel (protected)
    def admin_required(f):
        from functools import wraps
        @wraps(f)
        def wrapped(*a, **kw):
            if not session.get("admin_logged_in"):
                return redirect(url_for("admin_login"))
            return f(*a, **kw)
        return wrapped

    @app.route("/admin", methods=["GET"])
    @admin_required
    def admin_panel():
        # show latest 200 messages by default
        q = Message.query.order_by(Message.created_at.desc()).limit(200).all()
        return render_template("admin_panel.html", messages=q)

    # lightweight API endpoint to fetch newest messages (for live refresh on admin panel)
    @app.route("/admin/api/messages", methods=["GET"])
    @admin_required
    def admin_api_messages():
        after = request.args.get("after")  # ISO timestamp
        query = Message.query
        if after:
            from datetime import datetime
            try:
                dt = datetime.fromisoformat(after)
                query = query.filter(Message.created_at > dt)
            except Exception:
                pass
        msgs = query.order_by(Message.created_at.desc()).limit(200).all()
        rows = [{
            "id": m.id,
            "username": m.username,
            "content": m.content,
            "created_at": m.created_at.isoformat(),
            "ip_address": m.ip_address
        } for m in msgs]
        return jsonify(rows)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
