import React from 'react';
import { createRoot } from 'react-dom/client';
import { ContactForm } from '@/components/features/ContactForm';
import '@/styles.css';

const contactRoot = document.getElementById('contact-form-root');
if (contactRoot) {
  createRoot(contactRoot).render(
    <React.StrictMode>
      <ContactForm showLabels={true} />
    </React.StrictMode>
  );
}
