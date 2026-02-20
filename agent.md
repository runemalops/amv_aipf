# AGENTS.md

## Project Overview
This project is a personal portfolio web application built with Flask, SQLAlchemy, and Bootstrap CSS. It includes sections for About Me, My Projects, Work Experience, and Blog content, with an admin panel for content management.

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
    *   `portfolio.db`: SQLite database file.
    *   `venv/`: Python virtual environment.
    *   `migrations/`: Flask-Migrate database migrations.
    *   `templates/`: Directory for HTML templates.
        *   `base.html`: Base template with Bootstrap CSS and navigation.
        *   `index.html`: Home page with hero section and featured content.
        *   `about.html`: About Me section with skills and education.
        *   `projects.html`: Portfolio of projects.
        *   `experience.html`: Work experience timeline.
        *   `blog.html`: Blog listing page.
        *   `blog_post.html`: Individual blog post template.
        *   `admin/`: Admin panel templates.

## Setup Commands
*   **Create and activate virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    # On Windows: venv\\Scripts\\activate
    ```
*   **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
*   **Initialize database and run migrations:**
    ```bash
    flask db init
    flask db migrate -m "Initial migration"
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
    export FLASK_APP=app.py
    flask run
    ```

## Database Models
*   `User`: Admin user for authentication.
*   `Project`: Portfolio projects with title, description, technologies, links.
*   `Experience`: Work experience with company, period, responsibilities.
*   `Education`: Educational background.
*   `BlogPost`: Blog posts with title, content, category, date.
*   `Skill`: Technical skills.
*   `Interest`: Personal interests.

## Routes
### Public
*   `/` - Home page
*   `/about` - About Me
*   `/projects` - My Projects
*   `/experience` - Work Experience
*   `/blog` - Blog listing
*   `/blog/<id>` - Individual blog post

### Admin
*   `/admin/login` - Admin login
*   `/admin/logout` - Admin logout
*   `/admin/` - Admin dashboard
*   `/admin/projects` - Manage projects
*   `/admin/experience` - Manage work experience
*   `/admin/blog` - Manage blog posts
*   `/admin/skills` - Manage skills

## Testing Instructions
*   **Run unit tests (if applicable):**
    ```bash
    pip install pytest
    pytest
    ```

## Code Style
*   Follow [PEP 8](https://peps.python.org) style guidelines for all Python code.
*   Use type hinting where appropriate.
*   Prioritize small, focused commits.

## Boundaries
*   Do not modify the `templates/` directory unless explicitly instructed.
*   All new features should include corresponding tests.
