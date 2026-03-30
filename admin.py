from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    jsonify,
    current_app,
)
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
    Settings,
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
        translations = {"es": {}}
        if request.form.get("degree_es"):
            translations["es"]["degree"] = request.form.get("degree_es")
        if request.form.get("school_es"):
            translations["es"]["school"] = request.form.get("school_es")

        education = Education(
            degree=request.form.get("degree"),
            school=request.form.get("school"),
            year=request.form.get("year"),
            translations=translations if translations["es"] else {},
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

        translations = education.translations or {}
        if request.form.get("degree_es"):
            translations["es"] = translations.get("es", {})
            translations["es"]["degree"] = request.form.get("degree_es")
        if request.form.get("school_es"):
            translations["es"] = translations.get("es", {})
            translations["es"]["school"] = request.form.get("school_es")
        education.translations = translations

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
        translations = {"es": {}}
        if request.form.get("name_es"):
            translations["es"]["name"] = request.form.get("name_es")

        interest = Interest(
            name=request.form.get("name"),
            translations=translations if translations["es"] else {},
        )
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

        translations = interest.translations or {}
        if request.form.get("name_es"):
            translations["es"] = translations.get("es", {})
            translations["es"]["name"] = request.form.get("name_es")
        interest.translations = translations

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
        translations = {"es": {}}
        if request.form.get("platform_es"):
            translations["es"]["platform"] = request.form.get("platform_es")

        link = SocialLink(
            platform=request.form.get("platform"),
            url=request.form.get("url"),
            icon=request.form.get("icon"),
            translations=translations if translations["es"] else {},
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

        translations = link.translations or {}
        if request.form.get("platform_es"):
            translations["es"] = translations.get("es", {})
            translations["es"]["platform"] = request.form.get("platform_es")
        link.translations = translations

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


# ============ Settings ============


@admin.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "POST":
        smtp_fields = [
            "smtp_server",
            "smtp_port",
            "smtp_username",
            "smtp_password",
            "smtp_sender",
            "smtp_tls",
            "contact_recipient",
        ]
        for field in smtp_fields:
            value = request.form.get(field, "")
            Settings.set(field, value)

        current_app.config["MAIL_SERVER"] = Settings.get("smtp_server", "")
        current_app.config["MAIL_PORT"] = int(Settings.get("smtp_port") or 587)
        current_app.config["MAIL_USE_TLS"] = (
            Settings.get("smtp_tls", "true").lower() == "true"
        )
        current_app.config["MAIL_USERNAME"] = Settings.get("smtp_username", "")
        current_app.config["MAIL_PASSWORD"] = Settings.get("smtp_password", "")
        current_app.config["MAIL_DEFAULT_SENDER"] = Settings.get("smtp_sender", "")

        flash("Settings saved successfully!", "success")
        return redirect(url_for("admin.settings"))

    smtp_fields = {
        "smtp_server": Settings.get("smtp_server", ""),
        "smtp_port": Settings.get("smtp_port", "587"),
        "smtp_username": Settings.get("smtp_username", ""),
        "smtp_password": Settings.get("smtp_password", ""),
        "smtp_sender": Settings.get("smtp_sender", ""),
        "smtp_tls": Settings.get("smtp_tls", "true"),
        "contact_recipient": Settings.get("contact_recipient", ""),
    }

    return render_template("admin/settings.html", settings=smtp_fields)


@admin.route("/site-config", methods=["GET", "POST"])
@login_required
def site_config():
    if request.method == "POST":
        non_translatable_fields = [
            "hero_cta_link",
            "hero_cta_secondary_link",
            "about_image",
            "cv_download_link",
        ]
        translatable_fields = [
            "site_title",
            "site_subtitle",
            "hero_title",
            "hero_cta_text",
            "hero_cta_secondary_text",
            "what_i_do_title",
            "what_i_do_subtitle",
            "feature1_title",
            "feature1_desc",
            "feature2_title",
            "feature2_desc",
            "feature3_title",
            "feature3_desc",
            "about_badge",
            "about_intro",
            "about_description1",
            "about_description2",
            "projects_subtitle",
            "blog_subtitle",
            "cta_title",
            "cta_text",
        ]

        for field in non_translatable_fields:
            value = request.form.get(field, "")
            Settings.set(field, value)

        for field in translatable_fields:
            value = request.form.get(field, "")
            es_value = request.form.get(f"{field}_es", "")
            setting = Settings.query.filter_by(key=field).first()
            if setting:
                setting.value = value
                if es_value:
                    translations = setting.translations or {}
                    translations["es"] = es_value
                    setting.translations = translations
            else:
                setting = Settings(
                    key=field,
                    value=value,
                    translations={"es": es_value} if es_value else {},
                )
                db.session.add(setting)
            db.session.commit()

        flash("Site configuration saved successfully!", "success")
        return redirect(url_for("admin.site_config"))

    site_fields = {
        "site_title": Settings.get("site_title", "Your Name"),
        "site_subtitle": Settings.get("site_subtitle", "Your Title | Your Profession"),
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
        "projects_subtitle": Settings.get("projects_subtitle", "Showcase your work"),
        "blog_subtitle": Settings.get("blog_subtitle", "Share your insights"),
        "cta_title": Settings.get("cta_title", "Let's Work Together"),
        "cta_text": Settings.get("cta_text", "Have a project in mind? Let's discuss."),
    }

    site_fields_es = {}
    for key in site_fields:
        setting = Settings.query.filter_by(key=key).first()
        if setting and setting.translations:
            site_fields_es[key] = setting.translations.get("es", "")
        else:
            site_fields_es[key] = ""

    return render_template(
        "admin/site_config.html", config=site_fields, config_es=site_fields_es
    )


@admin.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if not current_user.check_password(current_password):
            flash("Current password is incorrect.", "danger")
            return redirect(url_for("admin.change_password"))

        if new_password != confirm_password:
            flash("New passwords do not match.", "danger")
            return redirect(url_for("admin.change_password"))

        if len(new_password) < 6:
            flash("New password must be at least 6 characters.", "danger")
            return redirect(url_for("admin.change_password"))

        current_user.set_password(new_password)
        db.session.commit()
        flash("Password changed successfully!", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/change_password.html")
