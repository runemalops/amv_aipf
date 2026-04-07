# OpenCode Skills

This project uses OpenCode's multi-skill system for AI-assisted development. Skills are defined in `.opencode/skills/` with each skill in its own directory.

## Available Skills

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| `ui-ux-pro-max` | UI/UX design intelligence | Designing pages, components, color schemes |
| `flask-backend-expert` | Flask web development | Routes, models, authentication, API |
| `backend-expert` | General backend development | APIs, databases, architecture |
| `python-developer` | Python development | Scripts, automation, data processing |
| `react-integration` | React + Flask hybrid | React components, Vite, Zustand |
| `react-native-expert` | React Native development | Mobile apps, iOS/Android |

## Adding New Skills

1. Create a directory: `.opencode/skills/<skill-name>/`
2. Add a `SKILL.md` file with YAML frontmatter:

```markdown
---
name: my-new-skill
description: "A brief description of when to use this skill (1-1024 chars)"
---

# My New Skill

Instructions for the AI agent...
```

### Skill Naming Rules
- 1-64 characters
- Lowercase alphanumeric with single hyphens
- No leading/trailing hyphens
- No consecutive hyphens
- Must match directory name

## Skill Discovery Locations

OpenCode searches these paths (highest priority last):
1. `.opencode/skills/<name>/SKILL.md` (project-local)
2. `~/.config/opencode/skills/<name>/SKILL.md` (global)
3. `.claude/skills/<name>/SKILL.md` (Claude-compatible)
4. `.agents/skills/<name>/SKILL.md` (Agent-compatible)

## Using Skills

When working with OpenCode:
1. The `skill` tool lists available skills
2. Use `skill({ name: "skill-name" })` to load a skill
3. The AI will automatically consider relevant skills based on context

## Skill Descriptions

### ui-ux-pro-max
Comprehensive UI/UX design guide with 50+ styles, color palettes, font pairings, and best practices for web and mobile applications.

### flask-backend-expert
Flask web development expertise including SQLAlchemy ORM, Flask-Migrate, Jinja2 templates, Flask-Login authentication, REST APIs, and deployment.

### python-developer
Python development for scripting, automation, data processing, and utility development with best practices.

### react-integration
React integration patterns for Flask applications covering component architecture, Zustand state management, Flask-React API communication, and modern UI patterns.

### backend-expert
General backend development expertise covering API design, database architecture, authentication patterns, microservices, and server-side best practices.

### react-native-expert
React Native development for cross-platform mobile applications covering component design, navigation, native modules, performance optimization, and iOS/Android deployment.
