import React from 'react';
import { createRoot } from 'react-dom/client';
import { ProjectsGrid } from '@/components/features/ProjectsGrid';
import '@/styles.css';

const projectsRoot = document.getElementById('projects-grid-root');
if (projectsRoot) {
  createRoot(projectsRoot).render(
    <React.StrictMode>
      <ProjectsGrid showFilters={true} />
    </React.StrictMode>
  );
}
