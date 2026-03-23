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
    *   `translation_utils.py`: Translation helpers with auto-translate fallback.
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
*   `Settings`: Key-value store for site configuration (SMTP, site content). Note: Site content fields need multilingual support (TODO).

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
*   `/admin/education` - Manage education
*   `/admin/blog` - Manage blog posts
*   `/admin/skills` - Manage skills
*   `/admin/interests` - Manage interests
*   `/admin/social-links` - Manage social media links
*   `/admin/contact-messages` - View contact messages
*   `/admin/settings` - Configure SMTP and site settings
*   `/admin/site-config` - Configure hero, about section, and site content

## Icons
Uses [Bootstrap Icons](https://icons.getbootstrap.com/).

## Internationalization (i18n)
The application supports English and Spanish languages. Users can switch languages via the dropdown in the navigation bar.

### Translation Architecture:
- **Static UI text**: Stored in `translations/en.json` and `translations/es.json`
- **Content translation**: Models use a `translations` JSON column with format:
  ```json
  {"es": {"title": "...", "description": "..."}}
  ```
- **Auto-translate fallback**: If a translation doesn't exist in the JSON, `translation_utils.py` will auto-translate using the MyMemory API and cache the result

### Adding Translations:
1. Static text: Edit `translations/en.json` or `translations/es.json`
2. Content: Add translations to the `translations` JSON column via admin or seed data

### Language Routes:
- `/set-lang/en` - Switch to English
- `/set-lang/es` - Switch to Spanish

### Multilingual Site Configuration (TODO):
The `/admin/site-config` page currently stores values as plain text without translation support.
**Required**: Update site configuration to support English and Spanish translations:
1. Store settings values as JSON: `{"en": "English text", "es": "Spanish text"}`
2. Add form fields for both languages in the admin template
3. Update `get_site_config()` to return the translated value based on current language
4. Follow the same pattern as other models with `translations` JSON column

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

## Deployment Workflow
After making changes and confirming they work locally or in the container:

1. **Rebuild the image:**
   ```bash
   podman build -t amv_aipf:latest -f deploy/Containerfile .
   ```

2. **Reload and restart the quadlet:**
   ```bash
   systemctl --user daemon-reload
   systemctl --user restart amv_aipf.service
   ```

3. **Verify the service is running:**
   ```bash
   systemctl --user status amv_aipf.service
   ```

4. **View logs if needed:**
   ```bash
   journalctl --user -u amv_aipf -f
   ```
