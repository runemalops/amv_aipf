# React Integration

This directory contains the React frontend for interactive components.

## Structure

```
react/
├── src/
│   ├── api/              # API client and types
│   ├── components/       # Reusable components
│   │   ├── ui/           # Primitive components (Button, Card, etc.)
│   │   ├── forms/       # Form components
│   │   ├── layout/      # Layout components
│   │   └── features/     # Feature components (ProjectsGrid, ContactForm)
│   ├── hooks/            # Custom React hooks
│   ├── stores/           # Zustand state stores
│   ├── utils/            # Utility functions
│   ├── entries/          # Entry points for each page
│   └── styles.css        # Global styles
├── public/               # Static assets
├── package.json
└── vite.config.ts
```

## Development

```bash
cd react

# Install dependencies
npm install

# Start dev server with proxy to Flask
npm run dev

# Build for production
npm run build
```

## Build Output

The production build outputs to `../static/react/`:
- `projects/assets/projects.js` - Projects page
- `contact/assets/contact.js` - Contact page

## Adding New Components

1. Create component in `src/components/`
2. Export from appropriate index.ts
3. Add entry point in `src/entries/` if needed
4. Update `vite.config.ts` inputs
5. Add script tag to Flask template

## API Integration

React components communicate with Flask via REST API:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/projects` | GET | List all projects |
| `/api/projects?featured=true` | GET | List featured projects |
| `/api/blog` | GET | List blog posts |
| `/api/experience` | GET | List experience |
| `/api/education` | GET | List education |
| `/api/skills` | GET | List skills |
| `/api/contact` | POST | Submit contact form |
