# AGENTS.md

## Project Overview
This project is a personal portfolio web application built with Flask, SQLAlchemy, and Bootstrap CSS. It includes sections for About Me, My Projects, Work Experience, Blog, Contact, with an admin panel for content management.

## Project Structure
*   `/`
    *   `app.py`: The main Flask application file.
    *   `routes.py`: URL routing definitions using Flask blueprints.
    *   `views.py`: Template rendering logic using database queries.
    *   `models.py`: SQLAlchemy database models.
    *   `auth.py`: Authentication routes (login/logout).
    *   `admin.py`: Admin panel routes for content management.
    *   `seed.py`: Script to seed initial data.
    *   `requirements.txt`: Project dependencies.
    *   `AGENTS.md`: This file.
    *   `instance/portfolio.db`: SQLite database file.
    *   `venv/`: Python virtual environment.
    *   `migrations/`: Flask-Migrate database migrations.
    *   `templates/`: Directory for HTML templates.
        *   `base.html`: Base template with Bootstrap CSS, Bootstrap Icons, and navigation.
        *   `index.html`: Home page with hero section, featured content, and latest blog posts.
        *   `about.html`: About Me section with skills (with icons) and education.
        *   `projects.html`: Portfolio of projects.
        *   `experience.html`: Work experience timeline.
        *   `blog.html`: Blog listing page.
        *   `blog_post.html`: Individual blog post template.
        *   `contact.html`: Contact form.
        *   `admin/`: Admin panel templates.

## Setup Commands
*   **Create and activate virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    # On Windows: venv\Scripts\activate
    ```
*   **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
*   **Run migrations:**
    ```bash
    flask db migrate -m "Migration description"
    flask db upgrade
    ```
*   **Seed initial data:**
    ```bash
    python seed.py
    ```
*   **Create admin user:**
    ```bash
    flask create-admin <username> <password>
    ```
*   **Run the application (in development mode):**
    ```bash
    source venv/bin/activate
    python app.py
    # Or: flask run
    ```

## Database Models
*   `User`: Admin user for authentication (id, username, password_hash, created_at).
*   `Project`: Portfolio projects (id, title, description, technologies, link, demo, featured, created_at).
*   `Experience`: Work experience (id, title, company, period, location, responsibilities, technologies, created_at).
*   `Education`: Educational background (id, degree, school, year, created_at).
*   `BlogPost`: Blog posts (id, title, excerpt, content, image, author, category, date, created_at).
*   `Skill`: Technical skills with icons (id, name, icon, category, created_at).
*   `Interest`: Personal interests (id, name, created_at).
*   `SocialLink`: Social media links (id, platform, url, icon, created_at).
*   `ContactMessage`: Contact form messages (id, name, email, subject, message, created_at).

## Routes
### Public
*   `/` - Home page
*   `/about` - About Me
*   `/projects` - My Projects
*   `/experience` - Work Experience
*   `/blog` - Blog listing
*   `/blog/<id>` - Individual blog post
*   `/contact` - Contact form

### Admin (requires login)
*   `/admin/login` - Admin login
*   `/admin/logout` - Admin logout
*   `/admin/` - Admin dashboard
*   `/admin/projects` - Manage projects
*   `/admin/projects/new` - Add project
*   `/admin/projects/<id>/edit` - Edit project
*   `/admin/experience` - Manage work experience
*   `/admin/experience/new` - Add experience
*   `/admin/experience/<id>/edit` - Edit experience
*   `/admin/blog` - Manage blog posts
*   `/admin/blog/new` - Add blog post
*   `/admin/blog/<id>/edit` - Edit blog post
*   `/admin/skills` - Manage skills
*   `/admin/skills/new` - Add skill
*   `/admin/skills/<id>/edit` - Edit skill
*   `/admin/social-links` - Manage social media links
*   `/admin/social-links/new` - Add social link
*   `/admin/contact-messages` - View contact messages

## Icons
The project uses [Bootstrap Icons](https://icons.getbootstrap.com/). Example icon classes:
*   GitHub: `bi-github`
*   YouTube: `bi-youtube`
*   LinkedIn: `bi-linkedin`
*   Twitter/X: `bi-twitter-x`
*   Email: `bi-envelope`
*   Python: `bi-python`
*   JavaScript: `bi-braces`
*   Code: `bi-code-slash`

## Testing Instructions
*   **Run the application:**
    ```bash
    source venv/bin/activate
    python app.py
    ```

## Code Style
*   Follow [PEP 8](https://peps.python.org) style guidelines for all Python code.
*   Use type hinting where appropriate.
*   When adding new features, create a database migration:
    ```bash
    flask db migrate -m "Description of changes"
    flask db upgrade
    ```

## Boundaries
*   All new features should include corresponding database migrations when models change.
*   Test the application after making changes.
