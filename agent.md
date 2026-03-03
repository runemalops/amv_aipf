# AGENTS.md

## Project Overview
This project is a personal portfolio web application built with Flask, SQLAlchemy, and Bootstrap CSS. It includes sections for About Me, My Projects, Work Experience, Blog, Contact, with an admin panel for content management.

## Project Structure
*   `/`
    *   `app.py`: The main Flask application file.
    *   `routes.py`: URL routing definitions using Flask blueprints.
    *   `views.py`: View functions for rendering templates.
    *   `models.py`: SQLAlchemy database models.
    *   `auth.py`: Authentication routes (login/logout).
    *   `admin.py`: Admin panel routes for content management.
    *   `seed.py`: Script to seed initial data.
    *   `translation_service.py`: Translation service using MyMemory API.
    *   `translations.py`: Translation helper functions.
    *   `requirements.txt`: Project dependencies.
    *   `instance/portfolio.db`: SQLite database file.
    *   `migrations/`: Flask-Migrate database migrations.
    *   `templates/`: Directory for HTML templates.
    *   `translations/`: Language translation JSON files (en.json, es.json).
    *   `deploy/`: Deployment files (Containerfile, quadlet).

## Setup Commands
*   **Create and activate virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
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
*   **Run the application:**
    ```bash
    source venv/bin/activate
    python app.py
    ```

## Deployment Commands
*   **Build container image:**
    ```bash
    # Run from project root directory
    podman build -f deploy/Containerfile -t amv_aipf:latest .
    ```
*   **Prepare instance directory for persistent database:**
    ```bash
    mkdir -p ~/.local/share/amv_aipf/instance
    cp instance/portfolio.db ~/.local/share/amv_aipf/instance/
    ```
*   **Set up environment file for secrets:**
    ```bash
    mkdir -p ~/.local/share/amv_aipf
    echo "SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')" > ~/.local/share/amv_aipf/amv_aipf.env
    ```
*   **Update quadlet to use EnvironmentFile:**
    
    Edit `~/.config/containers/systemd/amv_aipf.container`:
    ```ini
    [Container]
    Image=amv_aipf:latest
    ContainerName=amv_aipf
    PublishPort=5000:5000
    Volume=%h/.local/share/amv_aipf/instance:/app/instance
    Environment=FLASK_APP=app.py
    Environment=FLASK_ENV=production
    EnvironmentFile=%h/.local/share/amv_aipf/amv_aipf.env

    [Service]
    Restart=always
    ```
*   **Deploy with Quadlet (systemd):**
    ```bash
    mkdir -p ~/.config/containers/systemd/
    cp deploy/amv_aipf.container ~/.config/containers/systemd/
    # Edit the quadlet file to add EnvironmentFile line as shown above
    systemctl --user daemon-reload
    systemctl --user start amv_aipf
    ```
*   **View container logs:**
    ```bash
    journalctl --user -u amv_aipf -f
    ```

## Database Models
*   `User`: Admin user for authentication
*   `Project`: Portfolio projects
*   `Experience`: Work experience
*   `Education`: Educational background
*   `BlogPost`: Blog posts
*   `Skill`: Technical skills with icons
*   `Interest`: Personal interests
*   `SocialLink`: Social media links
*   `ContactMessage`: Contact form messages

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
*   `/admin/experience` - Manage work experience
*   `/admin/blog` - Manage blog posts
*   `/admin/skills` - Manage skills
*   `/admin/social-links` - Manage social media links
*   `/admin/contact-messages` - View contact messages

## Icons
Uses [Bootstrap Icons](https://icons.getbootstrap.com/).

## Internationalization (i18n)
The application supports English and Spanish languages. Users can switch languages via the dropdown in the navigation bar.

### Translation Features:
- Static UI text: Stored in `translations/en.json` and `translations/es.json`
- Content translation: Projects, Experience, Skills, and Blog Posts support Spanish translations
- Auto-translate: Admin panel has "Auto-Translate from English" buttons for content

### Adding Translations:
1. Static text: Edit `translations/en.json` or `translations/es.json`
2. Content: Use admin panel to add Spanish translations to projects, experience, skills, and blog posts

### Language Routes:
- `/set-lang/en` - Switch to English
- `/set-lang/es` - Switch to Spanish

## Code Style
*   Follow [PEP 8](https://peps.python.org) style guidelines
*   Use type hinting where appropriate
*   Create database migrations when models change:
    ```bash
    flask db migrate -m "Description of changes"
    flask db upgrade
    ```

## Boundaries
*   All new features should include corresponding database migrations when models change
*   Test the application after making changes
