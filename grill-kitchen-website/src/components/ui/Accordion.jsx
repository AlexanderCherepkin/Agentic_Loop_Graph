import React, { useState } from 'react'

/**
 * Accordion Component - Reusable collapsible content
 */
export default function Accordion({ 
  items = [], 
  className = '',
  ...props
}) {
  return (
    <div className={`space-y-4 ${className}`} {...props}>
      {items.map((item, index) => (
        <AccordionItem key={index} item={item} />
      ))}
    </div>
  )
}

/**
 * Accordion Item - Single collapsible item
 */
export function AccordionItem({ 
  title, 
  content, 
  icon = null,
  className = '',
  ...props
}) {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <div className={`border border-gray-200 rounded-lg overflow-hidden ${className}`} {...props}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full px-6 py-4 flex items-center justify-between bg-white hover:bg-gray-50 transition-colors"
        aria-expanded={isOpen}
      >
        <span className="text-left font-semibold text-secondary">{title}</span>
        
        {icon ? (
          icon 
        ) : (
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            className={`h-5 w-5 transition-transform duration-300 ${isOpen ? 'rotate-180' : ''}`} 
            fill="none" 
            viewBox="0 0 24 24" 
            stroke="currentColor"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        )}
      </button>
      
      {isOpen && (
        <div className="px-6 py-4 bg-gray-50 border-t border-gray-200 animate-fade-in">
          <p className="text-gray-700">{content}</p>
        </div>
      )}
    </div>
  )
}

/**
 * Accordion with predefined FAQ items
 */
export function FaqAccordion({ questions = [] }) {
  return (
    <Accordion 
      items={questions.map((question, index) => ({
        title: question.question,
        content: question.answer,
        icon: null
      }))}
    />
  )
}

/**
 * Accordion with custom icons
 */
export function FeatureAccordion({ features = [] }) {
  return (
    <Accordion 
      items={features.map((feature, index) => ({
        title: feature.title,
        content: feature.description,
        icon: feature.icon || null
      }))}
    />
  )
}

/**
 * Accordion with image content
 */
export function ImageAccordion({ items = [] }) {
  return (
    <div className="space-y-4">
      {items.map((item, index) => (
        <div 
          key={index} 
          className={`border border-gray-200 rounded-lg overflow-hidden bg-white ${item.className || ''}`}
        >
          <button
            onClick={() => item.setOpen?.(idx => !idx)}
            disabled={!item.setOpen}
            className="w-full px-6 py-4 flex items-center justify-between hover:bg-gray-50 transition-colors"
            aria-expanded={item.isOpen || false}
          >
            <span className="text-left font-semibold text-secondary">{item.title}</span>
            
            {item.setOpen && (
              <svg 
                xmlns="http://www.w3.org/2000/svg" 
                className={`h-5 w-5 transition-transform duration-300 ${item.isOpen ? 'rotate-180' : ''}`} 
                fill="none" 
                viewBox="0 0 24 24" 
                stroke="currentColor"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            )}
          </button>
          
          {item.isOpen && (
            <>
              {item.image && (
                <div className="h-48 w-full overflow-hidden">
                  <img 
                    src={item.image} 
                    alt={item.title} 
                    className="w-full h-full object-cover"
                  />
                </div>
              )}
              
              {item.content && (
                <div className="px-6 py-4 bg-gray-50 border-t border-gray-200">
                  <p className="text-gray-700">{item.content}</p>
                </div>
              )}
            </>
          )}
        </div>
      ))}
    </div>
  )
}

export function useAccordion() {
  const [openItems, setOpenItems] = useState({})

  const toggleItem = (index) => {
    setOpenItems(prev => ({
      ...prev,
      [index]: !prev[index]
    }))
  }

  return { openItems, toggleItem }
}