from flask import Flask, request, g, session, redirect, url_for
from flask_migrate import Migrate
from flask_login import LoginManager
from models import db, User, SocialLink
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
def inject_social_links():
    links = SocialLink.query.all()
    return {
        "social_links": [
            {"platform": l.platform, "url": l.url, "icon": l.icon} for l in links
        ]
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
