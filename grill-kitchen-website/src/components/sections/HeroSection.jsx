import { motion } from 'framer-motion'
import Button from '../ui/Button'

const containerVariants = {
  hidden: { opacity: 0 },
  visible: { 
    opacity: 1,
    transition: { 
      staggerChildren: 0.2,
      delayChildren: 0.3
    }
  }
}

const itemVariants = {
  hidden: { opacity: 0, y: 50 },
  visible: { 
    opacity: 1, 
    y: 0,
    transition: { duration: 0.6 }
  }
}

export default function HeroSection() {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden bg-gradient-to-br from-primary via-secondary to-gray-900">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute top-20 left-20 w-72 h-72 bg-white rounded-full blur-3xl"></div>
        <div className="absolute bottom-20 right-20 w-96 h-96 bg-primary rounded-full blur-3xl"></div>
      </div>

      {/* Content */}
      <motion.div 
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="relative z-10 max-w-7xl mx-auto px-4 md:px-6 text-center"
      >
        <motion.h1 
          variants={itemVariants}
          className="text-4xl md:text-5xl lg:text-7xl font-bold text-white mb-6 leading-tight"
        >
          Премиальные{' '}
          <span className="text-primary">Гриль-Кухни</span>
          <br />
          Для Вашей Террасы
        </motion.h1>

        <motion.p 
          variants={itemVariants}
          className="text-lg md:text-xl text-gray-300 mb-8 max-w-3xl mx-auto leading-relaxed"
        >
          Профессиональное проектирование и изготовление гриль-кухен из стали и композита HPL. 
          Открытые и закрытые зоны, встроенная техника, монтаж под ключ.
        </motion.p>

        <motion.div variants={itemVariants} className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-12">
          <Button variant="primary" size="lg">
            🎯 Рассчитать стоимость
          </Button>
          <Button variant="outline" size="lg" className="border-white text-white hover:bg-white hover:text-primary">
            👀 Смотреть портфолио
          </Button>
        </motion.div>

        {/* Stats */}
        <motion.div variants={itemVariants} className="grid grid-cols-3 gap-8 max-w-2xl mx-auto pt-8 border-t border-white border-opacity-20">
          <div>
            <p className="text-3xl font-bold text-white mb-1">5+</p>
            <p className="text-sm text-gray-400">Лет опыта</p>
          </div>
          <div>
            <p className="text-3xl font-bold text-primary mb-1">200+</p>
            <p className="text-sm text-gray-400">Изготовленных кухонь</p>
          </div>
          <div>
            <p className="text-3xl font-bold text-white mb-1">5 лет</p>
            <p className="text-sm text-gray-400">Гарантии качества</p>
          </div>
        </motion.div>
      </motion.div>

      {/* Scroll Indicator */}
      <motion.div 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1, y: [0, 10, 0] }}
        transition={{ delay: 1.5, duration: 2, repeat: Infinity }}
        className="absolute bottom-8 left-1/2 transform -translate-x-1/2"
      >
        <div className="w-6 h-10 border-2 border-white border-opacity-50 rounded-full flex justify-center pt-2">
          <div className="w-1.5 h-3 bg-white rounded-full"></div>
        </div>
      </motion.div>
    </section>
  )
}