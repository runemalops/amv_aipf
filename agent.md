# AGENTS.md

## Project Overview
This project is a personal portfolio web application built with Flask, SQLAlchemy, and Bootstrap CSS. It includes sections for About Me, My Projects, Work Experience, Blog, Contact, with an admin panel for content management.

## Project Structure
*   `/`
    *   `app.py`: The main Flask application file.
    *   `routes.py`: URL routing definitions using Flask blueprints.
    *   `models.py`: SQLAlchemy database models.
    *   `auth.py`: Authentication routes (login/logout).
    *   `admin.py`: Admin panel routes for content management.
    *   `seed.py`: Script to seed initial data.
    *   `requirements.txt`: Project dependencies.
    *   `instance/portfolio.db`: SQLite database file.
    *   `migrations/`: Flask-Migrate database migrations.
    *   `templates/`: Directory for HTML templates.
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
    ContainerName=portfolio
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
