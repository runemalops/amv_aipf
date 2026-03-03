# amv_aipf

Personal portfolio web application built with Flask, SQLAlchemy, and Bootstrap CSS.

## Features

- **Public Pages**: Home, About, Projects, Experience, Blog, Contact
- **Admin Panel**: Full CRUD management for all content
- **Authentication**: Secure admin login with password hashing
- **Database**: SQLite with Flask-Migrate for version control

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
podman build -f deploy/Containerfile -t localhost/amv_aipf:latest .
```

### Deploy with Quadlet

```bash
# Copy quadlet to systemd directory
mkdir -p ~/.config/containers/systemd/
cp deploy/amv_aipf.container ~/.config/containers/systemd/

# Reload systemd
systemctl --user daemon-reload

# Set secret key
export SECRET_KEY=your-secure-random-key

# Start the container
systemctl --user start amv_aipf

# Enable auto-start on boot
systemctl --user enable amv_aipf
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
├── auth.py             # Authentication
├── admin.py            # Admin panel
├── seed.py             # Data seeding
├── requirements.txt    # Dependencies
├── instance/           # SQLite database
├── migrations/         # Database migrations
├── templates/          # HTML templates
│   └── admin/          # Admin templates
└── deploy/             # Deployment files
    ├── Containerfile
    └── amv_aipf.container
```
