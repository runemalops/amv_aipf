import React from 'react';
import { createRoot } from 'react-dom/client';
import { ContactPanel } from '@/components/features/ContactPanel';
import '@/styles.css';

const panelRoot = document.getElementById('contact-panel-root');
if (panelRoot) {
  createRoot(panelRoot).render(
    <React.StrictMode>
      <ContactPanel />
    </React.StrictMode>
  );
}
