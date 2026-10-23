import React, { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import Button from '../ui/Button'

/**
 * Header Component - Main navigation header with mobile menu
 */
export default function Header({ 
  isMobileMenuOpen = false,
  onToggleMobileMenu = () => {}
}) {
  const location = useLocation()
  
  const navItems = [
    { label: 'Главная', href: '/' },
    { label: 'О нас', href: '#about' },
    { label: 'Услуги', href: '#services' },
    { label: 'Портфолио', href: '#portfolio' },
    { label: 'Цены', href: '#pricing' },
    { label: 'Отзывы', href: '#reviews' },
    { label: 'Контакты', href: '#contacts' },
  ]

  return (
    <header className="fixed top-0 left-0 right-0 z-40 bg-white shadow-sm">
      {/* Top Bar */}
      <div className="bg-primary text-white py-2 px-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between text-sm">
          <div className="flex items-center gap-6">
            <span>📞 +7 (903) 851-71-67</span>
            {location.pathname === '/' && (
              <>
                <span>✉️ info@grill-kitchen.ru</span>
                <Button 
                  variant="outline" 
                  size="sm"
                  className="text-white border-white hover:bg-white hover:text-primary"
                  onClick={onToggleMobileMenu}
                >
                  📋 Меню
                </Button>
              </>
            )}
          </div>
          
          <div className="hidden md:flex items-center gap-4">
            <span>🚚 Бесплатная доставка при заказе от 100 000 ₽</span>
          </div>
        </div>
      </div>

      {/* Main Navigation */}
      <nav className="py-3 px-4 md:px-6">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2 group">
            <div className="w-10 h-10 bg-primary rounded-lg flex items-center justify-center text-white font-bold text-xl group-hover:bg-opacity-85 transition-all">
              Г
            </div>
            <span className="text-xl font-bold text-secondary hidden sm:block">
              Grill Kitchen
            </span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden lg:flex items-center gap-1">
            {navItems.map((item, index) => (
              <Link
                key={index}
                to={item.href}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  location.pathname === item.href || location.pathname.includes(item.href)
                    ? 'text-primary bg-gray-100'
                    : 'text-secondary hover:bg-gray-100'
                }`}
              >
                {item.label}
              </Link>
            ))}
          </div>

          {/* CTA Buttons */}
          <div className="hidden md:flex items-center gap-3">
            <Button variant="outline" size="sm">
              📞 +7 (903) 851-71-67
            </Button>
            <Button variant="primary" size="sm">
              🎯 Рассчитать стоимость
            </Button>
          </div>

          {/* Mobile Menu Toggle */}
          {isMobileMenuOpen && (
            <button 
              onClick={onToggleMobileMenu}
              className="lg:hidden p-2 rounded-lg hover:bg-gray-100"
            >
              ✕
            </button>
          )}
        </div>

        {/* Mobile Navigation */}
        {isMobileMenuOpen && (
          <div className="lg:hidden py-4 border-t border-gray-200">
            <nav className="flex flex-col gap-2">
              {navItems.map((item, index) => (
                <Link
                  key={index}
                  to={item.href}
                  onClick={onToggleMobileMenu}
                  className={`px-4 py-3 rounded-lg text-base font-medium transition-colors ${
                    location.pathname === item.href || location.pathname.includes(item.href)
                      ? 'text-primary bg-gray-100'
                      : 'text-secondary hover:bg-gray-100'
                  }`}
                >
                  {item.label}
                </Link>
              ))}
            </nav>

            <div className="py-4 border-t border-gray-200 space-y-3">
              <Button variant="outline" size="md" className="w-full justify-center">
                📞 +7 (903) 851-71-67
              </Button>
              <Button variant="primary" size="md" className="w-full justify-center">
                🎯 Рассчитать стоимость
              </Button>
            </div>
          </div>
        )}
      </nav>
    </header>
  )
}

/**
 * Header with Contact Form Modal
 */
export function HeaderWithContact({ onOpenContactModal }) {
  return (
    <Header>
      {/* Add contact button in desktop nav */}
      <div className="hidden md:block lg:hidden absolute top-24 right-4">
        <Button 
          variant="primary" 
          size="sm"
          onClick={onOpenContactModal}
        >
          📞 Позвонить
        </Button>
      </div>
    </Header>
  )
}

export function ContactFormModal({ isOpen, onClose }) {
  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center p-4 bg-black bg-opacity-50">
      <div className="bg-white rounded-xl shadow-2xl w-full max-w-md p-6 animate-fade-in-up">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-xl font-bold text-secondary">Свяжитесь с нами</h3>
          <button 
            onClick={onClose}
            className="p-2 rounded-full hover:bg-gray-100 transition-colors"
          >
            ✕
          </button>
        </div>

        {/* Contact form would go here */}
      </div>
    </div>
  )
}