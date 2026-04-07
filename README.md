# amv_aipf

Personal portfolio web application built with Flask, SQLAlchemy, and Bootstrap CSS with React islands for interactive components.

## Features

- **Public Pages**: Home, About, Projects, Experience, Blog, Contact
- **Admin Panel**: Full CRUD management for all content (Projects, Experience, Education, Blog, Skills, Interests, Social Links)
- **Authentication**: Secure admin login with password hashing
- **Database**: SQLite with Flask-Migrate for version control
- **Internationalization**: English and Spanish language support with auto-translate
- **Multilingual Content**: All user content (projects, blog posts, skills, etc.) supports English and Spanish
- **React Islands**: Interactive components (ProjectsGrid with filtering, ContactForm with validation)

## Tech Stack

- **Backend**: Flask 3.x, SQLAlchemy
- **Auth**: Flask-Login with password hashing
- **Database**: SQLite with Flask-Migrate
- **Frontend**: Bootstrap 5, Bootstrap Icons, React 18
- **State Management**: Zustand
- **Build Tool**: Vite
- **Email**: Flask-Mail (SMTP)
- **Production**: Gunicorn, Podman

## Quick Start (Development)

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install React dependencies
cd react && npm install && cd ..

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

## React Development

Interactive components use React with Vite:

```bash
cd react

# Install dependencies
npm install

# Development server (proxies to Flask at localhost:5000)
npm run dev

# Production build
npm run build
```

### Flask-React Architecture

The application uses a hybrid approach:

| Section | Approach | Reason |
|---------|----------|--------|
| Header/Footer | Flask/Jinja | Static, SEO-critical |
| Project Grid | **React** | Technology filtering, animations |
| Contact Form | **React** | Client-side validation, async submit |
| Blog Posts | Flask | SEO-friendly content |
| About/Education | Flask | Simple display |

### API Endpoints

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
├── app.py                  # Main Flask application
├── api.py                  # REST API endpoints for React
├── models.py               # Database models with translations
├── routes.py               # Public URL routes
├── views.py                # View functions (business logic)
├── auth.py                 # Authentication routes
├── admin.py                # Admin panel CRUD operations
├── seed.py                 # Data seeding
├── translation_service.py  # MyMemory API integration
├── translation_utils.py    # Translation helpers
├── translations.py         # JSON file loader, t() function
├── requirements.txt        # Python dependencies
├── agent.md               # Agent instructions for AI assistants
├── .opencode/             # OpenCode skills configuration (optional)
│   └── skills/            # Multi-skill directory
│       ├── ui-ux-pro-max/ # UI/UX design skill
│       ├── flask-backend-expert/ # Flask backend skill
│       ├── backend-expert/ # General backend skill
│       ├── python-developer/ # Python development skill
│       ├── react-integration/ # React + Flask hybrid skill
│       └── react-native-expert/ # React Native mobile skill
├── react/                 # React frontend
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── api/          # API client and types
│   │   ├── hooks/        # Custom hooks
│   │   ├── stores/       # Zustand stores
│   │   └── entries/      # Entry points
│   └── vite.config.ts    # Vite configuration
├── instance/              # SQLite database
├── migrations/            # Flask-Migrate migrations
├── templates/             # HTML templates (Jinja2)
├── translations/          # Language JSON files
└── deploy/                # Deployment files
```

## OpenCode Skills (Optional)

This portfolio includes multi-skill support for [OpenCode](https://opencode.ai) AI assistant. Skills provide specialized knowledge about different aspects of the project.

### Enabling OpenCode Skills

1. **Create the skills directory structure:**
   ```bash
   mkdir -p .opencode/skills
   ```

2. **Create a skill file** with the following format:

   `.opencode/skills/<skill-name>/SKILL.md`
   ```
   ---
   name: <Skill Display Name>
   description: Brief description of what this skill covers
   ---
   
   # Skill Content
   
   Detailed instructions, patterns, and best practices...
   ```

3. **Example skill structure:**
   ```
   .opencode/skills/
   ├── README.md                    # Optional: lists all available skills
   ├── flask-backend-expert/
   │   └── SKILL.md
   ├── react-integration/
   │   └── SKILL.md
   └── python-developer/
       └── SKILL.md
   ```

### SKILL.md Format

Each skill file uses YAML frontmatter followed by Markdown content:

```markdown
---
name: Flask Backend Expert
description: Flask web development, routes, models, authentication, API
---

# Flask Backend Expert

## Architecture Patterns

This portfolio uses Flask blueprints for modular organization...

## Database Models

Models are defined in `models.py` using SQLAlchemy...

## API Design

REST endpoints are in `api.py`...
```

### Available Skills in This Project

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| `ui-ux-pro-max` | UI/UX design intelligence | Designing pages, components, color schemes |
| `flask-backend-expert` | Flask web development | Routes, models, authentication, API |
| `backend-expert` | General backend development | APIs, databases, architecture |
| `python-developer` | Python development | Scripts, automation, data processing |
| `react-integration` | React + Flask hybrid | React components, Vite, Zustand |
| `react-native-expert` | React Native development | Mobile apps, iOS/Android |

### Key Files Reference

When creating skills, reference these key files:

| File | Purpose |
|------|---------|
| `app.py` | Main Flask app, CLI commands |
| `api.py` | REST API endpoints |
| `models.py` | SQLAlchemy models |
| `views.py` | View functions |
| `admin.py` | Admin CRUD operations |
| `templates/` | Jinja2 HTML templates |
| `react/` | React frontend |

### Customizing Skills

To customize skills for your portfolio:

1. **Update skill descriptions** to match your stack
2. **Add project-specific patterns** (e.g., your admin structure)
3. **Include your conventions** (naming, organization)
4. **Document custom CLI commands** relevant to your project

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

## Skills with Auto-Icons

Skills automatically receive appropriate Bootstrap Icons based on their name. The icon mapping includes:

| Technology | Icon | Technology | Icon |
|-----------|------|-----------|------|
| Python | bi-filetype-py | Docker | bi-box-seam-fill |
| JavaScript/TypeScript | bi-braces | Git | bi-git |
| React | bi-lightning-charge | Linux/Bash | bi-terminal |
| Flask/Django | bi-file-code-fill | AWS/Azure/GCP | bi-cloud-fill |
| HTML | bi-filetype-html | Database (SQL) | bi-database-fill |
| CSS | bi-filetype-css | Node.js | bi-node-plus |
| Machine Learning/AI | bi-brain | Security | bi-shield-check |
| Terraform | bi-stack | FastAPI | bi-lightning-charge |

To set/update icons for all skills in the database:
```bash
flask set-skill-icons
```

This command updates all skills with icons matching the technology map.

## Interests with Auto-Icons

Interests also automatically receive appropriate Bootstrap Icons based on their name. The icon mapping includes:

| Interest | Icon | Interest | Icon |
|----------|------|----------|------|
| Coding/Programming | bi-code-square | Music | bi-music-note |
| Open Source | bi-github | Motorcycles | bi-bicycle |
| Cloud Computing | bi-cloud | Cars | bi-car-front |
| Machine Learning | bi-brain | Video Games | bi-controller |
| Cybersecurity | bi-shield-lock | Photography | bi-camera |
| Web Development | bi-globe | Hiking | bi-compass |
| Mobile Apps | bi-phone | Learning | bi-book |

To set/update icons for all interests in the database:
```bash
flask set-interest-icons
```
