from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models import db, Project, Experience, Education, BlogPost, Skill, Interest, SocialLink, ContactMessage
from translation_service import translate_text, translate_html

admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.route("/translate", methods=["POST"])
@login_required
def translate_content():
    data = request.get_json()
    text = data.get('text', '')
    target_lang = data.get('target_lang', 'es')
    
    translated = translate_text(text, target_lang)
    return jsonify({'translated': translated})


@admin.route("/translate-html", methods=["POST"])
@login_required
def translate_html_content():
    data = request.get_json()
    html = data.get('html', '')
    target_lang = data.get('target_lang', 'es')
    
    translated = translate_html(html, target_lang)
    return jsonify({'translated': translated})


@admin.route("/")
@login_required
def dashboard():
    project_count = Project.query.count()
    experience_count = Experience.query.count()
    blog_count = BlogPost.query.count()
    skill_count = Skill.query.count()
    
    return render_template(
        "admin/dashboard.html",
        project_count=project_count,
        experience_count=experience_count,
        blog_count=blog_count,
        skill_count=skill_count
    )


@admin.route("/projects", methods=["GET"])
@login_required
def projects():
    projects = Project.query.all()
    return render_template("admin/projects.html", projects=projects)


@admin.route("/projects/new", methods=["GET", "POST"])
@login_required
def new_project():
    if request.method == "POST":
        project = Project(
            title=request.form.get("title"),
            title_es=request.form.get("title_es"),
            description=request.form.get("description"),
            description_es=request.form.get("description_es"),
            technologies=request.form.get("technologies"),
            link=request.form.get("link"),
            demo=request.form.get("demo"),
            git_url=request.form.get("git_url"),
            git_icon=request.form.get("git_icon"),
            featured="featured" in request.form
        )
        db.session.add(project)
        db.session.commit()
        flash("Project created successfully!", "success")
        return redirect(url_for("admin.projects"))
    
    return render_template("admin/project_form.html", project=None)


@admin.route("/projects/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_project(id):
    project = Project.query.get_or_404(id)
    
    if request.method == "POST":
        project.title = request.form.get("title")
        project.title_es = request.form.get("title_es")
        project.description = request.form.get("description")
        project.description_es = request.form.get("description_es")
        project.technologies = request.form.get("technologies")
        project.link = request.form.get("link")
        project.demo = request.form.get("demo")
        project.git_url = request.form.get("git_url")
        project.git_icon = request.form.get("git_icon")
        project.featured = "featured" in request.form
        db.session.commit()
        flash("Project updated successfully!", "success")
        return redirect(url_for("admin.projects"))
    
    return render_template("admin/project_form.html", project=project)


@admin.route("/projects/<int:id>/delete", methods=["POST"])
@login_required
def delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash("Project deleted successfully!", "success")
    return redirect(url_for("admin.projects"))


@admin.route("/experience", methods=["GET"])
@login_required
def experiences():
    experiences = Experience.query.all()
    return render_template("admin/experiences.html", experiences=experiences)


@admin.route("/experience/new", methods=["GET", "POST"])
@login_required
def new_experience():
    if request.method == "POST":
        experience = Experience(
            title=request.form.get("title"),
            title_es=request.form.get("title_es"),
            company=request.form.get("company"),
            period=request.form.get("period"),
            location=request.form.get("location"),
            responsibilities=request.form.get("responsibilities"),
            responsibilities_es=request.form.get("responsibilities_es"),
            technologies=request.form.get("technologies")
        )
        db.session.add(experience)
        db.session.commit()
        flash("Experience created successfully!", "success")
        return redirect(url_for("admin.experiences"))
    
    return render_template("admin/experience_form.html", experience=None)


@admin.route("/experience/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_experience(id):
    experience = Experience.query.get_or_404(id)
    
    if request.method == "POST":
        experience.title = request.form.get("title")
        experience.title_es = request.form.get("title_es")
        experience.company = request.form.get("company")
        experience.period = request.form.get("period")
        experience.location = request.form.get("location")
        experience.responsibilities = request.form.get("responsibilities")
        experience.responsibilities_es = request.form.get("responsibilities_es")
        experience.technologies = request.form.get("technologies")
        db.session.commit()
        flash("Experience updated successfully!", "success")
        return redirect(url_for("admin.experiences"))
    
    return render_template("admin/experience_form.html", experience=experience)


@admin.route("/experience/<int:id>/delete", methods=["POST"])
@login_required
def delete_experience(id):
    experience = Experience.query.get_or_404(id)
    db.session.delete(experience)
    db.session.commit()
    flash("Experience deleted successfully!", "success")
    return redirect(url_for("admin.experiences"))


@admin.route("/blog", methods=["GET"])
@login_required
def blog_posts():
    posts = BlogPost.query.order_by(BlogPost.date.desc()).all()
    return render_template("admin/blog_posts.html", posts=posts)


@admin.route("/blog/new", methods=["GET", "POST"])
@login_required
def new_blog_post():
    if request.method == "POST":
        from datetime import datetime
        post_date = datetime.strptime(request.form.get("date"), "%Y-%m-%d").date()
        
        post = BlogPost(
            title=request.form.get("title"),
            title_es=request.form.get("title_es"),
            excerpt=request.form.get("excerpt"),
            excerpt_es=request.form.get("excerpt_es"),
            content=request.form.get("content"),
            content_es=request.form.get("content_es"),
            image=request.form.get("image"),
            author=request.form.get("author"),
            category=request.form.get("category"),
            date=post_date
        )
        db.session.add(post)
        db.session.commit()
        flash("Blog post created successfully!", "success")
        return redirect(url_for("admin.blog_posts"))
    
    return render_template("admin/blog_form.html", post=None)


@admin.route("/blog/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_blog_post(id):
    post = BlogPost.query.get_or_404(id)
    
    if request.method == "POST":
        from datetime import datetime
        post.title = request.form.get("title")
        post.title_es = request.form.get("title_es")
        post.excerpt = request.form.get("excerpt")
        post.excerpt_es = request.form.get("excerpt_es")
        post.content = request.form.get("content")
        post.content_es = request.form.get("content_es")
        post.image = request.form.get("image")
        post.author = request.form.get("author")
        post.category = request.form.get("category")
        post.date = datetime.strptime(request.form.get("date"), "%Y-%m-%d").date()
        db.session.commit()
        flash("Blog post updated successfully!", "success")
        return redirect(url_for("admin.blog_posts"))
    
    return render_template("admin/blog_form.html", post=post)


@admin.route("/blog/<int:id>/delete", methods=["POST"])
@login_required
def delete_blog_post(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash("Blog post deleted successfully!", "success")
    return redirect(url_for("admin.blog_posts"))


@admin.route("/skills", methods=["GET"])
@login_required
def skills():
    skills = Skill.query.all()
    return render_template("admin/skills.html", skills=skills)


@admin.route("/skills/new", methods=["GET", "POST"])
@login_required
def new_skill():
    if request.method == "POST":
        skill = Skill(
            name=request.form.get("name"),
            name_es=request.form.get("name_es"),
            icon=request.form.get("icon"),
            category=request.form.get("category")
        )
        db.session.add(skill)
        db.session.commit()
        flash("Skill created successfully!", "success")
        return redirect(url_for("admin.skills"))
    
    return render_template("admin/skill_form.html", skill=None)


@admin.route("/skills/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_skill(id):
    skill = Skill.query.get_or_404(id)
    
    if request.method == "POST":
        skill.name = request.form.get("name")
        skill.name_es = request.form.get("name_es")
        skill.icon = request.form.get("icon")
        skill.category = request.form.get("category")
        db.session.commit()
        flash("Skill updated successfully!", "success")
        return redirect(url_for("admin.skills"))
    
    return render_template("admin/skill_form.html", skill=skill)


@admin.route("/skills/<int:id>/delete", methods=["POST"])
@login_required
def delete_skill(id):
    skill = Skill.query.get_or_404(id)
    db.session.delete(skill)
    db.session.commit()
    flash("Skill deleted successfully!", "success")
    return redirect(url_for("admin.skills"))


@admin.route("/social-links", methods=["GET"])
@login_required
def social_links():
    links = SocialLink.query.all()
    return render_template("admin/social_links.html", links=links)


@admin.route("/social-links/new", methods=["GET", "POST"])
@login_required
def new_social_link():
    if request.method == "POST":
        link = SocialLink(
            platform=request.form.get("platform"),
            url=request.form.get("url"),
            icon=request.form.get("icon")
        )
        db.session.add(link)
        db.session.commit()
        flash("Social link created successfully!", "success")
        return redirect(url_for("admin.social_links"))
    
    return render_template("admin/social_link_form.html", link=None)


@admin.route("/social-links/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_social_link(id):
    link = SocialLink.query.get_or_404(id)
    
    if request.method == "POST":
        link.platform = request.form.get("platform")
        link.url = request.form.get("url")
        link.icon = request.form.get("icon")
        db.session.commit()
        flash("Social link updated successfully!", "success")
        return redirect(url_for("admin.social_links"))
    
    return render_template("admin/social_link_form.html", link=link)


@admin.route("/social-links/<int:id>/delete", methods=["POST"])
@login_required
def delete_social_link(id):
    link = SocialLink.query.get_or_404(id)
    db.session.delete(link)
    db.session.commit()
    flash("Social link deleted successfully!", "success")
    return redirect(url_for("admin.social_links"))


@admin.route("/contact-messages", methods=["GET"])
@login_required
def contact_messages():
    messages_list = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template("admin/contact_messages.html", messages_list=messages_list)


@admin.route("/contact-messages/<int:id>/delete", methods=["POST"])
@login_required
def delete_contact_message(id):
    message = ContactMessage.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    flash("Message deleted successfully!", "success")
    return redirect(url_for("admin.contact_messages"))
