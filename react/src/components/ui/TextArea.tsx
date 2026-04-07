import React from 'react';

interface TextAreaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
  hint?: string;
}

export const TextArea = React.forwardRef<HTMLTextAreaElement, TextAreaProps>(
  ({ label, error, hint, id, className = '', rows = 4, ...props }, ref) => {
    const inputId = id || `textarea-${Math.random().toString(36).substr(2, 9)}`;

    return (
      <div className={`form-group ${error ? 'has-error' : ''}`}>
        {label && (
          <label htmlFor={inputId} className="form-label">
            {label}
            {props.required && <span className="text-danger">*</span>}
          </label>
        )}
        <textarea
          ref={ref}
          id={inputId}
          rows={rows}
          className={`form-control ${error ? 'is-invalid' : ''} ${className}`}
          aria-invalid={!!error}
          aria-describedby={error ? `${inputId}-error` : hint ? `${inputId}-hint` : undefined}
          {...props}
        />
        {hint && !error && (
          <small id={`${inputId}-hint`} className="form-text">
            {hint}
          </small>
        )}
        {error && (
          <div id={`${inputId}-error`} className="invalid-feedback" role="alert">
            {error}
          </div>
        )}
      </div>
    );
  }
);

TextArea.displayName = 'TextArea';
