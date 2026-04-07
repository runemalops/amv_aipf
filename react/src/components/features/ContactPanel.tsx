import { useState, useEffect, useCallback } from 'react';
import { ContactForm } from './ContactForm';

interface ContactPanelProps {
  buttonText?: string;
  buttonIcon?: string;
}

export function ContactPanel({ 
  buttonText = 'Get in Touch',
  buttonIcon = 'bi-chat-dots'
}: ContactPanelProps) {
  const [isOpen, setIsOpen] = useState(false);

  const handleEscape = useCallback((e: KeyboardEvent) => {
    if (e.key === 'Escape') {
      setIsOpen(false);
    }
  }, []);

  useEffect(() => {
    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      document.body.style.overflow = 'hidden';
    }
    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = '';
    };
  }, [isOpen, handleEscape]);

  return (
    <>
      <button 
        className="contact-panel-trigger"
        onClick={() => setIsOpen(true)}
        aria-label="Open contact form"
      >
        <i className={`bi ${buttonIcon}`}></i>
        <span>{buttonText}</span>
      </button>

      <div className={`contact-panel-overlay ${isOpen ? 'active' : ''}`} onClick={() => setIsOpen(false)} />
      
      <div className={`contact-panel ${isOpen ? 'open' : ''}`}>
        <div className="contact-panel-header">
          <div className="contact-panel-header-content">
            <div className="contact-panel-icon">
              <i className="bi bi-envelope-paper-fill"></i>
            </div>
            <div>
              <h2 className="contact-panel-title">Let's Connect</h2>
              <p className="contact-panel-subtitle">Send me a message</p>
            </div>
          </div>
          <button 
            className="contact-panel-close"
            onClick={() => setIsOpen(false)}
            aria-label="Close panel"
          >
            <i className="bi bi-x-lg"></i>
          </button>
        </div>
        
        <div className="contact-panel-body">
          <ContactForm 
            showLabels={false}
            onSuccess={() => setTimeout(() => setIsOpen(false), 2000)}
          />
        </div>
        
        <div className="contact-panel-footer">
          <p className="contact-panel-footer-text">
            <i className="bi bi-clock me-1"></i>
            Usually responds within 24 hours
          </p>
        </div>
      </div>
    </>
  );
}
