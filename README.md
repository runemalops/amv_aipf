# amv_aipf

Personal portfolio web application built with Flask, SQLAlchemy, and Bootstrap CSS.

## Features

- **Public Pages**: Home, About, Projects, Experience, Blog, Contact
- **Admin Panel**: Full CRUD management for all content (Projects, Experience, Education, Blog, Skills, Interests, Social Links)
- **Authentication**: Secure admin login with password hashing
- **Database**: SQLite with Flask-Migrate for version control
- **Internationalization**: English and Spanish language support with auto-translate
- **Multilingual Content**: All user content (projects, blog posts, skills, etc.) supports English and Spanish

## Tech Stack

- **Backend**: Flask 3.x, SQLAlchemy
- **Auth**: Flask-Login with password hashing
- **Database**: SQLite with Flask-Migrate
- **Frontend**: Bootstrap 5, Bootstrap Icons
- **Email**: Flask-Mail (SMTP)
- **Production**: Gunicorn, Podman

## Quick Start (Development)

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
flask db migrate -m "Initial migration"
flask db upgrade

# Seed initial data (optional)
python seed.py

# Create admin user
flask create-admin <username> <password>

# Run development server
python app.py
```

Access at http://localhost:5000

## Deployment with Podman

### Build the Container Image

```bash
# Run from project root directory
podman build -f deploy/Containerfile -t amv_aipf:latest .
```

### Deploy with Quadlet

```bash
# Prepare instance directory for persistent database
mkdir -p ~/.local/share/amv_aipf/instance
cp instance/portfolio.db ~/.local/share/amv_aipf/instance/

# Create environment file with secret key
mkdir -p ~/.local/share/amv_aipf
echo "SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')" > ~/.local/share/amv_aipf/amv_aipf.env

# Copy quadlet to systemd directory
mkdir -p ~/.config/containers/systemd/
cp deploy/amv_aipf.container ~/.config/containers/systemd/

# Reload systemd and start the container
systemctl --user daemon-reload
systemctl --user start amv_aipf
```

### View Logs

```bash
journalctl --user -u amv_aipf -f
```

## Exposing with Cloudflare Tunnel

Run cloudflared on the host:

```bash
cloudflared tunnel --url http://localhost:5000
```

Or configure a persistent tunnel with your domain in `~/.cloudflared/config.yml`.

## Project Structure

```
amv_aipf/
├── app.py                  # Main Flask application (init, context processors)
├── models.py               # Database models with translations JSON columns
├── routes.py               # Public URL routes
├── views.py                # View functions (business logic)
├── auth.py                 # Authentication routes
├── admin.py                # Admin panel CRUD operations
├── seed.py                 # Data seeding
├── translation_service.py  # MyMemory API integration
├── translation_utils.py    # Translation helpers (get_translated, etc.)
├── translations.py         # JSON file loader, t() function
├── requirements.txt        # Python dependencies
├── agent.md               # Agent instructions for AI assistants
├── instance/               # SQLite database
├── migrations/            # Flask-Migrate migrations
├── templates/             # HTML templates (Jinja2)
│   ├── base.html          # Base layout with navbar/footer
│   ├── index.html         # Homepage
│   ├── about.html         # About page
│   ├── projects.html      # Projects listing
│   ├── experience.html    # Work experience
│   ├── blog.html          # Blog listing
│   ├── blog_post.html     # Single blog post
│   ├── contact.html       # Contact form
│   └── admin/             # Admin panel templates
├── translations/          # Language JSON files
│   ├── en.json           # English UI strings
│   └── es.json           # Spanish UI strings
└── deploy/                # Deployment files
    ├── Containerfile      # Podman container build
    └── amv_aipf.container # Quadlet systemd unit
```

## Internationalization Architecture

The application uses a 3-layer translation system:

| Layer | Source | Usage in Templates |
|-------|--------|-------------------|
| UI Strings | `translations/*.json` | `{{ t('key') }}` |
| Database Content | `translations` JSON column | Via `get_translated()` in views |
| Site Config | `Settings` model | `{{ site_config.field }}` |

### Translation Flow:
1. User selects language → stored in session
2. Route calls view function with `lang` parameter
3. View fetches data using `get_translated()` functions
4. Translated data passed to template
5. Template renders content in selected language
