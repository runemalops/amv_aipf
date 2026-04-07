import React from 'react';
import { createRoot } from 'react-dom/client';
import { ProjectsGrid } from '@/components/features/ProjectsGrid';
import { ContactForm } from '@/components/features/ContactForm';
import '@/styles.css';

const projectsRoot = document.getElementById('projects-grid-root');
if (projectsRoot) {
  createRoot(projectsRoot).render(
    <React.StrictMode>
      <ProjectsGrid />
    </React.StrictMode>
  );
}

const contactRoot = document.getElementById('contact-form-root');
if (contactRoot) {
  createRoot(contactRoot).render(
    <React.StrictMode>
      <ContactForm />
    </React.StrictMode>
  );
}
