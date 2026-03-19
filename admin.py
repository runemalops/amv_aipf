from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models import (
    db,
    Project,
    Experience,
    Education,
    BlogPost,
    Skill,
    Interest,
    SocialLink,
    ContactMessage,
)
from translation_service import translate_text, translate_html

admin = Blueprint("admin", __name__, url_prefix="/admin")


def get_translations(obj, field):
    translations = obj.translations or {}
    return translations.get(field, {})


@admin.route("/translate", methods=["POST"])
@login_required
def translate_content():
    data = request.get_json()
    text = data.get("text", "")
    target_lang = data.get("target_lang", "es")

    translated = translate_text(text, target_lang)
    return jsonify({"translated": translated})


@admin.route("/translate-html", methods=["POST"])
@login_required
def translate_html_content():
    data = request.get_json()
    html = data.get("html", "")
    target_lang = data.get("target_lang", "es")

    translated = translate_html(html, target_lang)
    return jsonify({"translated": translated})


@admin.route("/")
@login_required
def dashboard():
    project_count = Project.query.count()
    experience_count = Experience.query.count()
    blog_count = BlogPost.query.count()
    skill_count = Skill.query.count()
    education_count = Education.query.count()
    interest_count = Interest.query.count()

    return render_template(
        "admin/dashboard.html",
        project_count=project_count,
        experience_count=experience_count,
        blog_count=blog_count,
        skill_count=skill_count,
        education_count=education_count,
        interest_count=interest_count,
    )


# ============ Projects ============


@admin.route("/projects", methods=["GET"])
@login_required
def projects():
    projects = Project.query.all()
    return render_template("admin/projects.html", projects=projects)


@admin.route("/projects/new", methods=["GET", "POST"])
@login_required
def new_project():
    if request.method == "POST":
        translations = {"es": {}}
        if request.form.get("title_es"):
            translations["es"]["title"] = request.form.get("title_es")
        if request.form.get("description_es"):
            translations["es"]["description"] = request.form.get("description_es")

        project = Project(
            title=request.form.get("title"),
            description=request.form.get("description"),
            technologies=request.form.get("technologies"),
            link=request.form.get("link"),
            demo=request.form.get("demo"),
            git_url=request.form.get("git_url"),
            git_icon=request.form.get("git_icon"),
            featured="featured" in request.form,
            translations=translations if translations["es"] else {},
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
        project.description = request.form.get("description")
        project.technologies = request.form.get("technologies")
        project.link = request.form.get("link")
        project.demo = request.form.get("demo")
        project.git_url = request.form.get("git_url")
        project.git_icon = request.form.get("git_icon")
        project.featured = "featured" in request.form

        translations = project.translations or {}
        if request.form.get("title_es"):
            translations["es"] = translations.get("es", {})
            translations["es"]["title"] = request.form.get("title_es")
        if request.form.get("description_es"):
            translations["es"] = translations.get("es", {})
            translations["es"]["description"] = request.form.get("description_es")
        project.translations = translations

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


# ============ Experience ============


@admin.route("/experience", methods=["GET"])
@login_required
def experiences():
    experiences = Experience.query.all()
    return render_template("admin/experiences.html", experiences=experiences)


@admin.route("/experience/new", methods=["GET", "POST"])
@login_required
def new_experience():
    if request.method == "POST":
        translations = {"es": {}}
        if request.form.get("title_es"):
            translations["es"]["title"] = request.form.get("title_es")
        if request.form.get("responsibilities_es"):
            translations["es"]["responsibilities"] = request.form.get(
                "responsibilities_es"
            )

        experience = Experience(
            title=request.form.get("title"),
            company=request.form.get("company"),
            period=request.form.get("period"),
            location=request.form.get("location"),
            responsibilities=request.form.get("responsibilities"),
            technologies=request.form.get("technologies"),
            translations=translations if translations["es"] else {},
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
        experience.company = request.form.get("company")
        experience.period = request.form.get("period")
        experience.location = request.form.get("location")
        experience.responsibilities = request.form.get("responsibilities")
        experience.technologies = request.form.get("technologies")

        translations = experience.translations or {}
        if request.form.get("title_es"):
            translations["es"] = translations.get("es", {})
            translations["es"]["title"] = request.form.get("title_es")
        if request.form.get("responsibilities_es"):
            translations["es"] = translations.get("es", {})
            translations["es"]["responsibilities"] = request.form.get(
                "responsibilities_es"
            )
        experience.translations = translations

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


# ============ Education ============


@admin.route("/education", methods=["GET"])
@login_required
def educations():
    educations = Education.query.all()
    return render_template("admin/educations.html", educations=educations)


@admin.route("/education/new", methods=["GET", "POST"])
@login_required
def new_education():
    if request.method == "POST":
        education = Education(
            degree=request.form.get("degree"),
            school=request.form.get("school"),
            year=request.form.get("year"),
        )
        db.session.add(education)
        db.session.commit()
        flash("Education created successfully!", "success")
        return redirect(url_for("admin.educations"))

    return render_template("admin/education_form.html", education=None)


@admin.route("/education/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_education(id):
    education = Education.query.get_or_404(id)

    if request.method == "POST":
        education.degree = request.form.get("degree")
        education.school = request.form.get("school")
        education.year = request.form.get("year")
        db.session.commit()
        flash("Education updated successfully!", "success")
        return redirect(url_for("admin.educations"))

    return render_template("admin/education_form.html", education=education)


@admin.route("/education/<int:id>/delete", methods=["POST"])
@login_required
def delete_education(id):
    education = Education.query.get_or_404(id)
    db.session.delete(education)
    db.session.commit()
    flash("Education deleted successfully!", "success")
    return redirect(url_for("admin.educations"))


# ============ Blog Posts ============


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

        translations = {"es": {}}
        if request.form.get("title_es"):
            translations["es"]["title"] = request.form.get("title_es")
        if request.form.get("excerpt_es"):
            translations["es"]["excerpt"] = request.form.get("excerpt_es")
        if request.form.get("content_es"):
            translations["es"]["content"] = request.form.get("content_es")

        post = BlogPost(
            title=request.form.get("title"),
            excerpt=request.form.get("excerpt"),
            content=request.form.get("content"),
            image=request.form.get("image"),
            author=request.form.get("author"),
            category=request.form.get("category"),
            date=post_date,
            translations=translations if translations["es"] else {},
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
        post.excerpt = request.form.get("excerpt")
        post.content = request.form.get("content")
        post.image = request.form.get("image")
        post.author = request.form.get("author")
        post.category = request.form.get("category")
        post.date = datetime.strptime(request.form.get("date"), "%Y-%m-%d").date()

        translations = post.translations or {}
        if request.form.get("title_es"):
            translations["es"] = translations.get("es", {})
            translations["es"]["title"] = request.form.get("title_es")
        if request.form.get("excerpt_es"):
            translations["es"] = translations.get("es", {})
            translations["es"]["excerpt"] = request.form.get("excerpt_es")
        if request.form.get("content_es"):
            translations["es"] = translations.get("es", {})
            translations["es"]["content"] = request.form.get("content_es")
        post.translations = translations

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


# ============ Skills ============


@admin.route("/skills", methods=["GET"])
@login_required
def skills():
    skills = Skill.query.all()
    return render_template("admin/skills.html", skills=skills)


@admin.route("/skills/new", methods=["GET", "POST"])
@login_required
def new_skill():
    if request.method == "POST":
        translations = {"es": {}}
        if request.form.get("name_es"):
            translations["es"]["name"] = request.form.get("name_es")

        skill = Skill(
            name=request.form.get("name"),
            icon=request.form.get("icon"),
            category=request.form.get("category"),
            translations=translations if translations["es"] else {},
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
        skill.icon = request.form.get("icon")
        skill.category = request.form.get("category")

        translations = skill.translations or {}
        if request.form.get("name_es"):
            translations["es"] = translations.get("es", {})
            translations["es"]["name"] = request.form.get("name_es")
        skill.translations = translations

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


# ============ Interests ============


@admin.route("/interests", methods=["GET"])
@login_required
def interests():
    interests = Interest.query.all()
    return render_template("admin/interests.html", interests=interests)


@admin.route("/interests/new", methods=["GET", "POST"])
@login_required
def new_interest():
    if request.method == "POST":
        interest = Interest(name=request.form.get("name"))
        db.session.add(interest)
        db.session.commit()
        flash("Interest created successfully!", "success")
        return redirect(url_for("admin.interests"))

    return render_template("admin/interest_form.html", interest=None)


@admin.route("/interests/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_interest(id):
    interest = Interest.query.get_or_404(id)

    if request.method == "POST":
        interest.name = request.form.get("name")
        db.session.commit()
        flash("Interest updated successfully!", "success")
        return redirect(url_for("admin.interests"))

    return render_template("admin/interest_form.html", interest=interest)


@admin.route("/interests/<int:id>/delete", methods=["POST"])
@login_required
def delete_interest(id):
    interest = Interest.query.get_or_404(id)
    db.session.delete(interest)
    db.session.commit()
    flash("Interest deleted successfully!", "success")
    return redirect(url_for("admin.interests"))


# ============ Social Links ============


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
            icon=request.form.get("icon"),
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


# ============ Contact Messages ============


@admin.route("/contact-messages", methods=["GET"])
@login_required
def contact_messages():
    messages_list = ContactMessage.query.order_by(
        ContactMessage.created_at.desc()
    ).all()
    return render_template("admin/contact_messages.html", messages_list=messages_list)


@admin.route("/contact-messages/<int:id>/delete", methods=["POST"])
@login_required
def delete_contact_message(id):
    message = ContactMessage.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    flash("Message deleted successfully!", "success")
    return redirect(url_for("admin.contact_messages"))
