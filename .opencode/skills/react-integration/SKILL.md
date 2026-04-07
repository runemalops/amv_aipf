---
name: react-integration
description: "React integration patterns for Flask applications. Covers component architecture, state management with Zustand/Context, Flask-React communication via API endpoints, and modern UI patterns for portfolio/business applications."
---

# React Integration for Flask Applications

Expert guidance for integrating React into Flask applications with modern patterns.

## Architecture Overview

```
Flask Backend (Python)
├── REST API Endpoints (/api/*)
├── Authentication (session/JWT)
├── Database (SQLAlchemy)
└── Static Files (compiled React)

React Frontend (JavaScript)
├── Components (functional + hooks)
├── State Management (Zustand/Context)
├── Routing (React Router)
└── API Client (fetch/axios)
```

## When to Apply

- Adding interactive UI elements to Flask templates
- Building single-page sections within Flask pages
- Migrating to a React-based frontend while keeping Flask backend
- Adding dynamic forms, real-time updates, or complex interactions

## Flask-React Integration Patterns

### Pattern 1: Flask as API + React SPA

Best for: Complete frontend rewrite with Flask only for data

```
Flask: API endpoints only (REST/GraphQL)
React: Full SPA with React Router
```

**Pros:** Modern DX, full React ecosystem
**Cons:** More complex setup, SEO considerations

### Pattern 2: React Components in Flask Templates

Best for: Gradual migration, specific interactive sections

```html
<!-- Flask template -->
<div id="contact-form-root" data-csrf="{{ csrf_token() }}"></div>
<script type="module" src="{{ url_for('static', filename='js/contact-form.js') }}"></script>
```

**Pros:** Incremental adoption, simple setup
**Cons:** Multiple React roots, shared state complexity

### Pattern 3: React Islands Architecture

Best for: Mix of static and dynamic content

```html
<!-- Static Flask content -->
<h1>{{ page.title }}</h1>
<p>{{ page.content }}</p>

<!-- React island for interactivity -->
<div id="comments-section" data-page-id="{{ page.id }}"></div>

<!-- Only load React for islands that exist -->
{% if show_comments %}
<script type="module" src="/static/js/comments.js"></script>
{% endif %}
```

## Component Architecture

### Directory Structure

```
react/
├── src/
│   ├── components/           # Reusable UI components
│   │   ├── ui/              # Primitive components (Button, Input, Card)
│   │   ├── forms/           # Form components with validation
│   │   └── layout/          # Layout components (Navbar, Footer)
│   ├── features/            # Feature-specific components
│   │   ├── blog/            # Blog-related components
│   │   ├── projects/        # Project components
│   │   └── contact/         # Contact form
│   ├── hooks/                # Custom React hooks
│   ├── api/                  # API client functions
│   ├── stores/               # Zustand stores / Context providers
│   └── utils/                # Utility functions
├── public/
└── package.json
```

### Component Naming Conventions

```
components/
├── Button.tsx                # Button.tsx (primary)
├── Button.stories.tsx       # Storybook stories
├── Button.test.tsx          # Tests
├── Button.module.css        # Scoped styles
└── index.ts                 # Re-export

// Usage
import { Button } from '@/components/ui'
```

## State Management

### Zustand (Recommended for Most Cases)

```typescript
// stores/usePortfolioStore.ts
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface PortfolioState {
  language: 'en' | 'es'
  theme: 'light' | 'dark'
  setLanguage: (lang: 'en' | 'es') => void
  toggleTheme: () => void
}

export const usePortfolioStore = create<PortfolioState>()(
  persist(
    (set) => ({
      language: 'en',
      theme: 'light',
      setLanguage: (lang) => set({ language: lang }),
      toggleTheme: () => set((state) => ({
        theme: state.theme === 'light' ? 'dark' : 'light'
      })),
    }),
    { name: 'portfolio-storage' }
  )
)
```

### Context for Theme/Settings

```typescript
// context/ThemeContext.tsx
import React, { createContext, useContext, useState } from 'react'

interface ThemeContextType {
  theme: 'light' | 'dark'
  toggleTheme: () => void
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined)

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<'light' | 'dark'>('light')
  
  const toggleTheme = () => setTheme(t => t === 'light' ? 'dark' : 'light')
  
  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      <div data-theme={theme} className="app-root">
        {children}
      </div>
    </ThemeContext.Provider>
  )
}

export const useTheme = () => {
  const context = useContext(ThemeContext)
  if (!context) throw new Error('useTheme must be used within ThemeProvider')
  return context
}
```

## API Integration

### API Client Pattern

```typescript
// api/client.ts
const API_BASE = '/api'

interface FetchOptions extends RequestInit {
  csrf?: string
}

export async function apiFetch<T>(
  endpoint: string,
  options: FetchOptions = {}
): Promise<T> {
  const { csrf, ...fetchOptions } = options
  
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...options.headers,
  }
  
  if (csrf) {
    headers['X-CSRF-Token'] = csrf
  }
  
  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...fetchOptions,
    headers,
    credentials: 'include',
  })
  
  if (!response.ok) {
    throw new Error(`API Error: ${response.status}`)
  }
  
  return response.json()
}
```

### API Hooks

```typescript
// hooks/useProjects.ts
import { useState, useEffect } from 'react'
import { apiFetch } from '@/api/client'

interface Project {
  id: number
  title: string
  description: string
  technologies: string[]
}

export function useProjects() {
  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  
  useEffect(() => {
    apiFetch<Project[]>('/projects')
      .then(setProjects)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [])
  
  return { projects, loading, error }
}
```

## Flask API Endpoints

### RESTful Structure

```
/api
├── /projects                 # Projects CRUD
│   ├── GET    /projects     # List all
│   ├── POST   /projects     # Create (admin)
│   ├── GET    /projects/:id # Get one
│   ├── PUT    /projects/:id # Update (admin)
│   └── DELETE /projects/:id # Delete (admin)
├── /blog                    # Blog CRUD
├── /skills                  # Skills (public)
├── /contact                 # Contact form
└── /auth                   # Authentication
```

### Example Flask API Route

```python
# api/projects.py
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models import db, Project

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/projects', methods=['GET'])
def get_projects():
    lang = request.args.get('lang', 'en')
    projects = Project.query.all()
    return jsonify([
        {
            'id': p.id,
            'title': get_translated(p, 'title', lang),
            'description': get_translated(p, 'description', lang),
            'technologies': p.technologies.split(',') if p.technologies else [],
            'link': p.link,
            'featured': p.featured,
        }
        for p in projects
    ])

@api.route('/projects/<int:id>', methods=['PUT'])
@login_required
def update_project(id):
    project = Project.query.get_or_404(id)
    data = request.get_json()
    # ... update logic
    db.session.commit()
    return jsonify({'success': True})
```

## UI Component Patterns

### Reusable UI Components

```typescript
// components/ui/Button.tsx
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  loading?: boolean
}

export function Button({
  children,
  variant = 'primary',
  size = 'md',
  loading = false,
  disabled,
  className = '',
  ...props
}: ButtonProps) {
  return (
    <button
      className={`btn btn-${variant} btn-${size} ${loading ? 'loading' : ''} ${className}`}
      disabled={disabled || loading}
      {...props}
    >
      {loading && <span className="spinner" />}
      {children}
    </button>
  )
}
```

### Form Components with Validation

```typescript
// components/forms/ContactForm.tsx
import { useState } from 'react'
import { Button } from '@/components/ui'
import { useForm } from '@/hooks/useForm'

export function ContactForm() {
  const { values, errors, handleChange, handleSubmit, loading } = useForm({
    initialValues: { name: '', email: '', message: '' },
    validate: (values) => {
      const errors: Record<string, string> = {}
      if (!values.name) errors.name = 'Name is required'
      if (!values.email.includes('@')) errors.email = 'Valid email required'
      if (values.message.length < 10) errors.message = 'Message too short'
      return errors
    },
    onSubmit: async (values) => {
      await apiFetch('/contact', { method: 'POST', body: JSON.stringify(values) })
      // Handle success
    }
  })
  
  return (
    <form onSubmit={handleSubmit}>
      <input
        name="name"
        value={values.name}
        onChange={handleChange}
        placeholder="Your name"
      />
      {errors.name && <span className="error">{errors.name}</span>}
      {/* ... other fields */}
    </form>
  )
}
```

### Custom Hook for Forms

```typescript
// hooks/useForm.ts
import { useState, useCallback } from 'react'

interface UseFormOptions<T> {
  initialValues: T
  validate?: (values: T) => Partial<Record<keyof T, string>>
  onSubmit: (values: T) => Promise<void>
}

export function useForm<T extends Record<string, any>>({
  initialValues,
  validate,
  onSubmit,
}: UseFormOptions<T>) {
  const [values, setValues] = useState<T>(initialValues)
  const [errors, setErrors] = useState<Partial<Record<keyof T, string>>>({})
  const [loading, setLoading] = useState(false)
  
  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setValues(v => ({ ...v, [name]: value }))
  }, [])
  
  const handleSubmit = useCallback(async (e: React.FormEvent) => {
    e.preventDefault()
    const newErrors = validate?.(values) || {}
    setErrors(newErrors)
    
    if (Object.keys(newErrors).length === 0) {
      setLoading(true)
      try {
        await onSubmit(values)
      } finally {
        setLoading(false)
      }
    }
  }, [values, validate, onSubmit])
  
  return { values, errors, handleChange, handleSubmit, loading }
}
```

## Page Management Architecture

### Component-Based Pages

```
Flask Templates (Static Shell)
└── React Components (Dynamic Content)

index.html (Flask)
├── <Header />          (Flask/Jinja) or React
├── <HeroSection />     (Flask rendered)
├── <ProjectsGrid />    ← React island
├── <ExperienceList />  ← React island  
├── <BlogPreview />     ← React island
└── <Footer />          (Flask/Jinja) or React
```

### Page State Management

```typescript
// stores/usePageStore.ts
import { create } from 'zustand'

interface PageState {
  activeSection: string
  scrollProgress: number
  isMenuOpen: boolean
  setActiveSection: (section: string) => void
  setScrollProgress: (progress: number) => void
  toggleMenu: () => void
}

export const usePageStore = create<PageState>((set) => ({
  activeSection: 'home',
  scrollProgress: 0,
  isMenuOpen: false,
  setActiveSection: (section) => set({ activeSection: section }),
  setScrollProgress: (progress) => set({ scrollProgress: progress }),
  toggleMenu: () => set((state) => ({ isMenuOpen: !state.isMenuOpen })),
}))
```

## Build & Integration

### Vite Configuration for Flask

```javascript
// vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: '/static/',
  build: {
    outDir: 'dist',
    rollupOptions: {
      input: {
        main: './index.html',
        projects: './projects.html',
        blog: './blog.html',
        panel: './panel.html', // Contact slide-in panel
      }
    }
  },
  server: {
    proxy: {
      '/api': 'http://localhost:5000',
    }
  }
})
```

### Flask Static Serving

```python
# app.py - serve React build in production
import os

@app.route('/<path:path>')
def serve_react(path):
    if path.startswith('api/') or path.startswith('admin/'):
        return 404
    
    react_dist = os.path.join(os.path.dirname(__file__), 'react', 'dist')
    file_path = os.path.join(react_dist, path)
    
    if os.path.exists(file_path):
        return send_from_directory(react_dist, path)
    
    # Fallback to index for SPA routing
    return send_from_directory(react_dist, 'index.html')
```

## Performance Best Practices

- **Code Splitting**: Lazy load routes and heavy components
- **Memoization**: Use `React.memo`, `useMemo`, `useCallback` appropriately
- **Virtualization**: For long lists, use `react-window` or `react-virtualized`
- **Image Optimization**: Use `next/image` patterns or lazy loading
- **Bundle Size**: Monitor with `rollup-plugin-visualizer`

## Testing Strategy

```
tests/
├── unit/                    # Individual components
├── integration/             # API + components
└── e2e/                    # Playwright/Cypress
```

- **Unit**: Jest + React Testing Library
- **Integration**: Mock API responses
- **E2E**: Playwright for critical user flows
