from flask import Flask, request, g, session, redirect, url_for, jsonify
from flask_wtf.csrf import generate_csrf
from flask_wtf import FlaskForm
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from models import db, User, SocialLink, Settings
from routes import main
from auth import auth
from admin import admin
from api import api as api_blueprint
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
            "hero_background_image": Settings.get("hero_background_image", ""),
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
app.register_blueprint(api_blueprint)


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


SKILL_ICON_MAP = {
    "python": "bi-filetype-py",
    "javascript": "bi-braces",
    "js": "bi-braces",
    "typescript": "bi-braces",
    "ts": "bi-braces",
    "react": "bi-lightning-charge",
    "flask": "bi-file-code-fill",
    "django": "bi-file-code-fill",
    "fastapi": "bi-lightning-charge",
    "node": "bi-node-plus",
    "nodejs": "bi-node-plus",
    "html": "bi-filetype-html",
    "css": "bi-filetype-css",
    "sql": "bi-database-fill",
    "postgresql": "bi-database-fill",
    "postgres": "bi-database-fill",
    "mysql": "bi-database-fill",
    "mongodb": "bi-server",
    "mongo": "bi-server",
    "docker": "bi-box-seam-fill",
    "kubernetes": "bi-cloud",
    "k8s": "bi-cloud",
    "git": "bi-git",
    "github": "bi-github",
    "gitlab": "bi-github",
    "bitbucket": "bi-github",
    "aws": "bi-cloud-fill",
    "azure": "bi-cloud-fill",
    "gcp": "bi-cloud-fill",
    "linux": "bi-terminal",
    "ubuntu": "bi-terminal",
    "bash": "bi-terminal-fill",
    "shell": "bi-terminal-fill",
    "rust": "bi-gear-fill",
    "go": "bi-chevron-double-right",
    "golang": "bi-chevron-double-right",
    "java": "bi-cup-hot-fill",
    "spring": "bi-flower1",
    "c++": "bi-code-square",
    "c#": "bi-hash",
    "csharp": "bi-hash",
    "php": "bi-file-code-fill",
    "ruby": "bi-gem",
    "swift": "bi-apple",
    "kotlin": "bi-android2",
    "flutter": "bi-phone-fill",
    "react native": "bi-phone-fill",
    "nextjs": "bi-file-code-fill",
    "vue": "bi-vue",
    "angular": "bi-file-code-fill",
    "tailwind": "bi-palette-fill",
    "bootstrap": "bi-palette2",
    "sass": "bi-palette2",
    "graphql": "bi-diagram-3-fill",
    "rest": "bi-globe2",
    "api": "bi-globe2",
    "ci/cd": "bi-arrow-repeat",
    "devops": "bi-gear",
    "agile": "bi-people-fill",
    "scrum": "bi-people-fill",
    "machine learning": "bi-brain",
    "ml": "bi-brain",
    "ai": "bi-robot",
    "data science": "bi-bar-chart-fill",
    "security": "bi-shield-check",
    "testing": "bi-check-circle-fill",
    "tdd": "bi-check-all",
    "nginx": "bi-server",
    "apache": "bi-server",
    "redis": "bi-lightning-charge-fill",
    "elasticsearch": "bi-search",
    "kafka": "bi-arrow-left-right",
    "terraform": "bi-stack",
    "ansible": "bi-gear",
    "jenkins": "bi-arrow-repeat",
    "github actions": "bi-github",
    "figma": "bi-palette-fill",
    "photoshop": "bi-palette-fill",
    "illustrator": "bi-palette-fill",
    "wordpress": "bi-wordpress",
    "vue.js": "bi-vue",
    "nuxt": "bi-triangle",
    "svelte": "bi-triangle-half",
    "three.js": "bi-box",
    "webgl": "bi-box",
    "express": "bi-file-code",
    "prisma": "bi-database",
    "sequelize": "bi-database",
}


def get_default_icon(skill_name: str) -> str:
    name_lower = skill_name.lower()
    for key, icon in SKILL_ICON_MAP.items():
        if key in name_lower or name_lower in key:
            return icon
    return "bi-star"


@app.cli.command("set-skill-icons")
def set_skill_icons():
    """Set default icons for all skills."""
    from models import Skill

    with app.app_context():
        skills = Skill.query.all()
        updated = 0
        for skill in skills:
            old_icon = skill.icon
            skill.icon = get_default_icon(skill.name)
            if old_icon != skill.icon:
                updated += 1
        db.session.commit()
        click.echo(f"Updated {updated} skills with default icons.")


@app.cli.command("set-interest-icons")
def set_interest_icons():
    """Set default icons for all interests."""
    from models import Interest
    from translation_utils import get_default_interest_icon

    with app.app_context():
        interests = Interest.query.all()
        updated = 0
        for interest in interests:
            name = interest.name
            old_icon = interest.icon
            interest.icon = get_default_interest_icon(name)
            if old_icon != interest.icon:
                updated += 1
        db.session.commit()
        click.echo(f"Updated {updated} interests with default icons.")


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User}


@app.route("/api/csrf-token")
def get_csrf_token():
    from flask_wtf.csrf import generate_csrf

    return jsonify({"csrf_token": generate_csrf()})


if __name__ == "__main__":
    app.run(debug=True)
