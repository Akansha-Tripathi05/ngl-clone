# # from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
# # from config import Config
# # from models import db, Message
# # import os

# # def create_app():
# #     app = Flask(__name__, static_folder="static", template_folder="templates")
# #     app.config.from_object(Config)
# #     db.init_app(app)

# #     with app.app_context():
# #         db.create_all()

# #     # Public submission page
# #     @app.route("/", methods=["GET"])
# #     def submit_page():
# #         # page will attempt username detection via JS
# #         return render_template("submit.html")

# #     @app.route("/submit", methods=["POST"])
# #     def submit_message():
# #         data = request.form
# #         content = data.get("message", "").strip()
# #         username = data.get("username") or data.get("u") or None
# #         if not content:
# #             return jsonify({"status":"error","message":"Message cannot be empty"}), 400
# #         msg = Message(
# #             username=username,
# #             content=content,
# #             user_agent=request.headers.get("User-Agent"),
# #             ip_address=request.remote_addr
# #         )
# #         db.session.add(msg)
# #         db.session.commit()
# #         # nice JSON response to allow AJAX friendliness
# #         return jsonify({"status":"ok","id": msg.id, "created_at": msg.created_at.isoformat()})

# #     # Admin login
# #     @app.route("/admin/login", methods=["GET","POST"])
# #     def admin_login():
# #         if request.method == "POST":
# #             pw = request.form.get("password","")
# #             if pw == app.config["ADMIN_PASSWORD"]:
# #                 session["admin_logged_in"] = True
# #                 return redirect(url_for("admin_panel"))
# #             else:
# #                 flash("Incorrect password","danger")
# #         return render_template("admin_login.html")

# #     # Admin logout
# #     @app.route("/admin/logout")
# #     def admin_logout():
# #         session.pop("admin_logged_in", None)
# #         return redirect(url_for("admin_login"))

# #     # Admin panel (protected)
# #     def admin_required(f):
# #         from functools import wraps
# #         @wraps(f)
# #         def wrapped(*a, **kw):
# #             if not session.get("admin_logged_in"):
# #                 return redirect(url_for("admin_login"))
# #             return f(*a, **kw)
# #         return wrapped

# #     @app.route("/admin", methods=["GET"])
# #     @admin_required
# #     def admin_panel():
# #         # show latest 200 messages by default
# #         q = Message.query.order_by(Message.created_at.desc()).limit(200).all()
# #         return render_template("admin_panel.html", messages=q)

# #     # lightweight API endpoint to fetch newest messages (for live refresh on admin panel)
# #     @app.route("/admin/api/messages", methods=["GET"])
# #     @admin_required
# #     def admin_api_messages():
# #         after = request.args.get("after")  # ISO timestamp
# #         query = Message.query
# #         if after:
# #             from datetime import datetime
# #             try:
# #                 dt = datetime.fromisoformat(after)
# #                 query = query.filter(Message.created_at > dt)
# #             except Exception:
# #                 pass
# #         msgs = query.order_by(Message.created_at.desc()).limit(200).all()
# #         rows = [{
# #             "id": m.id,
# #             "username": m.username,
# #             "content": m.content,
# #             "created_at": m.created_at.isoformat(),
# #             "ip_address": m.ip_address
# #         } for m in msgs]
# #         return jsonify(rows)

# #     return app

# # if __name__ == "__main__":
# #     app = create_app()
# #     app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))

# from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
# from config import Config
# from models import db, Message
# import os

# def create_app():
#     app = Flask(__name__, static_folder="static", template_folder="templates")
#     app.config.from_object(Config)
#     db.init_app(app)

#     with app.app_context():
#         db.create_all()

#     # Public submission page - NOW ACCEPTS USERNAME IN URL
#     @app.route("/", methods=["GET"])
#     @app.route("/<username>", methods=["GET"])
#     def submit_page(username=None):
#         # Pass username to template if provided in URL
#         return render_template("submit.html", target_username=username)

#     @app.route("/submit", methods=["POST"])
#     def submit_message():
#         data = request.form
#         content = data.get("message", "").strip()
#         # Check multiple sources for username
#         username = data.get("username") or data.get("u") or request.args.get("u") or None
        
#         if not content:
#             return jsonify({"status":"error","message":"Message cannot be empty"}), 400
        
#         msg = Message(
#             username=username,
#             content=content,
#             user_agent=request.headers.get("User-Agent"),
#             ip_address=request.remote_addr
#         )
#         db.session.add(msg)
#         db.session.commit()
#         return jsonify({"status":"ok","id": msg.id, "created_at": msg.created_at.isoformat()})

#     # Admin login
#     @app.route("/admin/login", methods=["GET","POST"])
#     def admin_login():
#         if request.method == "POST":
#             pw = request.form.get("password","")
#             if pw == app.config["ADMIN_PASSWORD"]:
#                 session["admin_logged_in"] = True
#                 return redirect(url_for("admin_panel"))
#             else:
#                 flash("Incorrect password","danger")
#         return render_template("admin_login.html")

#     # Admin logout
#     @app.route("/admin/logout")
#     def admin_logout():
#         session.pop("admin_logged_in", None)
#         return redirect(url_for("admin_login"))

#     # Admin panel (protected)
#     def admin_required(f):
#         from functools import wraps
#         @wraps(f)
#         def wrapped(*a, **kw):
#             if not session.get("admin_logged_in"):
#                 return redirect(url_for("admin_login"))
#             return f(*a, **kw)
#         return wrapped

#     @app.route("/admin", methods=["GET"])
#     @admin_required
#     def admin_panel():
#         q = Message.query.order_by(Message.created_at.desc()).limit(200).all()
#         return render_template("admin_panel.html", messages=q)

#     # NEW: Link generator for admin
#     @app.route("/admin/generate-link", methods=["GET", "POST"])
#     @admin_required
#     def generate_link():
#         if request.method == "POST":
#             username = request.form.get("username", "").strip()
#             if username:
#                 # Generate the shareable link
#                 base_url = request.url_root.rstrip('/')
#                 share_link = f"{base_url}/{username}"
#                 return render_template("generate_link.html", 
#                                      share_link=share_link, 
#                                      username=username)
#         return render_template("generate_link.html")

#     # API endpoint for live refresh
#     @app.route("/admin/api/messages", methods=["GET"])
#     @admin_required
#     def admin_api_messages():
#         after = request.args.get("after")
#         query = Message.query
#         if after:
#             from datetime import datetime
#             try:
#                 dt = datetime.fromisoformat(after)
#                 query = query.filter(Message.created_at > dt)
#             except Exception:
#                 pass
#         msgs = query.order_by(Message.created_at.desc()).limit(200).all()
#         rows = [{
#             "id": m.id,
#             "username": m.username,
#             "content": m.content,
#             "created_at": m.created_at.isoformat(),
#             "ip_address": m.ip_address
#         } for m in msgs]
#         return jsonify(rows)

#     return app

# if __name__ == "__main__":
#     app = create_app()
#     app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))

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

    # Public submission page - NOW ACCEPTS RECIPIENT USERNAME IN URL
    @app.route("/", methods=["GET"])
    @app.route("/<recipient_username>", methods=["GET"])
    def submit_page(recipient_username=None):
        # Pass recipient username to template if provided in URL
        return render_template("submit.html", recipient_username=recipient_username)

    @app.route("/submit", methods=["POST"])
    def submit_message():
        data = request.form
        content = data.get("message", "").strip()
        
        if not content:
            return jsonify({"status":"error","message":"Message cannot be empty"}), 400
        
        # Get recipient
        recipient_username = data.get("recipient_username", "").strip() or None
        
        # Get device and location data
        device_type = data.get("device_type", "").strip() or None
        device_model = data.get("device_model", "").strip() or None
        browser = data.get("browser", "").strip() or None
        os = data.get("os", "").strip() or None
        os_version = data.get("os_version", "").strip() or None
        location_city = data.get("location_city", "").strip() or None
        location_region = data.get("location_region", "").strip() or None
        location_country = data.get("location_country", "").strip() or None
        timezone = data.get("timezone", "").strip() or None
        isp = data.get("isp", "").strip() or None
        fingerprint = data.get("fingerprint", "").strip() or None
        device_details = data.get("device_details", "").strip() or None
        
        # Format username display for admin panel
        if fingerprint and recipient_username:
            username_display = f"[{fingerprint}] → {recipient_username}"
        elif fingerprint:
            username_display = f"[{fingerprint}]"
        elif recipient_username:
            username_display = f"[Unknown] → {recipient_username}"
        else:
            username_display = "[Unknown]"
        
        # Create message record with all device and location data
        msg = Message(
            username=username_display,
            content=content,
            user_agent=request.headers.get("User-Agent"),
            ip_address=request.remote_addr,
            # Device info
            device_type=device_type,
            device_model=device_model,
            browser=browser,
            os=os,
            os_version=os_version,
            # Location info
            location_city=location_city,
            location_region=location_region,
            location_country=location_country,
            timezone=timezone,
            isp=isp,
            # Fingerprint
            fingerprint=fingerprint,
            device_details=device_details
        )
        db.session.add(msg)
        db.session.commit()
        
        # Log for debugging
        print(f"✓ Message received:")
        print(f"  Device: {device_type} {device_model}")
        print(f"  Browser: {browser}")
        print(f"  Location: {location_city}, {location_country}")
        print(f"  Fingerprint: {fingerprint}")
        
        return jsonify({
            "status": "ok",
            "id": msg.id,
            "created_at": msg.created_at.isoformat()
        })

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
        q = Message.query.order_by(Message.created_at.desc()).limit(200).all()
        return render_template("admin_panel.html", messages=q)

    # NEW: Link generator for admin
    @app.route("/admin/generate-link", methods=["GET", "POST"])
    @admin_required
    def generate_link():
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            if username:
                # Generate the shareable link
                base_url = request.url_root.rstrip('/')
                share_link = f"{base_url}/{username}"
                return render_template("generate_link.html", 
                                     share_link=share_link, 
                                     username=username)
        return render_template("generate_link.html")

    # API endpoint for live refresh
    @app.route("/admin/api/messages", methods=["GET"])
    @admin_required
    def admin_api_messages():
        after = request.args.get("after")
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
