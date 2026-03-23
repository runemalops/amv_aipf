from flask import Flask, request, g, session, redirect, url_for
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from models import db, User, SocialLink, Settings
from routes import main
from auth import auth
from admin import admin
import click

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///portfolio.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "your-secret-key-change-in-production"
app.config["LANGUAGES"] = ["en", "es"]

db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    app.config["MAIL_SERVER"] = Settings.get("smtp_server", "") or ""
    app.config["MAIL_PORT"] = int(Settings.get("smtp_port") or 587)
    app.config["MAIL_USE_TLS"] = Settings.get("smtp_tls", "true").lower() == "true"
    app.config["MAIL_USERNAME"] = Settings.get("smtp_username", "") or ""
    app.config["MAIL_PASSWORD"] = Settings.get("smtp_password", "") or ""
    app.config["MAIL_DEFAULT_SENDER"] = Settings.get("smtp_sender", "") or ""

mail = Mail(app)


def get_locale():
    if "lang" in session:
        return session["lang"]
    if hasattr(g, "lang"):
        return g.lang
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route("/set-lang/<lang>")
def set_language(lang):
    if lang in app.config["LANGUAGES"]:
        session["lang"] = lang
    referer = request.headers.get("Referer", "/")
    return redirect(referer)


def set_lang(lang):
    g.lang = lang


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.context_processor
def inject_site_config():
    from models import Settings

    return {
        "site_config": {
            "site_title": Settings.get("site_title", "Your Name"),
            "site_subtitle": Settings.get(
                "site_subtitle", "Your Title | Your Profession"
            ),
            "hero_title": Settings.get("hero_title", "Your Hero Headline"),
            "hero_cta_text": Settings.get("hero_cta_text", "View My Work"),
            "hero_cta_link": Settings.get("hero_cta_link", "/projects"),
            "hero_cta_secondary_text": Settings.get(
                "hero_cta_secondary_text", "Download CV"
            ),
            "hero_cta_secondary_link": Settings.get("hero_cta_secondary_link", "#"),
            "what_i_do_title": Settings.get("what_i_do_title", "What I Do"),
            "what_i_do_subtitle": Settings.get(
                "what_i_do_subtitle", "Describe what you do"
            ),
            "feature1_title": Settings.get("feature1_title", "Feature 1"),
            "feature1_desc": Settings.get("feature1_desc", "Feature description"),
            "feature2_title": Settings.get("feature2_title", "Feature 2"),
            "feature2_desc": Settings.get("feature2_desc", "Feature description"),
            "feature3_title": Settings.get("feature3_title", "Feature 3"),
            "feature3_desc": Settings.get("feature3_desc", "Feature description"),
            "about_badge": Settings.get("about_badge", "Get To Know Me"),
            "about_intro": Settings.get("about_intro", "Your Professional Title"),
            "about_description1": Settings.get(
                "about_description1", "Write your first description here."
            ),
            "about_description2": Settings.get(
                "about_description2", "Write your second description here."
            ),
            "about_image": Settings.get("about_image", ""),
            "cv_download_link": Settings.get("cv_download_link", ""),
            "projects_subtitle": Settings.get(
                "projects_subtitle", "Showcase your work"
            ),
            "blog_subtitle": Settings.get("blog_subtitle", "Share your insights"),
            "cta_title": Settings.get("cta_title", "Let's Work Together"),
            "cta_text": Settings.get(
                "cta_text", "Have a project in mind? Let's discuss."
            ),
        }
    }


@app.context_processor
def inject_translations():
    from translations import inject_translations

    return inject_translations()


app.register_blueprint(main)
app.register_blueprint(auth)
app.register_blueprint(admin)


@app.cli.command("create-admin")
@click.argument("username")
@click.argument("password")
def create_admin(username, password):
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if user:
            click.echo(f"User '{username}' already exists.")
            return

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        click.echo(f"Admin user '{username}' created successfully!")


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User}


if __name__ == "__main__":
    app.run(debug=True)
