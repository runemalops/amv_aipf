from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    technologies = db.Column(db.String(500))
    link = db.Column(db.String(300))
    demo = db.Column(db.String(300))
    git_url = db.Column(db.String(300))
    git_icon = db.Column(db.String(50))
    featured = db.Column(db.Boolean, default=False)
    translations = db.Column(db.JSON, default={})
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    period = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    responsibilities = db.Column(db.Text)
    technologies = db.Column(db.String(500))
    translations = db.Column(db.JSON, default={})
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    degree = db.Column(db.String(200), nullable=False)
    school = db.Column(db.String(200), nullable=False)
    year = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    excerpt = db.Column(db.String(500))
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(500))
    author = db.Column(db.String(100), default="Your Name")
    category = db.Column(db.String(100))
    date = db.Column(db.Date, nullable=False)
    translations = db.Column(db.JSON, default={})
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(100))
    category = db.Column(db.String(50))
    translations = db.Column(db.JSON, default={})
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class SocialLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    icon = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Interest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
