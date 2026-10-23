import React, { useEffect } from 'react'

/**
 * Modal Component - Reusable modal dialog
 */
export default function Modal({ 
  isOpen, 
  onClose, 
  title, 
  children, 
  size = 'md',
  showCloseButton = true,
  className = '',
  ...props
}) {
  const [isVisible, setIsVisible] = React.useState(isOpen)

  useEffect(() => {
    if (isOpen) {
      setIsVisible(true)
      document.body.style.overflow = 'hidden'
    } else {
      setTimeout(() => {
        setIsVisible(false)
        document.body.style.overflow = ''
      }, 300)
    }

    return () => {
      document.body.style.overflow = ''
    }
  }, [isOpen])

  const handleBackdropClick = (e) => {
    if (e.target === e.currentTarget) {
      onClose()
    }
  }

  if (!isVisible && !isOpen) return null

  const sizes = {
    sm: 'max-w-md',
    md: 'max-w-2xl',
    lg: 'max-w-4xl',
    xl: 'max-w-6xl'
  }

  return (
    <div 
      className={`fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-50 backdrop-blur-sm ${className}`}
      onClick={handleBackdropClick}
      {...props}
    >
      <div 
        role="dialog"
        aria-modal="true"
        className={`bg-white rounded-xl shadow-2xl w-full max-h-[90vh] overflow-y-auto transform transition-all duration-300 ${sizes[size]} ${isOpen ? 'opacity-100 scale-100' : 'opacity-0 scale-95'}`}
      >
        <div className="flex flex-col">
          {/* Modal Header */}
          {(title || showCloseButton) && (
            <div className={`px-6 py-4 border-b border-gray-200 ${!title ? 'bg-primary text-white' : ''}`}>
              {showCloseButton && (
                <button
                  onClick={onClose}
                  className="absolute top-4 right-4 p-1 rounded-full hover:bg-opacity-20 bg-inherit transition-colors"
                  aria-label="Закрыть модальное окно"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              )}
              
              {title && (
                <h3 className="text-xl font-bold">{title}</h3>
              )}
            </div>
          )}

          {/* Modal Body */}
          <div className="p-6">
            {children}
          </div>
        </div>
      </div>
    </div>
  )
}

/**
 * ConfirmModal - Pre-styled confirmation modal
 */
export function ConfirmModal({ 
  isOpen, 
  onClose, 
  onConfirm, 
  title = 'Подтверждение',
  message,
  confirmText = 'Да',
  cancelText = 'Нет'
}) {
  return (
    <Modal 
      isOpen={isOpen} 
      onClose={onClose} 
      size="sm"
      title={title}
    >
      <div className="space-y-4">
        <p>{message}</p>
        
        <div className="flex gap-3 pt-4">
          <button
            onClick={() => {
              onConfirm()
              onClose()
            }}
            className="btn btn-primary flex-1"
          >
            {confirmText}
          </button>
          
          <button
            onClick={onClose}
            className="btn outline-btn w-24"
          >
            {cancelText}
          </button>
        </div>
      </div>
    </Modal>
  )
}

/**
 * ModalForm - Modal with built-in form handling
 */
export function ModalForm({ 
  isOpen, 
  onClose, 
  title,
  children,
  submitButtonText = 'Отправить'
}) {
  const handleSubmit = (e) => {
    e.preventDefault()
    // Handle form submission here
  }

  return (
    <Modal isOpen={isOpen} onClose={onClose} size="md" showCloseButton={false}>
      <form onSubmit={handleSubmit} className="space-y-4">
        {children}
        
        <div className="flex gap-3 pt-4">
          <button type="submit" className="btn btn-primary flex-1">{submitButtonText}</button>
          <button 
            type="button" 
            onClick={onClose}
            className="btn outline-btn w-24"
          >
            Отмена
          </button>
        </div>
      </form>
    </Modal>
  )
}