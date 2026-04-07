import React from 'react';

interface SpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  variant?: 'primary' | 'secondary' | 'white';
  className?: string;
}

export function Spinner({ size = 'md', variant = 'primary', className = '' }: SpinnerProps) {
  return (
    <div
      className={`spinner spinner-${size} spinner-${variant} ${className}`.trim()}
      role="status"
      aria-label="Loading"
    >
      <span className="visually-hidden">Loading...</span>
    </div>
  );
}

interface SkeletonProps {
  variant?: 'text' | 'circular' | 'rectangular';
  width?: string | number;
  height?: string | number;
  className?: string;
}

export function Skeleton({ variant = 'text', width, height, className = '' }: SkeletonProps) {
  const style: React.CSSProperties = {};
  if (width) style.width = typeof width === 'number' ? `${width}px` : width;
  if (height) style.height = typeof height === 'number' ? `${height}px` : height;

  return (
    <div
      className={`skeleton skeleton-${variant} ${className}`.trim()}
      style={style}
      aria-hidden="true"
    />
  );
}
