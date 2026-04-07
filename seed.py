from datetime import date
from app import app
from models import db, Project, Experience, Education, BlogPost, Skill, Interest


def seed_data():
    with app.app_context():
        if Project.query.first():
            print("Database already seeded. Skipping...")
            return

        projects = [
            Project(
                title="Sample Project",
                description="A sample project demonstrating key features and technologies.",
                technologies="Python,Flask,SQLAlchemy",
                link="#",
                demo="#",
                git_url="#",
                git_icon="bi-github",
                featured=True,
            ),
            Project(
                title="Another Project",
                description="Another demonstration project with different technologies.",
                technologies="JavaScript,React,PostgreSQL",
                link="#",
                demo="#",
                git_url="#",
                git_icon="bi-github",
                featured=True,
            ),
            Project(
                title="Third Project",
                description="A third sample project to showcase your work.",
                technologies="Django,Bootstrap,Docker",
                link="#",
                demo=None,
                git_url="#",
                git_icon="bi-github",
                featured=False,
            ),
        ]

        experiences = [
            Experience(
                title="Senior Developer",
                company="Company Name",
                period="2020 - Present",
                location="City, Country",
                responsibilities="Describe your role and responsibilities here.\nAdd more details on a new line.",
                technologies="Python,JavaScript,Docker",
            ),
            Experience(
                title="Junior Developer",
                company="Company Name",
                period="2018 - 2020",
                location="City, Country",
                responsibilities="Describe your role and responsibilities here.\nAdd more details on a new line.",
                technologies="Python,Flask,PostgreSQL",
            ),
        ]

        education = [
            Education(
                degree="Bachelor's Degree", school="University Name", year="2014 - 2018"
            ),
        ]

        blog_posts = [
            BlogPost(
                title="Welcome to My Blog",
                excerpt="This is a sample blog post. Add your content here.",
                content="<p>This is sample content for your blog post. Replace it with your own content.</p>",
                author="Your Name",
                category="General",
                date=date(2026, 1, 1),
            ),
            BlogPost(
                title="Another Blog Post",
                excerpt="Another sample post to get you started.",
                content="<p>More sample content goes here. You can use HTML for formatting.</p>",
                author="Your Name",
                category="General",
                date=date(2026, 1, 15),
            ),
        ]

        skills = [
            Skill(name="Python", icon="bi-filetype-py", category="Backend"),
            Skill(name="JavaScript", icon="bi-braces", category="Frontend"),
            Skill(name="HTML/CSS", icon="bi-filetype-html", category="Frontend"),
            Skill(name="PostgreSQL", icon="bi-database-fill", category="Database"),
            Skill(name="Git", icon="bi-git", category="Tools"),
            Skill(name="Docker", icon="bi-box-seam-fill", category="DevOps"),
        ]

        interests = [
            Interest(name="Coding", icon="bi-code-square"),
            Interest(name="Open Source", icon="bi-github"),
            Interest(name="Cloud Computing", icon="bi-cloud"),
            Interest(name="Machine Learning", icon="bi-brain"),
            Interest(name="Cybersecurity", icon="bi-shield-lock"),
            Interest(name="Web Development", icon="bi-globe"),
            Interest(name="Mobile Apps", icon="bi-phone"),
            Interest(name="Music", icon="bi-music-note"),
            Interest(name="Motorcycles", icon="bi-bicycle"),
            Interest(name="Cars", icon="bi-car-front"),
            Interest(name="Video Games", icon="bi-controller"),
            Interest(name="Photography", icon="bi-camera"),
            Interest(name="Hiking", icon="bi-compass"),
        ]

        db.session.add_all(projects)
        db.session.add_all(experiences)
        db.session.add_all(education)
        db.session.add_all(blog_posts)
        db.session.add_all(skills)
        db.session.add_all(interests)
        db.session.commit()
        print("Database seeded successfully!")


if __name__ == "__main__":
    seed_data()
