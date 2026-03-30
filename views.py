from flask import (
    render_template,
    request,
    flash,
    redirect,
    url_for,
    session,
    current_app,
)
from flask_mail import Message
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
from translation_utils import (
    get_translated,
    get_translated_list,
    get_education_list,
    get_interests_list,
    get_social_links_list,
)


def get_featured_projects(lang="en"):
    projects = (
        Project.query.filter_by(featured=True).order_by(Project.created_at.desc()).all()
    )
    return get_translated_list(projects, ["title", "description"], lang)


def get_all_projects(lang="en"):
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return get_translated_list(projects, ["title", "description"], lang)


def get_latest_posts(lang="en"):
    posts = BlogPost.query.order_by(BlogPost.date.desc()).limit(3).all()
    result = []
    for p in posts:
        result.append(
            {
                "id": p.id,
                "title": get_translated(p, "title", lang),
                "excerpt": get_translated(p, "excerpt", lang),
                "image": p.image,
                "date": p.date.strftime("%B %d, %Y") if p.date else "",
            }
        )
    return result


def get_all_posts(lang="en"):
    posts = BlogPost.query.order_by(BlogPost.date.desc()).all()
    result = []
    for p in posts:
        result.append(
            {
                "id": p.id,
                "title": get_translated(p, "title", lang),
                "excerpt": get_translated(p, "excerpt", lang),
                "image": p.image,
                "content": get_translated(p, "content", lang),
                "date": p.date.strftime("%B %d, %Y") if p.date else "",
                "author": p.author,
                "category": p.category,
            }
        )
    return result


def get_skills(lang="en"):
    skills = Skill.query.all()
    return [{"name": get_translated(s, "name", lang), "icon": s.icon} for s in skills]


def get_social_links(lang="en"):
    links = SocialLink.query.all()
    return get_social_links_list(links, lang)


def get_interests(lang="en"):
    interests = Interest.query.all()
    return get_interests_list(interests, lang)


def get_education(lang="en"):
    education = Education.query.all()
    return get_education_list(education, lang)


def get_experience(lang="en"):
    experiences = Experience.query.order_by(Experience.created_at.desc()).all()
    result = []
    for e in experiences:
        responsibilities = get_translated(e, "responsibilities", lang)
        result.append(
            {
                "title": get_translated(e, "title", lang),
                "company": e.company,
                "period": e.period,
                "location": e.location or "",
                "responsibilities": responsibilities.split("\n")
                if responsibilities
                else [],
                "technologies": e.technologies.split(",") if e.technologies else [],
            }
        )
    return result


def get_site_config(lang="en"):
    return {
        "site_title": Settings.get_translated("site_title", lang, "Your Name"),
        "site_subtitle": Settings.get_translated(
            "site_subtitle", lang, "Your Title | Your Profession"
        ),
        "hero_title": Settings.get_translated("hero_title", lang, "Your Hero Headline"),
        "hero_cta_text": Settings.get_translated("hero_cta_text", lang, "View My Work"),
        "hero_cta_link": Settings.get("hero_cta_link", "/projects"),
        "hero_cta_secondary_text": Settings.get_translated(
            "hero_cta_secondary_text", lang, "Download CV"
        ),
        "hero_cta_secondary_link": Settings.get("hero_cta_secondary_link", "#"),
        "what_i_do_title": Settings.get_translated(
            "what_i_do_title", lang, "What I Do"
        ),
        "what_i_do_subtitle": Settings.get_translated(
            "what_i_do_subtitle", lang, "Describe what you do"
        ),
        "feature1_title": Settings.get_translated("feature1_title", lang, "Feature 1"),
        "feature1_desc": Settings.get_translated(
            "feature1_desc", lang, "Feature description"
        ),
        "feature2_title": Settings.get_translated("feature2_title", lang, "Feature 2"),
        "feature2_desc": Settings.get_translated(
            "feature2_desc", lang, "Feature description"
        ),
        "feature3_title": Settings.get_translated("feature3_title", lang, "Feature 3"),
        "feature3_desc": Settings.get_translated(
            "feature3_desc", lang, "Feature description"
        ),
        "about_badge": Settings.get_translated("about_badge", lang, "Get To Know Me"),
        "about_intro": Settings.get_translated(
            "about_intro", lang, "Your Professional Title"
        ),
        "about_description1": Settings.get_translated(
            "about_description1", lang, "Write your first description here."
        ),
        "about_description2": Settings.get_translated(
            "about_description2", lang, "Write your second description here."
        ),
        "about_image": Settings.get("about_image", ""),
        "cv_download_link": Settings.get("cv_download_link", ""),
        "projects_subtitle": Settings.get_translated(
            "projects_subtitle", lang, "Showcase your work"
        ),
        "blog_subtitle": Settings.get_translated(
            "blog_subtitle", lang, "Share your insights"
        ),
        "cta_title": Settings.get_translated("cta_title", lang, "Let's Work Together"),
        "cta_text": Settings.get_translated(
            "cta_text", lang, "Have a project in mind? Let's discuss."
        ),
    }


def render_index():
    lang = session.get("lang", "en")
    return render_template(
        "index.html",
        featured_projects=get_featured_projects(lang),
        latest_posts=get_latest_posts(lang),
        social_links=get_social_links(lang),
        site_config=get_site_config(lang),
    )


def render_about():
    lang = session.get("lang", "en")
    return render_template(
        "about.html",
        skills=get_skills(lang),
        interests=get_interests(lang),
        education=get_education(lang),
        social_links=get_social_links(lang),
        site_config=get_site_config(lang),
    )


def render_projects():
    lang = session.get("lang", "en")
    return render_template("projects.html", projects=get_all_projects(lang))


def render_experience():
    lang = session.get("lang", "en")
    return render_template("experience.html", experience=get_experience(lang))


def render_blog():
    lang = session.get("lang", "en")
    return render_template("blog.html", posts=get_all_posts(lang))


def render_blog_post(post_id):
    lang = session.get("lang", "en")

    post = BlogPost.query.get(post_id)

    if not post:
        return "Post not found", 404

    posts = BlogPost.query.order_by(BlogPost.date.desc()).all()
    posts_sorted = list(posts)

    current_index = next(
        (i for i, p in enumerate(posts_sorted) if p.id == post_id), None
    )

    prev_post = (
        posts_sorted[current_index + 1]
        if current_index is not None and current_index + 1 < len(posts_sorted)
        else None
    )
    next_post = (
        posts_sorted[current_index - 1]
        if current_index is not None and current_index > 0
        else None
    )

    post_data = {
        "title": get_translated(post, "title", lang),
        "content": get_translated(post, "content", lang),
        "image": post.image,
        "date": post.date.strftime("%B %d, %Y") if post.date else "",
        "author": post.author,
        "category": post.category,
    }

    prev_lang_title = get_translated(prev_post, "title", lang) if prev_post else None
    next_lang_title = get_translated(next_post, "title", lang) if next_post else None

    prev_data = {"id": prev_post.id, "title": prev_lang_title} if prev_post else None
    next_data = {"id": next_post.id, "title": next_lang_title} if next_post else None

    return render_template(
        "blog_post.html",
        post=post_data,
        prev_post=prev_data,
        next_post=next_data,
        social_links=get_social_links(lang),
    ), 200


def render_contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")

        contact = ContactMessage(
            name=name, email=email, subject=subject, message=message
        )
        db.session.add(contact)
        db.session.commit()

        recipient = Settings.get("contact_recipient", "")
        smtp_server = Settings.get("smtp_server", "")

        if recipient and smtp_server:
            try:
                from app import mail

                msg = Message(
                    subject=f"Contact Form: {subject}",
                    recipients=[recipient],
                    body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
                )
                mail.send(msg)
            except Exception as e:
                current_app.logger.error(f"Failed to send email: {e}")

        flash("Message sent successfully!", "success")
        return redirect(url_for("main.contact"))

    return render_template(
        "contact.html", social_links=get_social_links(session.get("lang", "en"))
    )
