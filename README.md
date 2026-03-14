# amv_aipf

Personal portfolio web application built with Flask, SQLAlchemy, and Bootstrap CSS.

## Features

- **Public Pages**: Home, About, Projects, Experience, Blog, Contact
- **Admin Panel**: Full CRUD management for all content
- **Authentication**: Secure admin login with password hashing
- **Database**: SQLite with Flask-Migrate for version control
- **Internationalization**: English and Spanish language support with auto-translate

## Tech Stack

- Flask 3.x
- SQLAlchemy
- Flask-Login
- Flask-Migrate
- Bootstrap 5 + Bootstrap Icons
- Gunicorn (production)

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
├── app.py              # Main Flask application
├── models.py           # Database models
├── routes.py           # Public routes
├── views.py            # View functions
├── auth.py             # Authentication
├── admin.py            # Admin panel
├── seed.py             # Data seeding
├── translation_service.py  # Translation API service
├── translation_utils.py    # Translation helpers with auto-translate
├── translations.py     # Translation helpers
├── requirements.txt    # Dependencies
├── instance/           # SQLite database
├── migrations/         # Database migrations
├── templates/          # HTML templates
│   └── admin/          # Admin templates
├── translations/       # Language files (en.json, es.json)
└── deploy/             # Deployment files
    ├── Containerfile
    └── amv_aipf.container
```
