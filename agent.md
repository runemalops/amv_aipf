# AGENTS.md

## Project Overview
This project is a personal portfolio web application built with Flask, SQLAlchemy, and Bootstrap CSS with React islands for interactive components. It includes sections for About Me, My Projects, Work Experience, Blog, Contact, with an admin panel for content management.

## Architecture Layers

### Flask-React Hybrid Architecture

| Section | Approach | Reason |
|---------|----------|--------|
| Header/Footer | Flask/Jinja | Static, SEO-critical |
| Project Grid | **React** | Technology filtering, animations |
| Contact Form | **React** | Client-side validation, async submit |
| Blog Posts | Flask | SEO-friendly content |
| About/Education | Flask | Simple display |

### API Endpoints for React

React components communicate via REST API:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/projects` | GET | List all projects |
| `/api/projects?featured=true` | GET | Featured projects only |
| `/api/blog` | GET | Blog posts |
| `/api/blog?limit=3` | GET | Limited posts |
| `/api/experience` | GET | Work experience |
| `/api/education` | GET | Education |
| `/api/skills` | GET | Skills |
| `/api/contact` | POST | Submit contact form |
| `/api/csrf-token` | GET | CSRF token for forms |

React files are in `/react/` with Vite for building. The Flask-React hybrid uses a "React Islands" pattern where only interactive components are React-powered.

### Layer 1: Flask Application (app.py)
- Initializes Flask app with configuration
- Registers blueprints: `main`, `auth`, `admin`
- Sets up extensions: `db`, `migrate`, `login_manager`, `mail`
- **Context Processors**: Injects `site_config` and `t()` function to ALL templates automatically
- **Language Handling**: `get_locale()` detects language from session or browser

### Layer 2: Routes/Blueprints (routes.py, auth.py, admin.py)
- **routes.py**: Public URL definitions (`/`, `/about`, `/projects`, etc.)
- **auth.py**: Authentication routes (login/logout)
- **admin.py**: All admin CRUD operations with translation support

### Layer 3: Views (views.py)
- Contains business logic functions (`render_index()`, `render_about()`, etc.)
- Fetches data using model methods
- Calls translation functions with current language
- Returns `render_template()` with translated data

### Layer 4: Models (models.py)
- SQLAlchemy ORM models
- Most models have `translations` JSON column
- `Settings` model uses `get_translated()` for multilingual site content

### Layer 5: Translation Utilities
- **translations.py**: Loads JSON files, provides `t()` function
- **translation_utils.py**: `get_translated()`, `get_translated_list()` helpers
- **translation_service.py**: MyMemory API integration for auto-translate

### Layer 6: Templates (Jinja2)
- **base.html**: Layout with navbar, footer, language switcher
- **Page templates**: index, about, projects, experience, blog, contact
- **Admin templates**: Forms with English/Spanish fields

## Project Structure
*   `/`
    *   `app.py`: The main Flask application file.
    *   `api.py`: REST API endpoints for React components.
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
    *   `react/`: React frontend (Vite + Zustand)
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
All models with translatable content have a `translations` JSON column for multilingual support.

| Model | Fields | Translatable Fields |
|-------|--------|---------------------|
| `User` | id, username, password_hash, created_at | None (auth only) |
| `Project` | id, title, description, technologies, link, demo, git_url, featured, translations | title, description |
| `Experience` | id, title, company, period, location, responsibilities, technologies, translations | title, responsibilities |
| `Education` | id, degree, school, year, translations | degree, school |
| `BlogPost` | id, title, excerpt, content, image, author, category, date, translations | title, excerpt, content |
| `Skill` | id, name, icon, category, translations | name |
| `Interest` | id, name, translations | name |
| `SocialLink` | id, platform, url, icon, translations | platform |
| `ContactMessage` | id, name, email, subject, message, created_at | None (form data) |
| `Settings` | id, key, value, translations, created_at, updated_at | value (via translations) |

**Settings Keys**: Site content stored in Settings includes hero section, about section, features, CTAs, and SMTP configuration. All text content is translatable.

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

### Translation Architecture (3 Layers):

**Layer 1 - Static UI Text (JSON files)**
- Located in `translations/en.json` and `translations/es.json`
- Used in templates via `{{ t('key') }}` function
- Examples: navigation labels, button text, section headers

**Layer 2 - Database Content (translations JSON column)**
- Each model with translatable content has a `translations` JSON column
- Format: `{"es": {"field_name": "translated value"}}`
- Used via `get_translated(model_instance, "field_name", lang)` function
- Examples: project titles, blog post content, skill names

**Layer 3 - Site Configuration (Settings model)**
- Uses `Settings.get_translated(key, lang, default)` static method
- Stores English as default value, Spanish in `translations` JSON column
- Available globally via `site_config` context processor

### Translation Flow:
```
Request → routes.py → views.py → get_translated() → Template
                    ↓
              translation_utils.py → Database (translations JSON)
                    ↓
              translations.py → JSON files (UI strings)
```

### Key Functions (translation_utils.py):
- `get_translated(obj, field, lang)` - Get translated value from model
- `get_translated_list(items, fields, lang)` - Translate multiple items
- `get_education_list(educations, lang)` - Translate education entries
- `get_interests_list(interests, lang)` - Translate interests
- `get_social_links_list(links, lang)` - Translate social links

### Adding Translations:
1. **Static UI text**: Edit `translations/en.json` or `translations/es.json`
2. **Database content**: Via admin panel forms (Spanish fields have `_es` suffix)
3. **Site config**: Via `/admin/site-config` with separate English/Spanish fields

### Language Detection & Switching:
- Session-based: `session["lang"]`
- Browser preference: `request.accept_languages.best_match()`
- Routes: `/set-lang/en` and `/set-lang/es`

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
*   When models change, update BOTH local (`instance/portfolio.db`) AND production (`~/.local/share/amv_aipf/instance/portfolio.db`) databases:
  ```bash
  # For local development
  python3 -c "import sqlite3; conn = sqlite3.connect('instance/portfolio.db'); cursor.execute('ALTER TABLE table_name ADD COLUMN ...'); conn.commit()"
  
  # For production (if migration not possible)
  python3 -c "import sqlite3; conn = sqlite3.connect('/home/user/.local/share/amv_aipf/instance/portfolio.db'); ..."
  ```

## Migration Workflow
When modifying database models:

1. **Development**: Update `models.py` with new columns/tables
2. **Local DB**: Add columns directly to `instance/portfolio.db` (SQLite limitations)
3. **Rebuild & Restart Container**:
   ```bash
   podman build -t amv_aipf:latest -f deploy/Containerfile .
   podman stop amv_aipf && podman rm amv_aipf
   podman run -d --name amv_aipf -p 5000:5000 \
     -v ~/.local/share/amv_aipf/instance:/app/instance \
     -e FLASK_APP=app.py -e FLASK_ENV=production \
     --env-file ~/.local/share/amv_aipf/amv_aipf.env \
     localhost/amv_aipf:latest
   ```
4. **Production DB**: Add columns to `~/.local/share/amv_aipf/instance/portfolio.db`

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

## OpenCode Skills

This project uses OpenCode's multi-skill system. Skills are in `.opencode/skills/`:

| Skill | Purpose |
|-------|---------|
| `ui-ux-pro-max` | UI/UX design intelligence |
| `flask-backend-expert` | Flask web development |
| `backend-expert` | General backend/API architecture |
| `python-developer` | Python scripting and automation |
| `react-integration` | React + Flask hybrid patterns |
| `react-native-expert` | React Native mobile development |

See `.opencode/skills/README.md` for full details.
