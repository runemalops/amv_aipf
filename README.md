# amv_aipf

Personal portfolio web application built with Flask and React, featuring a hybrid architecture with Flask/Jinja templates and React islands for interactive components.

## Features

- **Public Pages**: Home, About, Projects, Experience, Blog
- **Admin Panel**: Full CRUD for all content with auto-translate
- **Authentication**: Secure admin login with password hashing
- **Multilingual**: English and Spanish with auto-translate
- **React Islands**: Interactive project filtering and contact form
- **Database**: SQLite with Flask-Migrate
- **Deployment**: Podman with Quadlet systemd integration

---

## Quick Start

```bash
# Create virtual environment
python3 -m venv venv && source venv/bin/activate

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

---

## Project Structure

```
amv_aipf/
├── app.py                    # Main Flask application, CLI commands
├── api.py                    # REST API endpoints for React
├── models.py                 # SQLAlchemy database models
├── routes.py                 # Public URL routes
├── views.py                  # View functions, business logic
├── auth.py                   # Authentication routes
├── admin.py                  # Admin panel CRUD operations
├── seed.py                   # Database seeding script
├── translation_service.py     # MyMemory API translation
├── translation_utils.py       # Translation helpers, icon maps
├── translations.py            # JSON file loader, t() function
├── requirements.txt          # Python dependencies
├── agent.md                 # AI agent instructions
│
├── templates/                # Jinja2 HTML templates
│   ├── base.html            # Base template with navbar, footer
│   ├── index.html           # Home page
│   ├── about.html           # About page (skills, interests, education)
│   ├── projects.html        # Projects page (React island)
│   ├── experience.html      # Work experience timeline
│   ├── blog.html            # Blog listing
│   ├── blog_post.html       # Single blog post
│   └── admin/               # Admin templates
│
├── react/                   # React frontend
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── features/    # Feature components (ProjectsGrid, ContactForm)
│   │   │   └── ui/         # UI components (Button, Card, Input)
│   │   ├── api/            # API client, types
│   │   ├── hooks/          # Custom hooks
│   │   ├── stores/         # Zustand state stores
│   │   └── entries/        # Entry points
│   ├── vite.config.ts      # Vite build configuration
│   └── styles.css          # React component styles
│
├── instance/                # SQLite database (gitignored)
├── migrations/              # Flask-Migrate migrations
├── translations/            # Language JSON files (en.json, es.json)
└── deploy/                  # Deployment files
    ├── Containerfile        # Multi-stage Docker build
    └── amv_aipf.container   # Quadlet systemd unit
```

---

## Backend Layer

### Flask Application (`app.py`)

Main application factory with:
- Blueprint registration
- Database initialization
- Custom CLI commands (`create-admin`, `set-skill-icons`, `set-interest-icons`)
- Session configuration

### Models (`models.py`)

SQLAlchemy models with translation support:

| Model | Fields | Translatable |
|-------|--------|--------------|
| `Project` | title, description, technologies, link, demo, featured | title, description |
| `Experience` | title, company, period, location, responsibilities, technologies | title, responsibilities |
| `Education` | degree, school, year | degree, school |
| `BlogPost` | title, excerpt, content, image, author, category, date | title, excerpt, content |
| `Skill` | name, icon, category | name |
| `Interest` | name, icon | name |
| `SocialLink` | platform, url, icon | platform |
| `ContactMessage` | name, email, subject, message |
| `Settings` | key, value, translations | value |

### REST API (`api.py`)

Endpoints for React components:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/projects` | GET | List all projects |
| `/api/projects?featured=true` | GET | Featured projects only |
| `/api/blog` | GET | Blog posts (optional `?limit=N`) |
| `/api/experience` | GET | Work experience |
| `/api/education` | GET | Education entries |
| `/api/skills` | GET | Skills with auto-icons |
| `/api/contact` | POST | Submit contact form |
| `/api/csrf-token` | GET | CSRF token for forms |

### Admin Panel (`admin.py`)

CRUD operations at `/admin/`:
- Projects, Experience, Education, Blog Posts
- Skills, Interests, Social Links
- Contact Messages viewing
- Settings and Site Configuration
- Change password

---

## Frontend Layer

### Templates (`templates/`)

Flask/Jinja templates using Bootstrap 5 and Bootstrap Icons.

**Page Sections:**
- `index.html` - Hero, Features, Featured Projects, Latest Posts, CTA
- `about.html` - Introduction, Skills (auto-icons), Interests (auto-icons), Education
- `projects.html` - React ProjectsGrid island
- `experience.html` - Timeline of work experience
- `blog.html` - Blog post listings
- `blog_post.html` - Single blog post with translations

### Flask-React Hybrid Architecture

| Section | Approach | Reason |
|---------|----------|--------|
| Header/Footer | Flask/Jinja | Static, SEO-critical |
| Project Grid | **React** | Technology filtering, animations |
| Contact Form | **React** | Client-side validation, slide-in panel |
| Blog Posts | Flask | SEO-friendly content |
| About/Education | Flask | Simple display |

### React Components (`react/`)

**Entry Points:**
- `projects.tsx` - ProjectsGrid with filters
- `contact.tsx` - Full page contact form
- `panel.tsx` - Slide-in contact panel (floating button)

**Features:**
- `ProjectsGrid.tsx` - Filter buttons, project cards, modals
- `ContactForm.tsx` - Form validation, async submission

**UI Components:**
- Button, Card, Input, TextArea, Badge, Modal, Loading

---

## Data Layer

### Database (`instance/`)

SQLite database with Flask-Migrate for version control.

### Migrations

```bash
# Create migration
flask db migrate -m "Description"

# Apply migrations
flask db upgrade

# Rollback
flask db downgrade
```

### Seeding (`seed.py`)

Initial data for development:
- Admin user
- Sample projects
- Work experience
- Education
- Skills with auto-icons
- Interests with auto-icons

---

## Features

### Internationalization

Three-layer translation system:

| Layer | Source | Usage |
|-------|--------|-------|
| UI Strings | `translations/*.json` | `{{ t('key') }}` |
| Database Content | Model `translations` column | `get_translated()` |
| Site Config | `Settings` model | `{{ site_config.field }}` |

**Admin auto-translate** buttons available for:
- Projects, Experience, Education, Blog Posts
- Skills, Interests, Social Links

### Auto-Icons

#### Skills Icon Map

| Technology | Icon | Technology | Icon |
|-----------|------|-----------|------|
| Python | bi-filetype-py | Docker | bi-box-seam-fill |
| JavaScript/TypeScript | bi-braces | Git | bi-git |
| React | bi-lightning-charge | Linux/Bash | bi-terminal |
| Flask/Django | bi-file-code-fill | AWS/Azure/GCP | bi-cloud-fill |
| HTML | bi-filetype-html | Database | bi-database-fill |
| CSS | bi-filetype-css | Node.js | bi-node-plus |
| ML/AI | bi-brain | Security | bi-shield-check |
| Terraform | bi-stack | FastAPI | bi-lightning-charge |

#### Interests Icon Map

| Interest | Icon | Interest | Icon |
|----------|------|----------|------|
| Coding | bi-code-square | Music | bi-music-note |
| Open Source | bi-github | Motorcycles | bi-bicycle |
| Cloud | bi-cloud | Cars | bi-car-front |
| ML/AI | bi-brain | Video Games | bi-controller |
| Cybersecurity | bi-shield-lock | Photography | bi-camera |
| Web Dev | bi-globe | Hiking | bi-compass |
| Mobile | bi-phone | Learning | bi-book |

**CLI commands:**
```bash
flask set-skill-icons      # Update skill icons
flask set-interest-icons   # Update interest icons
```

---

## Development

### React Development

```bash
cd react

# Install dependencies
npm install

# Development server (proxies to Flask)
npm run dev

# Production build
npm run build
```

### Flask Development

```bash
# Set environment
export FLASK_ENV=development
export FLASK_DEBUG=1

# Run server
python app.py
```

---

## Deployment

### Build Container

```bash
podman build -f deploy/Containerfile -t amv_aipf:latest .
```

### Quadlet Deployment

```bash
# Prepare directories
mkdir -p ~/.local/share/amv_aipf/instance
mkdir -p ~/.local/share/amv_aipf

# Copy database
cp instance/portfolio.db ~/.local/share/amv_aipf/instance/

# Create secret key
echo "SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')" \
  > ~/.local/share/amv_aipf/amv_aipf.env

# Copy quadlet
mkdir -p ~/.config/containers/systemd/
cp deploy/amv_aipf.container ~/.config/containers/systemd/

# Start service
systemctl --user daemon-reload
systemctl --user start amv_aipf

# Check status
systemctl --user status amv_aipf

# View logs
journalctl --user -u amv_aipf -f
```

### Cloudflare Tunnel

```bash
cloudflared tunnel --url http://localhost:5000
```

Or configure a persistent tunnel in `~/.cloudflared/config.yml`.

---

## OpenCode Skills (Optional)

Enable AI assistant skills for [OpenCode](https://opencode.ai).

### Setup

```bash
mkdir -p .opencode/skills
```

### Create a Skill

`.opencode/skills/<name>/SKILL.md`:
```markdown
---
name: Skill Display Name
description: What this skill covers
---

# Skill Content

Detailed instructions...
```

### Available Skills

| Skill | Purpose |
|-------|---------|
| `ui-ux-pro-max` | UI/UX design |
| `flask-backend-expert` | Flask development |
| `backend-expert` | General backend/API |
| `python-developer` | Python scripts |
| `react-integration` | React + Flask hybrid |
| `react-native-expert` | React Native mobile |

### Key Files Reference

| File | Purpose |
|------|---------|
| `app.py` | Main app, CLI commands |
| `api.py` | REST API |
| `models.py` | Database models |
| `views.py` | View functions |
| `admin.py` | Admin CRUD |
| `templates/` | Jinja2 templates |
| `react/` | React frontend |
