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
                title="Task Manager App",
                description="A full-featured task management application with user authentication, Kanban boards, and team collaboration.",
                technologies="Python,Flask,React,PostgreSQL",
                link="https://github.com/username/task-manager",
                demo="https://task-manager.demo.com",
                git_url="https://github.com/username/task-manager",
                git_icon="bi-github",
                featured=True
            ),
            Project(
                title="E-Commerce Platform",
                description="A complete online store with product catalog, shopping cart, checkout process, and admin dashboard.",
                technologies="Django,HTML/CSS,Stripe,AWS",
                link="https://github.com/username/ecommerce",
                demo="https://ecommerce.demo.com",
                git_url="https://github.com/username/ecommerce",
                git_icon="bi-github",
                featured=True
            ),
            Project(
                title="Real-Time Chat",
                description="A messaging application supporting individual and group chats, file sharing, and online status indicators.",
                technologies="Node.js,Socket.io,MongoDB,Redis",
                link="https://gitlab.com/username/chat-app",
                demo=None,
                git_url="https://gitlab.com/username/chat-app",
                git_icon="bi-git",
                featured=True
            ),
            Project(
                title="Portfolio Website",
                description="A responsive personal portfolio website showcasing projects, experience, and blog posts.",
                technologies="Flask,Bootstrap,HTML/CSS",
                link="https://github.com/username/portfolio",
                demo="https://portfolio.demo.com",
                git_url="https://github.com/username/portfolio",
                git_icon="bi-github",
                featured=False
            ),
            Project(
                title="Weather Dashboard",
                description="A weather application that displays current conditions and forecasts using a weather API.",
                technologies="JavaScript,OpenWeather API,CSS",
                link="https://bitbucket.org/username/weather-dashboard",
                demo="https://weather.demo.com",
                git_url="https://bitbucket.org/username/weather-dashboard",
                git_icon="bi-git",
                featured=False
            ),
            Project(
                title="Blog CMS",
                description="A content management system for blogging with markdown support, categories, and commenting.",
                technologies="Flask,SQLAlchemy,Markdown",
                link="https://github.com/username/blog-cms",
                demo=None,
                git_url="https://github.com/username/blog-cms",
                git_icon="bi-github",
                featured=False
            ),
        ]

        experiences = [
            Experience(
                title="Software Engineering Manager",
                company="PayPal Inc.",
                period="May 2021 - Present",
                location="Guatemala, C.A.",
                responsibilities="Led a team of software engineers to successfully develop a major software project on time and on budget, focused on Google Cloud Platform Provider, delivering a Google Kubernetes Engine environment that enables Git-ops model-oriented deployments.\nImplemented a set of best practices and documented procedures for software deployment, resulting in increased accuracy and reliability of software products.\nImproved compliance with security standards which increased SLA compliance from 60% to 99%, which allowed better performance in Coalfire and PCI DSS compliance.",
                technologies="GCP,Golang,Terraform,Docker,OL8"
            ),
            Experience(
                title="Software Engineer",
                company="PayPal Inc.",
                period="November 2015 - April 2021",
                location="Guatemala, C.A.",
                responsibilities="Provide support for monitoring tools for software and infrastructure development teams.\nDeveloped custom software tools to automate application and virtual machine monitoring, enabling proactive issue resolution.\nReviewed software requirements and provided feedback to ensure the software meets customer needs.\nDebugging Software problems, identifying root causes and proposed solutions to software problems",
                technologies="Django,PostgreSQL,JavaScript"
            ),
            Experience(
                title="Customer Engineer",
                company="Cognizant Technology Solutions",
                period="March 2014 - October 2015",
                location="Guatemala, C.A.",
                responsibilities="Research and identify the root cause of customer issues and provide detailed reports to stakeholders.\nSupported the development and testing of new software applications, ensuring a smooth transition to production.\nProvided technical support to customers via phone and email, resulting in a 99.95% customer satisfaction rate.\nEstablished and maintained monitoring systems that identified and resolved system issues before customers were affected.\nDeveloped and implemented policies and procedures to ensure data integrity and security.",
                technologies="JavaScript,HTML/CSS,PHP"
            ),
        ]

        education = [
            Education(
                degree="Bachelor of Science in Computer Science",
                school="University of Technology",
                year="2018 - 2022"
            ),
        ]

        blog_posts = [
            BlogPost(
                title="Getting Started with Flask",
                excerpt="Learn how to build your first web application with Flask framework.",
                content="<p>Flask is a lightweight WSGI web application framework in Python. It's designed to make getting started quick and easy, with the ability to scale up to complex applications.</p><h3>Why Flask?</h3><p>Flask is beginner-friendly and provides the essentials without imposing constraints.</p><h3>Key Features</h3><ul><li>Lightweight and flexible</li><li>Built-in development server</li><li>RESTful request handling</li><li>Extensible with plugins</li></ul>",
                author="Your Name",
                category="Python",
                date=date(2026, 1, 15)
            ),
            BlogPost(
                title="Best Practices for REST APIs",
                excerpt="Essential tips for designing clean and efficient REST APIs.",
                content="<p>REST APIs are the backbone of modern web applications.</p><h3>Key Principles</h3><ul><li>Use proper HTTP methods</li><li>Return appropriate status codes</li><li>Use consistent naming</li><li>Implement error handling</li></ul>",
                author="Your Name",
                category="API Design",
                date=date(2026, 1, 10)
            ),
            BlogPost(
                title="Introduction to Docker",
                excerpt="Containerize your applications for consistent deployment.",
                content="<p>Docker allows you to package applications into containers.</p><h3>Benefits</h3><ul><li>Consistent environments</li><li>Isolation</li><li>Easy deployment</li><li>Scalability</li></ul>",
                author="Your Name",
                category="DevOps",
                date=date(2026, 1, 5)
            ),
            BlogPost(
                title="Web Security Fundamentals",
                excerpt="Essential security practices for web developers.",
                content="<p>Security should be a top priority.</p><h3>Common Threats</h3><ul><li>SQL Injection</li><li>XSS</li><li>CSRF</li><li>Password security</li></ul>",
                author="Your Name",
                category="Security",
                date=date(2025, 12, 20)
            ),
            BlogPost(
                title="Modern CSS Techniques",
                excerpt="Explore modern CSS features like Flexbox and Grid.",
                content="<p>CSS has evolved significantly.</p><h3>Key Technologies</h3><ul><li>Flexbox</li><li>CSS Grid</li><li>Custom properties</li><li>Animations</li></ul>",
                author="Your Name",
                category="Frontend",
                date=date(2025, 12, 15)
            ),
            BlogPost(
                title="Database Design Patterns",
                excerpt="Learn effective database design for scalable applications.",
                content="<p>Good database design is crucial.</p><h3>Best Practices</h3><ul><li>Normalize data</li><li>Use indexes</li><li>Implement relationships</li><li>Plan for scalability</li></ul>",
                author="Your Name",
                category="Database",
                date=date(2025, 12, 10)
            ),
        ]

        skills = [
            Skill(name="Python", icon="bi-python", category="Backend"),
            Skill(name="JavaScript", category="Frontend"),
            Skill(name="Flask", category="Backend"),
            Skill(name="Django", category="Backend"),
            Skill(name="React", category="Frontend"),
            Skill(name="HTML/CSS", category="Frontend"),
            Skill(name="PostgreSQL", category="Database"),
            Skill(name="MongoDB", category="Database"),
            Skill(name="Git", category="Tools"),
            Skill(name="Docker", icon="bi-docker", category="IaC"),
            Skill(name="AWS", category="Cloud"),
            Skill(name="Terraform", icon="bi-terraform", category="IaC"),
        ]

        interests = [
            Interest(name="Open Source"),
            Interest(name="Machine Learning"),
            Interest(name="Cloud Computing"),
            Interest(name="Web Development"),
            Interest(name="Mobile Apps"),
            Interest(name="Cybersecurity"),
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
