import { motion } from 'framer-motion'

const steps = [
  {
    number: '01',
    title: 'Консультация',
    description: 'Обсуждаем ваши идеи, требования и бюджет. Получаете бесплатную консультацию от наших экспертов.',
    icon: '💬'
  },
  {
    number: '02',
    title: 'Проектирование',
    description: 'Разрабатываем индивидуальный проект с детальной проработкой всех элементов и расчётом стоимости.',
    icon: '📐'
  },
  {
    number: '03',
    title: 'Изготовление',
    description: 'Производим гриль-кухню на современном оборудовании с использованием качественных материалов.',
    icon: '⚙️'
  },
  {
    number: '04',
    title: 'Доставка и монтаж',
    description: 'Бесплатная доставка до объекта и профессиональный монтаж под ключ.',
    icon: '🛠️'
  }
]

export default function WorkProcessSection() {
  return (
    <section className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 md:px-6">
        {/* Section Header */}
        <motion.div 
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl md:text-4xl font-bold text-secondary mb-4">
            Процесс работы
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Прозрачный и понятный путь от идеи до готовой гриль-кухни на вашем участке
          </p>
        </motion.div>

        {/* Steps */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {steps.map((step, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              className="relative"
            >
              {/* Step Number */}
              <div className="text-6xl font-bold text-primary mb-4">{step.number}</div>
              
              {/* Icon */}
              <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center text-2xl mb-4 mx-auto">
                {step.icon}
              </div>

              {/* Content */}
              <h3 className="text-xl font-bold text-secondary mb-3 text-center">
                {step.title}
              </h3>
              <p className="text-gray-600 leading-relaxed">
                {step.description}
              </p>
            </motion.div>
          ))}
        </div>

        {/* Connection Lines (Desktop) */}
        <div className="hidden lg:block absolute top-full left-1/3 w-px h-24 bg-gradient-to-b from-primary to-transparent"></div>
        <div className="hidden lg:block absolute top-full right-1/3 w-px h-24 bg-gradient-to-b from-primary to-transparent"></div>

        {/* CTA */}
        <motion.div 
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="mt-16 text-center"
        >
          <p className="text-lg text-gray-600 mb-4">Готовы начать проект?</p>
          <a 
            href="#calculator" 
            className="inline-block px-8 py-3 bg-primary text-white rounded-full font-semibold hover:bg-red-700 transition-colors duration-300"
          >
            📋 Заполнить анкету
          </a>
        </motion.div>
      </div>
    </section>
  )
}