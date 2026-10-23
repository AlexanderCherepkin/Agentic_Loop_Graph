import { motion } from 'framer-motion'
import Button from '../ui/Button'

const features = [
  {
    icon: '🎨',
    title: 'Индивидуальный дизайн',
    description: 'Разработка уникального проекта с учётом всех пожеланий и особенностей вашего участка.',
    color: 'from-primary to-red-600'
  },
  {
    icon: '⚙️',
    title: 'Профессиональное изготовление',
    description: 'Изготовление на современном оборудовании с использованием качественных материалов.',
    color: 'from-secondary to-gray-800'
  },
  {
    icon: '🔧',
    title: 'Монтаж под ключ',
    description: 'Профессиональная установка и подключение всех элементов гриль-кухни.',
    color: 'from-primary to-red-600'
  },
  {
    icon: '💎',
    title: 'Премиальные материалы',
    description: 'Сталь, композит HPL и другие материалы высшего качества для долговечности.',
    color: 'from-secondary to-gray-800'
  },
  {
    icon: '📋',
    title: 'Проектирование',
    description: 'Детальные чертежи, 3D визуализация и расчёт стоимости до начала работ.',
    color: 'from-primary to-red-600'
  },
  {
    icon: '🚚',
    title: 'Бесплатная доставка',
    description: 'Доставка готовой продукции бесплатно при заказе от 100 000 ₽.',
    color: 'from-secondary to-gray-800'
  }
]

const containerVariants = {
  hidden: { opacity: 0 },
  visible: { 
    opacity: 1,
    transition: { staggerChildren: 0.15 }
  }
}

const itemVariants = {
  hidden: { opacity: 0, y: 30 },
  visible: { 
    opacity: 1, 
    y: 0,
    transition: { duration: 0.5 }
  }
}

export default function FeaturesSection() {
  return (
    <section className="py-20 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 md:px-6">
        {/* Section Header */}
        <motion.div 
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl md:text-4xl font-bold text-secondary mb-4">
            Наши преимущества
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Мы предлагаем комплексное решение для создания идеальной гриль-зоны на вашем участке
          </p>
        </motion.div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              variants={itemVariants}
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true }}
              className="bg-white rounded-xl p-8 shadow-md hover:shadow-xl transition-all duration-300 group border border-gray-100"
            >
              <div className={`w-14 h-14 bg-gradient-to-br ${feature.color} rounded-lg flex items-center justify-center text-2xl mb-6 group-hover:scale-110 transition-transform`}>
                {feature.icon}
              </div>
              <h3 className="text-xl font-bold text-secondary mb-3">
                {feature.title}
              </h3>
              <p className="text-gray-600 leading-relaxed">
                {feature.description}
              </p>
            </motion.div>
          ))}
        </div>

        {/* CTA */}
        <motion.div 
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="mt-16 text-center"
        >
          <Button variant="primary" size="lg">
            📞 Заказать консультацию
          </Button>
        </motion.div>
      </div>
    </section>
  )
}