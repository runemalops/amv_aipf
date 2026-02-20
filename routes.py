from flask import Blueprint
from views import (
    render_index,
    render_about,
    render_projects,
    render_experience,
    render_blog,
    render_blog_post,
    render_contact
)

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_index()


@main.route("/about")
def about():
    return render_about()


@main.route("/projects")
def projects():
    return render_projects()


@main.route("/experience")
def experience():
    return render_experience()


@main.route("/blog")
def blog():
    return render_blog()


@main.route("/blog/<int:post_id>")
def blog_post(post_id):
    result = render_blog_post(post_id)
    if result[1] == 404:
        return "Post not found", 404
    return result[0]


@main.route("/contact", methods=["GET", "POST"])
def contact():
    return render_contact()
