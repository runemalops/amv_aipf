from flask import render_template
from models import db, Project, Experience, Education, BlogPost, Skill, Interest


def get_featured_projects():
    projects = Project.query.filter_by(featured=True).all()
    return [
        {
            "title": p.title,
            "description": p.description,
            "technologies": p.technologies.split(",") if p.technologies else [],
            "link": p.link or "#"
        }
        for p in projects
    ]


def get_all_projects():
    projects = Project.query.all()
    return [
        {
            "title": p.title,
            "description": p.description,
            "technologies": p.technologies.split(",") if p.technologies else [],
            "link": p.link or "#",
            "demo": p.demo
        }
        for p in projects
    ]


def get_latest_posts():
    posts = BlogPost.query.order_by(BlogPost.date.desc()).limit(3).all()
    return [
        {
            "id": p.id,
            "title": p.title,
            "excerpt": p.excerpt,
            "date": p.date.strftime("%B %d, %Y")
        }
        for p in posts
    ]


def get_all_posts():
    posts = BlogPost.query.order_by(BlogPost.date.desc()).all()
    return [
        {
            "id": p.id,
            "title": p.title,
            "excerpt": p.excerpt,
            "content": p.content,
            "date": p.date.strftime("%B %d, %Y"),
            "author": p.author,
            "category": p.category
        }
        for p in posts
    ]


def get_skills():
    skills = Skill.query.all()
    return [s.name for s in skills]


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


def get_experience():
    experiences = Experience.query.order_by(Experience.id.desc()).all()
    return [
        {
            "title": e.title,
            "company": e.company,
            "period": e.period,
            "location": e.location or "",
            "responsibilities": e.responsibilities.split("\n") if e.responsibilities else [],
            "technologies": e.technologies.split(",") if e.technologies else []
        }
        for e in experiences
    ]


def render_index():
    return render_template(
        "index.html",
        featured_projects=get_featured_projects(),
        latest_posts=get_latest_posts()
    )


def render_about():
    return render_template(
        "about.html",
        skills=get_skills(),
        interests=get_interests(),
        education=get_education()
    )


def render_projects():
    return render_template(
        "projects.html",
        projects=get_all_projects()
    )


def render_experience():
    return render_template(
        "experience.html",
        experience=get_experience()
    )


def render_blog():
    return render_template(
        "blog.html",
        posts=get_all_posts()
    )


def render_blog_post(post_id):
    post = BlogPost.query.get(post_id)
    
    if not post:
        return "Post not found", 404
    
    posts = BlogPost.query.order_by(BlogPost.date.desc()).all()
    posts_sorted = list(posts)
    
    current_index = next((i for i, p in enumerate(posts_sorted) if p.id == post_id), None)
    
    prev_post = posts_sorted[current_index + 1] if current_index is not None and current_index + 1 < len(posts_sorted) else None
    next_post = posts_sorted[current_index - 1] if current_index is not None and current_index > 0 else None
    
    post_data = {
        "title": post.title,
        "content": post.content,
        "date": post.date.strftime("%B %d, %Y"),
        "author": post.author,
        "category": post.category
    }
    
    prev_data = {"id": prev_post.id, "title": prev_post.title} if prev_post else None
    next_data = {"id": next_post.id, "title": next_post.title} if next_post else None
    
    return render_template(
        "blog_post.html",
        post=post_data,
        prev_post=prev_data,
        next_post=next_data
    ), 200
