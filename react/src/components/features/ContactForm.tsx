import { useState } from 'react';
import { Input } from '@/components/ui';
import { TextArea } from '@/components/ui';
import { Button } from '@/components/ui';
import { useForm } from '@/hooks';
import { getCsrfToken } from '@/api/client';
import type { ContactFormData } from '@/api/types';

interface ContactFormProps {
  onSuccess?: () => void;
  showLabels?: boolean;
}

export function ContactForm({ onSuccess, showLabels = true }: ContactFormProps) {
  const [serverError, setServerError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const { values, errors, touched, loading, handleChange, handleBlur, handleSubmit, reset } = useForm<ContactFormData>({
    initialValues: {
      name: '',
      email: '',
      subject: '',
      message: '',
    },
    validate: (values) => {
      const errors: Partial<Record<keyof ContactFormData, string>> = {};
      
      if (!values.name.trim()) {
        errors.name = 'Name is required';
      } else if (values.name.length < 2) {
        errors.name = 'Name must be at least 2 characters';
      }

      if (!values.email.trim()) {
        errors.email = 'Email is required';
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(values.email)) {
        errors.email = 'Please enter a valid email address';
      }

      if (!values.subject.trim()) {
        errors.subject = 'Subject is required';
      }

      if (!values.message.trim()) {
        errors.message = 'Message is required';
      } else if (values.message.length < 10) {
        errors.message = 'Message must be at least 10 characters';
      }

      return errors;
    },
    onSubmit: async (values) => {
      setServerError(null);
      
      try {
        const response = await fetch('/api/contact', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRF-Token': getCsrfToken(),
          },
          credentials: 'include',
          body: JSON.stringify(values),
        });

        if (!response.ok) {
          const data = await response.json();
          throw new Error(data.error || 'Failed to send message');
        }

        setSuccess(true);
        reset();
        onSuccess?.();
        
        setTimeout(() => setSuccess(false), 5000);
      } catch (err) {
        setServerError(err instanceof Error ? err.message : 'Failed to send message');
      }
    },
  });

  return (
    <form onSubmit={handleSubmit} className="contact-form" noValidate>
      {serverError && (
        <div className="alert alert-danger" role="alert">
          {serverError}
        </div>
      )}
      
      {success && (
        <div className="alert alert-success" role="alert">
          Message sent successfully! I'll get back to you soon.
        </div>
      )}

      <Input
        type="text"
        name="name"
        label={showLabels ? 'Name' : undefined}
        placeholder={showLabels ? undefined : 'Your name'}
        value={values.name}
        onChange={handleChange}
        onBlur={handleBlur}
        error={touched.name ? errors.name : undefined}
        required
        autoComplete="name"
      />

      <Input
        type="email"
        name="email"
        label={showLabels ? 'Email' : undefined}
        placeholder={showLabels ? undefined : 'your.email@example.com'}
        value={values.email}
        onChange={handleChange}
        onBlur={handleBlur}
        error={touched.email ? errors.email : undefined}
        required
        autoComplete="email"
      />

      <Input
        type="text"
        name="subject"
        label={showLabels ? 'Subject' : undefined}
        placeholder={showLabels ? undefined : 'What is this about?'}
        value={values.subject}
        onChange={handleChange}
        onBlur={handleBlur}
        error={touched.subject ? errors.subject : undefined}
        required
      />

      <TextArea
        name="message"
        label={showLabels ? 'Message' : undefined}
        placeholder={showLabels ? undefined : 'Tell me about your project...'}
        value={values.message}
        onChange={handleChange}
        onBlur={handleBlur}
        error={touched.message ? errors.message : undefined}
        required
        rows={5}
      />

      <Button
        type="submit"
        variant="primary"
        size="lg"
        loading={loading}
        className="w-100"
      >
        Send Message
      </Button>
    </form>
  );
}
