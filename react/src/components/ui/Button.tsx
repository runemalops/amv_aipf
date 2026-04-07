import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  icon?: React.ReactNode;
  iconPosition?: 'left' | 'right';
}

export function Button({
  children,
  variant = 'primary',
  size = 'md',
  loading = false,
  disabled,
  icon,
  iconPosition = 'left',
  className = '',
  ...props
}: ButtonProps) {
  const baseClasses = 'btn';
  const variantClasses = `btn-${variant}`;
  const sizeClasses = `btn-${size}`;
  const loadingClass = loading ? 'btn-loading' : '';

  return (
    <button
      className={`${baseClasses} ${variantClasses} ${sizeClasses} ${loadingClass} ${className}`.trim()}
      disabled={disabled || loading}
      {...props}
    >
      {loading && <span className="btn-spinner" aria-hidden="true" />}
      {icon && iconPosition === 'left' && <span className="btn-icon-left">{icon}</span>}
      {children && <span className="btn-text">{children}</span>}
      {icon && iconPosition === 'right' && <span className="btn-icon-right">{icon}</span>}
    </button>
  );
}
