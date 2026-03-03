from flask import render_template, request, flash, redirect, url_for
from models import db, Project, Experience, Education, BlogPost, Skill, Interest, SocialLink, ContactMessage


def get_featured_projects(lang='en'):
    projects = Project.query.filter_by(featured=True).all()
    return [
        {
            "title": p.title_es if lang == 'es' and p.title_es else p.title,
            "description": p.description_es if lang == 'es' and p.description_es else p.description,
            "technologies": p.technologies.split(",") if p.technologies else [],
            "link": p.link or "#",
            "demo": p.demo,
            "git_url": p.git_url,
            "git_icon": p.git_icon
        }
        for p in projects
    ]


def get_all_projects(lang='en'):
    projects = Project.query.all()
    return [
        {
            "title": p.title_es if lang == 'es' and p.title_es else p.title,
            "description": p.description_es if lang == 'es' and p.description_es else p.description,
            "technologies": p.technologies.split(",") if p.technologies else [],
            "link": p.link or "#",
            "demo": p.demo,
            "git_url": p.git_url,
            "git_icon": p.git_icon
        }
        for p in projects
    ]


def get_latest_posts(lang='en'):
    posts = BlogPost.query.order_by(BlogPost.date.desc()).limit(3).all()
    return [
        {
            "id": p.id,
            "title": p.title_es if lang == 'es' and p.title_es else p.title,
            "excerpt": p.excerpt_es if lang == 'es' and p.excerpt_es else p.excerpt,
            "image": p.image,
            "date": p.date.strftime("%B %d, %Y")
        }
        for p in posts
    ]


def get_all_posts(lang='en'):
    posts = BlogPost.query.order_by(BlogPost.date.desc()).all()
    return [
        {
            "id": p.id,
            "title": p.title_es if lang == 'es' and p.title_es else p.title,
            "excerpt": p.excerpt_es if lang == 'es' and p.excerpt_es else p.excerpt,
            "image": p.image,
            "content": p.content_es if lang == 'es' and p.content_es else p.content,
            "date": p.date.strftime("%B %d, %Y"),
            "author": p.author,
            "category": p.category
        }
        for p in posts
    ]


def get_skills(lang='en'):
    skills = Skill.query.all()
    return [{"name": s.name_es if lang == 'es' and s.name_es else s.name, "icon": s.icon} for s in skills]


def get_social_links():
    links = SocialLink.query.all()
    return [{"platform": l.platform, "url": l.url, "icon": l.icon} for l in links]


def get_interests():
    interests = Interest.query.all()
    return [i.name for i in interests]


def get_education():
    education = Education.query.all()
    return [
        {
            "degree": e.degree,
            "school": e.school,
            "year": e.year
        }
        for e in education
    ]


def get_experience(lang='en'):
    experiences = Experience.query.order_by(Experience.id.desc()).all()
    return [
        {
            "title": e.title_es if lang == 'es' and e.title_es else e.title,
            "company": e.company,
            "period": e.period,
            "location": e.location or "",
            "responsibilities": (e.responsibilities_es if lang == 'es' and e.responsibilities_es else e.responsibilities).split("\n") if (e.responsibilities_es if lang == 'es' and e.responsibilities_es else e.responsibilities) else [],
            "technologies": e.technologies.split(",") if e.technologies else []
        }
        for e in experiences
    ]


def render_index():
    from flask import session
    lang = session.get('lang', 'en')
    return render_template(
        "index.html",
        featured_projects=get_featured_projects(lang),
        latest_posts=get_latest_posts(lang),
        social_links=get_social_links()
    )


def render_about():
    from flask import session
    lang = session.get('lang', 'en')
    return render_template(
        "about.html",
        skills=get_skills(lang),
        interests=get_interests(),
        education=get_education(),
        social_links=get_social_links()
    )


def render_projects():
    from flask import session
    lang = session.get('lang', 'en')
    return render_template(
        "projects.html",
        projects=get_all_projects(lang)
    )


def render_experience():
    from flask import session
    lang = session.get('lang', 'en')
    return render_template(
        "experience.html",
        experience=get_experience(lang)
    )


def render_blog():
    from flask import session
    lang = session.get('lang', 'en')
    return render_template(
        "blog.html",
        posts=get_all_posts(lang)
    )


def render_blog_post(post_id):
    from flask import session
    lang = session.get('lang', 'en')
    
    post = BlogPost.query.get(post_id)
    
    if not post:
        return "Post not found", 404
    
    posts = BlogPost.query.order_by(BlogPost.date.desc()).all()
    posts_sorted = list(posts)
    
    current_index = next((i for i, p in enumerate(posts_sorted) if p.id == post_id), None)
    
    prev_post = posts_sorted[current_index + 1] if current_index is not None and current_index + 1 < len(posts_sorted) else None
    next_post = posts_sorted[current_index - 1] if current_index is not None and current_index > 0 else None
    
    post_data = {
        "title": post.title_es if lang == 'es' and post.title_es else post.title,
        "content": post.content_es if lang == 'es' and post.content_es else post.content,
        "image": post.image,
        "date": post.date.strftime("%B %d, %Y"),
        "author": post.author,
        "category": post.category
    }
    
    prev_lang_title = prev_post.title_es if lang == 'es' and prev_post.title_es else prev_post.title if prev_post else None
    next_lang_title = next_post.title_es if lang == 'es' and next_post.title_es else next_post.title if next_post else None
    
    prev_data = {"id": prev_post.id, "title": prev_lang_title} if prev_post else None
    next_data = {"id": next_post.id, "title": next_lang_title} if next_post else None
    
    return render_template(
        "blog_post.html",
        post=post_data,
        prev_post=prev_data,
        next_post=next_data,
        social_links=get_social_links()
    ), 200


def render_contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")
        
        contact = ContactMessage(name=name, email=email, subject=subject, message=message)
        db.session.add(contact)
        db.session.commit()
        flash("Message sent successfully!", "success")
        return redirect(url_for("main.contact"))
    
    return render_template(
        "contact.html",
        social_links=get_social_links()
    )
