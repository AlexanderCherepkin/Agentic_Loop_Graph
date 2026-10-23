import React from 'react'

/**
 * Card Component - Reusable card with hover effects
 */
export default function Card({ 
  children, 
  className = '',
  title,
  subtitle,
  image,
  footer,
  ...props
}) {
  return (
    <div className={`bg-white rounded-xl shadow-md p-6 hover:shadow-xl transition-shadow duration-300 ${className}`} {...props}>
      {image && (
        <div className="mb-4 rounded-lg overflow-hidden">
          <img 
            src={image} 
            alt={title || 'Card image'} 
            className="w-full h-auto object-cover"
            loading="lazy"
          />
        </div>
      )}
      
      {title && (
        <h3 className="text-xl font-bold text-secondary mb-2">{title}</h3>
      )}
      
      {subtitle && (
        <p className="text-gray-600 mb-4">{subtitle}</p>
      )}
      
      <div className="flex flex-col gap-4">
        {children}
      </div>
      
      {footer && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          {footer}
        </div>
      )}
    </div>
  )
}

/**
 * Card Image Component - Reusable image card
 */
export function CardImage({ 
  src, 
  alt, 
  className = '',
  width = '100%',
  height = 'auto',
  ...props
}) {
  return (
    <img 
      src={src} 
      alt={alt} 
      className={`w-full h-auto object-cover rounded-lg ${className}`}
      style={{ width, height }}
      loading="lazy"
      {...props}
    />
  )
}

/**
 * Card Icon Component - Reusable icon card
 */
export function CardIcon({ 
  icon, 
  className = '',
  size = 'md',
  ...props
}) {
  const sizes = {
    sm: 'w-8 h-8 text-lg',
    md: 'w-12 h-12 text-xl',
    lg: 'w-16 h-16 text-2xl'
  }

  return (
    <div className={`${sizes[size]} ${className}`}>
      {icon}
    </div>
  )
}