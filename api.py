from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models import db, Project, BlogPost, Experience, Education, Skill, ContactMessage
from translation_utils import get_translated, get_translated_list

api = Blueprint("api", __name__, url_prefix="/api")


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


def serialize_project(project, lang="en"):
    return {
        "id": project.id,
        "title": get_translated(project, "title", lang),
        "description": get_translated(project, "description", lang),
        "technologies": (
            [t.strip() for t in project.technologies.split(",")]
            if project.technologies
            else []
        ),
        "link": project.link,
        "demo": project.demo,
        "git_url": project.git_url,
        "featured": project.featured,
    }


def serialize_blog_post(post, lang="en"):
    return {
        "id": post.id,
        "title": get_translated(post, "title", lang),
        "excerpt": get_translated(post, "excerpt", lang),
        "content": get_translated(post, "content", lang),
        "image": post.image,
        "date": post.date.strftime("%B %d, %Y") if post.date else "",
        "author": post.author,
        "category": post.category,
    }


def serialize_experience(exp, lang="en"):
    responsibilities = get_translated(exp, "responsibilities", lang)
    return {
        "id": exp.id,
        "title": get_translated(exp, "title", lang),
        "company": exp.company,
        "period": exp.period,
        "location": exp.location or "",
        "responsibilities": (responsibilities.split("\n") if responsibilities else []),
        "technologies": (
            [t.strip() for t in exp.technologies.split(",")] if exp.technologies else []
        ),
    }


def serialize_education(edu, lang="en"):
    return {
        "id": edu.id,
        "degree": get_translated(edu, "degree", lang),
        "school": get_translated(edu, "school", lang),
        "year": edu.year,
    }


def serialize_skill(skill, lang="en"):
    name = get_translated(skill, "name", lang)
    icon = skill.icon if skill.icon else get_default_icon(name)
    return {
        "id": skill.id,
        "name": name,
        "icon": icon,
        "category": skill.category,
    }


@api.route("/projects", methods=["GET"])
def get_projects():
    lang = request.args.get("lang", "en")
    featured_only = request.args.get("featured", "false").lower() == "true"

    query = Project.query
    if featured_only:
        query = query.filter_by(featured=True)

    projects = query.order_by(Project.created_at.desc()).all()
    return jsonify([serialize_project(p, lang) for p in projects])


@api.route("/projects/<int:project_id>", methods=["GET"])
def get_project(project_id):
    lang = request.args.get("lang", "en")
    project = Project.query.get_or_404(project_id)
    return jsonify(serialize_project(project, lang))


@api.route("/projects", methods=["POST"])
@login_required
def create_project():
    data = request.get_json()

    project = Project(
        title=data.get("title"),
        description=data.get("description"),
        technologies=",".join(data.get("technologies", [])),
        link=data.get("link"),
        demo=data.get("demo"),
        git_url=data.get("git_url"),
        featured=data.get("featured", False),
    )

    if "translations" in data:
        project.translations = data["translations"]

    db.session.add(project)
    db.session.commit()

    return jsonify(serialize_project(project)), 201


@api.route("/projects/<int:project_id>", methods=["PUT"])
@login_required
def update_project(project_id):
    project = Project.query.get_or_404(project_id)
    data = request.get_json()

    if "title" in data:
        project.title = data["title"]
    if "description" in data:
        project.description = data["description"]
    if "technologies" in data:
        project.technologies = ",".join(data["technologies"])
    if "link" in data:
        project.link = data["link"]
    if "demo" in data:
        project.demo = data["demo"]
    if "git_url" in data:
        project.git_url = data["git_url"]
    if "featured" in data:
        project.featured = data["featured"]
    if "translations" in data:
        project.translations = data["translations"]

    db.session.commit()
    return jsonify(serialize_project(project))


@api.route("/projects/<int:project_id>", methods=["DELETE"])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return jsonify({"success": True})


@api.route("/blog", methods=["GET"])
def get_blog_posts():
    lang = request.args.get("lang", "en")
    limit = request.args.get("limit", type=int)

    query = BlogPost.query.order_by(BlogPost.date.desc())

    if limit:
        query = query.limit(limit)

    posts = query.all()
    return jsonify([serialize_blog_post(p, lang) for p in posts])


@api.route("/blog/<int:post_id>", methods=["GET"])
def get_blog_post(post_id):
    lang = request.args.get("lang", "en")
    post = BlogPost.query.get_or_404(post_id)
    return jsonify(serialize_blog_post(post, lang))


@api.route("/experience", methods=["GET"])
def get_experience():
    lang = request.args.get("lang", "en")
    experience = Experience.query.order_by(Experience.created_at.desc()).all()
    return jsonify([serialize_experience(e, lang) for e in experience])


@api.route("/education", methods=["GET"])
def get_education():
    lang = request.args.get("lang", "en")
    education = Education.query.order_by(Education.created_at.desc()).all()
    return jsonify([serialize_education(e, lang) for e in education])


@api.route("/skills", methods=["GET"])
def get_skills():
    lang = request.args.get("lang", "en")
    skills = Skill.query.all()
    return jsonify([serialize_skill(s, lang) for s in skills])


@api.route("/contact", methods=["POST"])
def submit_contact():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    subject = data.get("subject")
    message = data.get("message")

    if not all([name, email, subject, message]):
        return jsonify({"error": "All fields are required"}), 400

    contact = ContactMessage(name=name, email=email, subject=subject, message=message)
    db.session.add(contact)
    db.session.commit()

    return jsonify({"success": True, "id": contact.id}), 201
