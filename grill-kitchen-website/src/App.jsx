import { useState } from 'react'
import Header from './components/layout/Header'
import HeroSection from './components/sections/HeroSection'
import FeaturesSection from './components/sections/FeaturesSection'
import WorkProcessSection from './components/sections/WorkProcessSection'
import CalculatorSection from './components/sections/CalculatorSection'
import PortfolioSection from './components/sections/PortfolioSection'
import VideoSection from './components/sections/VideoSection'
import ReviewsSection from './components/sections/ReviewsSection'
import FaqSection from './components/sections/FaqSection'
import BrandsSection from './components/sections/BrandsSection'
import StoresSection from './components/sections/StoresSection'
import Footer from './components/layout/Footer'

function App() {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  
  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <Header 
        isMobileMenuOpen={isMobileMenuOpen}
        onToggleMobileMenu={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
      />
      
      {/* Main Content */}
      <main>
        <HeroSection />
        <FeaturesSection />
        <WorkProcessSection />
        <CalculatorSection />
        <PortfolioSection />
        <VideoSection />
        <ReviewsSection />
        <FaqSection />
        <BrandsSection />
        <StoresSection />
      </main>
      
      {/* Footer */}
      <Footer />
    </div>
  )
}

export default App