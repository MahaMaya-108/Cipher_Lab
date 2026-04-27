import os
from datetime import datetime
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify,
)
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)

from models import db, User, Log
from ciphers import (
    encrypt_caesar,
    decrypt_caesar,
    encrypt_vigenere,
    decrypt_vigenere,
)


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SESSION_SECRET", "dev-secret-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cipherlab.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"
    login_manager.login_message_category = "warning"

    @login_manager.user_loader
    def load_user(user_id: str):
        return db.session.get(User, int(user_id))

    with app.app_context():
        db.create_all()

    def record_log(action_name: str) -> None:
        entry = Log(action_name=action_name, user_id=current_user.id)
        db.session.add(entry)
        db.session.commit()

    @app.route("/")
    def index():
        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))
        return redirect(url_for("login"))

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))
        if request.method == "POST":
            username = (request.form.get("username") or "").strip()
            password = request.form.get("password") or ""
            confirm = request.form.get("confirm") or ""

            if not username or not password:
                flash("Username and password are required.", "error")
            elif len(password) < 6:
                flash("Password must be at least 6 characters.", "error")
            elif password != confirm:
                flash("Passwords do not match.", "error")
            elif User.query.filter_by(username=username).first():
                flash("That username is already taken.", "error")
            else:
                user = User(username=username)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                login_user(user)
                flash("Account created. Welcome to CipherLab.", "success")
                return redirect(url_for("dashboard"))
        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))
        if request.method == "POST":
            username = (request.form.get("username") or "").strip()
            password = request.form.get("password") or ""
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                flash(f"Welcome back, {user.username}.", "success")
                next_url = request.args.get("next")
                return redirect(next_url or url_for("dashboard"))
            flash("Invalid username or password.", "error")
        return render_template("login.html")

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("You have been logged out.", "success")
        return redirect(url_for("login"))

    @app.route("/dashboard")
    @login_required
    def dashboard():
        return render_template("dashboard.html")

    @app.route("/api/cipher", methods=["POST"])
    @login_required
    def cipher_api():
        data = request.get_json(silent=True) or {}
        mode = data.get("mode")
        cipher = data.get("cipher")
        text = data.get("text", "")
        key = data.get("key", "")

        if not isinstance(text, str) or text == "":
            return jsonify({"error": "Text is required."}), 400
        if mode not in {"encrypt", "decrypt"}:
            return jsonify({"error": "Invalid mode."}), 400
        if cipher not in {"caesar", "vigenere"}:
            return jsonify({"error": "Invalid cipher."}), 400

        try:
            if cipher == "caesar":
                try:
                    shift = int(key)
                except (TypeError, ValueError):
                    return jsonify({"error": "Caesar key must be an integer."}), 400
                result = (
                    encrypt_caesar(text, shift)
                    if mode == "encrypt"
                    else decrypt_caesar(text, shift)
                )
                action_name = (
                    "Caesar Encryption" if mode == "encrypt" else "Caesar Decryption"
                )
            else:
                if not isinstance(key, str) or not key:
                    return jsonify({"error": "Vigenere keyword is required."}), 400
                result = (
                    encrypt_vigenere(text, key)
                    if mode == "encrypt"
                    else decrypt_vigenere(text, key)
                )
                action_name = (
                    "Vigenere Encryption"
                    if mode == "encrypt"
                    else "Vigenere Decryption"
                )
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400

        record_log(action_name)
        return jsonify({"result": result, "action": action_name})

    @app.route("/history")
    @login_required
    def history():
        entries = (
            Log.query.filter_by(user_id=current_user.id)
            .order_by(Log.timestamp.desc())
            .limit(200)
            .all()
        )
        return render_template("history.html", entries=entries)

    @app.route("/history/clear", methods=["POST"])
    @login_required
    def clear_history():
        Log.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        flash("History cleared.", "success")
        return redirect(url_for("history"))

    @app.template_filter("fmt_dt")
    def fmt_dt(value: datetime) -> str:
        if not value:
            return ""
        return value.strftime("%Y-%m-%d %H:%M:%S")

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
