import React, { useState } from 'react';

const CalculatorSection = () => {
  const [selectedGrillSize, setSelectedGrillSize] = useState('');
  const [selectedFeatures, setSelectedFeatures] = useState({});
  const [estimatedPrice, setEstimatedPrice] = useState(0);

  // Размеры грилей (цена за базовую модель)
  const grillSizes = {
    'small': { name: 'Малый', price: 15000 },
    'medium': { name: 'Средний', price: 25000 },
    'large': { name: 'Большой', price: 35000 }
  };

  // Дополнительные опции и их цены
  const features = [
    { id: 'lid_insulation', name: 'Термоизоляция крышки', price: 2000 },
    { id: 'side_burner', name: 'Доп. горелка сбоку', price: 3500 },
    { id: 'smoker_box', name: 'Ящик для дыма', price: 1500 },
    { id: 'rotisserie', name: 'Шашлычница', price: 2500 },
    { id: 'grate_coating', name: 'Премиум покрытие решетки', price: 3000 }
  ];

  const handleSizeChange = (size) => {
    setSelectedGrillSize(size);
    // Сбрасываем опции при смене размера
    const newFeatures = {};
    features.forEach(f => newFeatures[f.id] = false);
    setSelectedFeatures(newFeatures);
  };

  const toggleFeature = (featureId) => {
    setSelectedFeatures(prev => ({
      ...prev,
      [featureId]: !prev[featureId]
    }));
  };

  // Расчет итоговой цены
  React.useEffect(() => {
    let total = 0;

    if (selectedGrillSize) {
      total += grillSizes[selectedGrillSize].price;
    }

    features.forEach(feature => {
      if (selectedFeatures[feature.id]) {
        total += feature.price;
      }
    });

    setEstimatedPrice(total);
  }, [selectedGrillSize, selectedFeatures]);

  const handleRequestQuote = () => {
    alert(`Спасибо за ваш запрос!

Выбранный гриль: ${grillSizes[selectedGrillSize]?.name || 'Не выбран'}
Дополнительные опции: ${features.filter(f => selectedFeatures[f.id]).length} шт.
Ориентировочная цена: ${estimatedPrice.toLocaleString()} руб. 

Наш менеджер свяжется с вами в ближайшее время.`);
  };

  return (
    <section className="calculator-section" id="calculator">
      <div className="container">
        <h2>Расчет стоимости вашего гриля</h2>
        <p>Соберите свой идеальный гриль и узнайте ориентировочную стоимость</p>

        <div className="calculator-wrapper">
          {/* Выбор размера */}
          <div className="calculation-step">
            <h3>1. Выберите размер гриля</h3>

            <div className="size-options">
              {Object.entries(grillSizes).map(([key, size]) => (
                <button
                  key={key}
                  className={`size-btn ${selectedGrillSize === key ? 'active' : ''}`}
                  onClick={() => handleSizeChange(key)}
                >
                  {size.name} — {size.price.toLocaleString()} руб.
                </button>
              ))}
            </div>
          </div>

          {/* Дополнительные опции */}
          <div className="calculation-step">
            <h3>2. Выберите дополнительные опции</h3>
            <div className="features-list">
              {features.map(feature => (
                <label key={feature.id} className={`feature-label ${selectedFeatures[feature.id] ? 'checked' : ''}`}>
                  <input
                    type="checkbox"
                    checked={!!selectedFeatures[feature.id]}
                    onChange={() => toggleFeature(feature.id)}
                  />
                  {feature.name} — {feature.price.toLocaleString()} руб.
                </label>
              ))}
            </div>
          </div>

          {/* Итоговая цена */}
          <div className="calculation-step">
            <h3>Итоговая стоимость</h3>
            <p className="total-price">{estimatedPrice.toLocaleString()} руб.</p>
          </div>
        </div>

        {/* Форма запроса */}
        <form onSubmit={handleRequestQuote}>
          <Button variant="gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-200 shadow-md hover:shadow-lg" type="submit">
            Рассчитать стоимость
          </Button>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Дополнительные пожелания
            </label>
            <Textarea 
              name="comments"
              placeholder="Опишите ваши идеи, требования или особые пожелания..."
              rows={3}
            />
          </div>
        </form>

        <p className="text-xs text-gray-500 mt-3 text-center">
          *Это ориентировочная расчетная стоимость. Точную цену уточняйте у менеджера.
        </p>
      </div>
    </section>
  )
}

export default CalculatorSection;
import React, { useState } from 'react';

const CalculatorSection = () => {
  const [selectedGrillSize, setSelectedGrillSize] = useState('');
  const [selectedFeatures, setSelectedFeatures] = useState({});
  const [estimatedPrice, setEstimatedPrice] = useState(0);

  // Размеры грилей (цена за базовую модель)
  const grillSizes = {
    'small': { name: 'Малый', price: 15000 },
    'medium': { name: 'Средний', price: 25000 },
    'large': { name: 'Большой', price: 35000 }
  };

  // Дополнительные опции и их цены
  const features = [
    { id: 'lid_insulation', name: 'Термоизоляция крышки', price: 2000 },
    { id: 'side_burner', name: 'Доп. горелка сбоку', price: 3500 },
    { id: 'smoker_box', name: 'Ящик для дыма', price: 1500 },
    { id: 'rotisserie', name: 'Шашлычница', price: 2500 },
    { id: 'grate_coating', name: 'Премиум покрытие решетки', price: 3000 }
  ];

  const handleSizeChange = (size) => {
    setSelectedGrillSize(size);
    // Сбрасываем опции при смене размера
    const newFeatures = {};
    features.forEach(f => newFeatures[f.id] = false);
    setSelectedFeatures(newFeatures);
  };

  const toggleFeature = (featureId) => {
    setSelectedFeatures(prev => ({
      ...prev,
      [featureId]: !prev[featureId]
    }));
  };

  // Расчет итоговой цены
  React.useEffect(() => {
    let total = 0;

    if (selectedGrillSize) {
      total += grillSizes[selectedGrillSize].price;
    }

    features.forEach(feature => {
      if (selectedFeatures[feature.id]) {
        total += feature.price;
      }
    });

    setEstimatedPrice(total);
  }, [selectedGrillSize, selectedFeatures]);

  const handleRequestQuote = () => {
    alert(`Спасибо за ваш запрос!

Выбранный гриль: ${grillSizes[selectedGrillSize]?.name || 'Не выбран'}
Дополнительные опции: ${features.filter(f => selectedFeatures[f.id]).length} шт.
Ориентировочная цена: ${estimatedPrice.toLocaleString()} руб. 

Наш менеджер свяжется с вами в ближайшее время.`);
  };

  return (
    <section className="calculator-section" id="calculator">
      <div className="container">
        <h2>Расчет стоимости вашего гриля</h2>
        <p>Соберите свой идеальный гриль и узнайте ориентировочную стоимость</p>

        <div className="calculator-wrapper">
          {/* Выбор размера */}
          <div className="calculation-step">
            <h3>1. Выберите размер гриля</h3>

            <div className="size-options">
              {Object.entries(grillSizes).map(([key, size]) => (
                <button
                  key={key}
                  className={`size-btn ${selectedGrillSize === key ? 'active' : ''}`}
                  onClick={() => handleSizeChange(key)}
                >
                  {size.name} — {size.price.toLocaleString()} руб.
                </button>
              ))}
            </div>
          </div>

          {/* Дополнительные опции */}
          <div className="calculation-step">
            <h3>2. Выберите дополнительные опции</h3>
            <div className="features-list">
              {features.map(feature => (
                <label key={feature.id} className={`feature-label ${selectedFeatures[feature.id] ? 'checked' : ''}`}>
                  <input
                    type="checkbox"
                    checked={!!selectedFeatures[feature.id]}
                    onChange={() => toggleFeature(feature.id)}
                  />
                  {feature.name} — {feature.price.toLocaleString()} руб.
                </label>
              ))}
            </div>
          </div>

          {/* Итоговая цена */}
          <div className="calculation-step">
            <h3>Итоговая стоимость</h3>
            <p className="total-price">{estimatedPrice.toLocaleString()} руб.</p>
          </div>
        </div>

        {/* Форма запроса */}
        <form onSubmit={handleRequestQuote}>
          <Button variant="gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-200 shadow-md hover:shadow-lg" type="submit">
            Рассчитать стоимость
          </Button>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Дополнительные пожелания
            </label>
            <Textarea 
              name="comments"
              placeholder="Опишите ваши идеи, требования или особые пожелания..."
              rows={3}
            />
          </div>
        </form>

        <p className="text-xs text-gray-500 mt-3 text-center">
          *Это ориентировочная расчетная стоимость. Точную цену уточняйте у менеджера.
        </p>
      </div>
    </section>
  )
}

export default CalculatorSection;
import React, { useState } from 'react';

const CalculatorSection = () => {
  const [selectedGrillSize, setSelectedGrillSize] = useState('');
  const [selectedFeatures, setSelectedFeatures] = useState({});
  const [estimatedPrice, setEstimatedPrice] = useState(0);

  // Размеры грилей (цена за базовую модель)
  const grillSizes = {
    'small': { name: 'Малый', price: 15000 },
    'medium': { name: 'Средний', price: 25000 },
    'large': { name: 'Большой', price: 35000 }
  };

  // Дополнительные опции и их цены
  const features = [
    { id: 'lid_insulation', name: 'Термоизоляция крышки', price: 2000 },
    { id: 'side_burner', name: 'Доп. горелка сбоку', price: 3500 },
    { id: 'smoker_box', name: 'Ящик для дыма', price: 1500 },
    { id: 'rotisserie', name: 'Шашлычница', price: 2500 },
    { id: 'grate_coating', name: 'Премиум покрытие решетки', price: 3000 }
  ];

  const handleSizeChange = (size) => {
    setSelectedGrillSize(size);
    // Сбрасываем опции при смене размера
    const newFeatures = {};
    features.forEach(f => newFeatures[f.id] = false);
    setSelectedFeatures(newFeatures);
  };

  const toggleFeature = (featureId) => {
    setSelectedFeatures(prev => ({
      ...prev,
      [featureId]: !prev[featureId]
    }));
  };

  // Расчет итоговой цены
  React.useEffect(() => {
    let total = 0;

    if (selectedGrillSize) {
      total += grillSizes[selectedGrillSize].price;
    }

    features.forEach(feature => {
      if (selectedFeatures[feature.id]) {
        total += feature.price;
      }
    });

    setEstimatedPrice(total);
  }, [selectedGrillSize, selectedFeatures]);

  const handleRequestQuote = () => {
    alert(`Спасибо за ваш запрос!

Выбранный гриль: ${grillSizes[selectedGrillSize]?.name || 'Не выбран'}
Дополнительные опции: ${features.filter(f => selectedFeatures[f.id]).length} шт.
Ориентировочная цена: ${estimatedPrice.toLocaleString()} руб. 

Наш менеджер свяжется с вами в ближайшее время.`);
  };

  return (
    <section className="calculator-section" id="calculator">
      <div className="container">
        <h2>Расчет стоимости вашего гриля</h2>
        <p>Соберите свой идеальный гриль и узнайте ориентировочную стоимость</p>

        <div className="calculator-wrapper">
          {/* Выбор размера */}
          <div className="calculation-step">
            <h3>1. Выберите размер гриля</h3>

            <div className="size-options">
              {Object.entries(grillSizes).map(([key, size]) => (
                <button
                  key={key}
                  className={`size-btn ${selectedGrillSize === key ? 'active' : ''}`}
                  onClick={() => handleSizeChange(key)}
                >
                  {size.name} — {size.price.toLocaleString()} руб.
                </button>
              ))}
            </div>
          </div>

          {/* Дополнительные опции */}
          <div className="calculation-step">
            <h3>2. Выберите дополнительные опции</h3>
            <div className="features-list">
              {features.map(feature => (
                <label key={feature.id} className={`feature-label ${selectedFeatures[feature.id] ? 'checked' : ''}`}>
                  <input
                    type="checkbox"
                    checked={!!selectedFeatures[feature.id]}
                    onChange={() => toggleFeature(feature.id)}
                  />
                  {feature.name} — {feature.price.toLocaleString()} руб.
                </label>
              ))}
            </div>
          </div>

          {/* Итоговая цена */}
          <div className="calculation-step">
            <h3>Итоговая стоимость</h3>
            <p className="total-price">{estimatedPrice.toLocaleString()} руб.</p>
          </div>
        </div>

        {/* Форма запроса */}
        <form onSubmit={handleRequestQuote}>
          <Button variant="gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-200 shadow-md hover:shadow-lg" type="submit">
            Рассчитать стоимость
          </Button>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Дополнительные пожелания
            </label>
            <Textarea 
              name="comments"
              placeholder="Опишите ваши идеи, требования или особые пожелания..."
              rows={3}
            />
          </div>
        </form>

        <p className="text-xs text-gray-500 mt-3 text-center">
          *Это ориентировочная расчетная стоимость. Точную цену уточняйте у менеджера.
        </p>
      </div>
    </section>
  )
}

export default CalculatorSection;
import React, { useState } from 'react';

const CalculatorSection = () => {
  const [selectedGrillSize, setSelectedGrillSize] = useState('');
  const [selectedFeatures, setSelectedFeatures] = useState({});
  const [estimatedPrice, setEstimatedPrice] = useState(0);

  // Размеры грилей (цена за базовую модель)
  const grillSizes = {
    'small': { name: 'Малый', price: 15000 },
    'medium': { name: 'Средний', price: 25000 },
    'large': { name: 'Большой', price: 35000 }
  };

  // Дополнительные опции и их цены
  const features = [
    { id: 'lid_insulation', name: 'Термоизоляция крышки', price: 2000 },
    { id: 'side_burner', name: 'Доп. горелка сбоку', price: 3500 },
    { id: 'smoker_box', name: 'Ящик для дыма', price: 1500 },
    { id: 'rotisserie', name: 'Шашлычница', price: 2500 },
    { id: 'grate_coating', name: 'Премиум покрытие решетки', price: 3000 }
  ];

  const handleSizeChange = (size) => {
    setSelectedGrillSize(size);
    // Сбрасываем опции при смене размера
    const newFeatures = {};
    features.forEach(f => newFeatures[f.id] = false);
    setSelectedFeatures(newFeatures);
  };

  const toggleFeature = (featureId) => {
    setSelectedFeatures(prev => ({
      ...prev,
      [featureId]: !prev[featureId]
    }));
  };

  // Расчет итоговой цены
  React.useEffect(() => {
    let total = 0;

    if (selectedGrillSize) {
      total += grillSizes[selectedGrillSize].price;
    }

    features.forEach(feature => {
      if (selectedFeatures[feature.id]) {
        total += feature.price;
      }
    });

    setEstimatedPrice(total);
  }, [selectedGrillSize, selectedFeatures]);

  const handleRequestQuote = () => {
    alert(`Спасибо за ваш запрос!\n\nВыбранный гриль: ${grillSizes[selectedGrillSize]?.name || 'Не выбран'}\nДополнительные опции: ${features.filter(f => selectedFeatures[f.id]).length} шт.\nОриентировочная цена: ${estimatedPrice.toLocaleString()} руб. \n\nНаш менеджер свяжется с вами в ближайшее время.`);
  };

  return (
    <section className="calculator-section" id="calculator">
      <div className="container">
        <h2>Расчет стоимости вашего гриля</h2>
        <p>Соберите свой идеальный гриль и узнайте ориентировочную стоимость</p>

        <div className="calculator-wrapper">
          {/* Выбор размера */}
          <div className="calculation-step">
            <h3>1. Выберите размер гриля</h3>



export default CalculatorSection;



export default CalculatorSection;

export default CalculatorSection;





export default CalculatorSection;

export default CalculatorSection;

export default CalculatorSection;

export default CalculatorSection;



export default CalculatorSection;
export default CalculatorSection;


export default CalculatorSection;
            <div className="size-options">
              {Object.entries(grillSizes).map(([key, size]) => (
                <button
                  key={key}
                  className={`size-btn ${selectedGrillSize === key ? 'active' : ''}`}
                  onClick={() => handleSizeChange(key)}
                >
                  {size.name} — {size.price.toLocaleString()} руб.
                </button>
              ))}
            </div>
          </div>

          {/* Дополнительные опции */}
          <div className="calculation-step">
            <h3>2. Выберите дополнительные опции</h3>
            <div className="features-list">
              {features.map(feature => (
                <label key={feature.id} className={`feature-label ${selectedFeatures[feature.id] ? 'checked' : ''}`}>
                  <input
                    type="checkbox"
                    checked={!!selectedFeatures[feature.id]}
                    onChange={() => toggleFeature(feature.id)}
                  />
                  <span>{feature.name}</span>
                  <span className="price">+{feature.price.toLocaleString()} руб.</span>
                </label>
              ))}
            </div>
          </div>

          {/* Итоговая цена */}
          <div className="calculation-summary">
            <h3>Итого:</h3>
            <div className="total-price">
              {estimatedPrice.toLocaleString()} руб.
            </div>
            <button 
              className="quote-btn" 
              onClick={handleRequestQuote}
              disabled={!selectedGrillSize}
            >
              Запросить расчет
            </button>
          </div>
        </div>

        {/* Инфо блок */}
        <div className="calculator-info">
          <p><strong>Примечание:</strong> Данная стоимость является ориентировочной и может изменяться в зависимости от наличия компонентов на складе.</p>
        </div>
      </div>
    </section>
  );
};

export default CalculatorSection;
import React, { useState } from 'react';

const CalculatorSection = () => {
  const [selectedGrillSize, setSelectedGrillSize] = useState('');
  const [selectedFeatures, setSelectedFeatures] = useState({});
  const [estimatedPrice, setEstimatedPrice] = useState(0);

  // Размеры грилей (цена за базовую модель)
  const grillSizes = {
    'small': { name: 'Малый', price: 15000 },
    'medium': { name: 'Средний', price: 25000 },
    'large': { name: 'Большой', price: 35000 }
  };

  // Дополнительные опции и их цены
  const features = [
    { id: 'lid_insulation', name: 'Термоизоляция крышки', price: 2000 },
    { id: 'side_burner', name: 'Доп. горелка сбоку', price: 3500 },
    { id: 'smoker_box', name: 'Ящик для дыма', price: 1500 },
    { id: 'rotisserie', name: 'Шашлычница', price: 2500 },
    { id: 'grate_coating', name: 'Премиум покрытие решетки', price: 3000 }
  ];

  const handleSizeChange = (size) => {
    setSelectedGrillSize(size);
    // Сбрасываем опции при смене размера
    const newFeatures = {};
    features.forEach(f => newFeatures[f.id] = false);
    setSelectedFeatures(newFeatures);
  };

  const toggleFeature = (featureId) => {
    setSelectedFeatures(prev => ({
      ...prev,
      [featureId]: !prev[featureId]
    }));
  };

  // Расчет итоговой цены
  React.useEffect(() => {
    let total = 0;

    if (selectedGrillSize) {
      total += grillSizes[selectedGrillSize].price;
    }

    features.forEach(feature => {
      if (selectedFeatures[feature.id]) {
        total += feature.price;
      }
    });

    setEstimatedPrice(total);
  }, [selectedGrillSize, selectedFeatures]);

  const handleRequestQuote = () => {
    alert(`Спасибо за ваш запрос!\n\nВыбранный гриль: ${grillSizes[selectedGrillSize]?.name || 'Не выбран'}\nДополнительные опции: ${features.filter(f => selectedFeatures[f.id]).length} шт.\nОриентировочная цена: ${estimatedPrice.toLocaleString()} руб. \n\nНаш менеджер свяжется с вами в ближайшее время.`);
  };


export default CalculatorSection;


export default CalculatorSection;


export default CalculatorSection;




export default CalculatorSection;



export default CalculatorSection;

export default CalculatorSection;
export default CalculatorSection;
import React, { useState } from 'react';

const CalculatorSection = () => {
  const [selectedGrillSize, setSelectedGrillSize] = useState('');
  const [selectedFeatures, setSelectedFeatures] = useState({});
  const [estimatedPrice, setEstimatedPrice] = useState(0);

  // Размеры грилей (цена за базовую модель)
  const grillSizes = {
    'small': { name: 'Малый', price: 15000 },
    'medium': { name: 'Средний', price: 25000 },
    'large': { name: 'Большой', price: 35000 }
  };

  // Дополнительные опции и их цены
  const features = [
    { id: 'lid_insulation', name: 'Термоизоляция крышки', price: 2000 },
    { id: 'side_burner', name: 'Доп. горелка сбоку', price: 3500 },
    { id: 'smoker_box', name: 'Ящик для дыма', price: 1500 },
    { id: 'rotisserie', name: 'Шашлычница', price: 2500 },
    { id: 'grate_coating', name: 'Премиум покрытие решетки', price: 3000 }
  ];

  const handleSizeChange = (size) => {
    setSelectedGrillSize(size);
    // Сбрасываем опции при смене размера
    const newFeatures = {};
    features.forEach(f => newFeatures[f.id] = false);
    setSelectedFeatures(newFeatures);
  };

  const toggleFeature = (featureId) => {
    setSelectedFeatures(prev => ({
      ...prev,
      [featureId]: !prev[featureId]
    }));
  };

  // Расчет итоговой цены
  React.useEffect(() => {
    let total = 0;

    if (selectedGrillSize) {
      total += grillSizes[selectedGrillSize].price;
    }

    features.forEach(feature => {
      if (selectedFeatures[feature.id]) {
        total += feature.price;
      }
    });

    setEstimatedPrice(total);
  }, [selectedGrillSize, selectedFeatures]);

  const handleRequestQuote = () => {
    alert(`Спасибо за ваш запрос!\n\nВыбранный гриль: ${grillSizes[selectedGrillSize]?.name || 'Не выбран'}\nДополнительные опции: ${features.filter(f => selectedFeatures[f.id]).length} шт.\nОриентировочная цена: ${estimatedPrice.toLocaleString()} руб. \n\nНаш менеджер свяжется с вами в ближайшее время.`);
  };

  return (
    <section className="calculator-section" id="calculator">
      <div className="container">
        <h2>Расчет стоимости вашего гриля</h2>
        <p>Соберите свой идеальный гриль и узнайте ориентировочную стоимость</p>

        <div className="calculator-wrapper">
          {/* Выбор размера */}
          <div className="calculation-step">
            <h3>1. Выберите размер гриля</h3>
            <div className="size-options">
              {Object.entries(grillSizes).map(([key, size]) => (
                <button
                  key={key}
                  className={`size-btn ${selectedGrillSize === key ? 'active' : ''}`}
                  onClick={() => handleSizeChange(key)}
                >
                  {size.name} — {size.price.toLocaleString()} руб.
                </button>
              ))}
            </div>
          </div>

          {/* Дополнительные опции */}
          <div className="calculation-step">
            <h3>2. Выберите дополнительные опции</h3>
            <div className="features-list">
              {features.map(feature => (
                <label key={feature.id} className={`feature-label ${selectedFeatures[feature.id] ? 'checked' : ''}`}>
                  <input
                    type="checkbox"
                    checked={!!selectedFeatures[feature.id]}
                    onChange={() => toggleFeature(feature.id)}
                  />
                  <span>{feature.name}</span>
                  <span className="price">+{feature.price.toLocaleString()} руб.</span>
                </label>
              ))}
            </div>
          </div>

          {/* Итоговая цена */}
          <div className="calculation-summary">
            <h3>Итого:</h3>
            <div className="total-price">
              {estimatedPrice.toLocaleString()} руб.
            </div>
            <button 
              className="quote-btn" 
              onClick={handleRequestQuote}
              disabled={!selectedGrillSize}
            >
              Запросить расчет
            </button>
          </div>
        </div>

        {/* Инфо блок */}
        <div className="calculator-info">
          <p><strong>Примечание:</strong> Данная стоимость является ориентировочной и может изменяться в зависимости от наличия компонентов на складе.</p>
        </div>
      </div>
    </section>
  );
};

export default CalculatorSection;
  return (
    <section className="calculator-section" id="calculator">
      <div className="container">
        <h2>Расчет стоимости вашего гриля</h2>
        <p>Соберите свой идеальный гриль и узнайте ориентировочную стоимость</p>

        <div className="calculator-wrapper">
          {/* Выбор размера */}
          <div className="calculation-step">
            <h3>1. Выберите размер гриля</h3>
            <div className="size-options">
              {Object.entries(grillSizes).map(([key, size]) => (
                <button
                  key={key}
                  className={`size-btn ${selectedGrillSize === key ? 'active' : ''}`}
                  onClick={() => handleSizeChange(key)}
                >
                  {size.name} — {size.price.toLocaleString()} руб.
                </button>
              ))}
            </div>
          </div>

          {/* Дополнительные опции */}
          <div className="calculation-step">
            <h3>2. Выберите дополнительные опции</h3>
            <div className="features-list">
              {features.map(feature => (
                <label key={feature.id} className={`feature-label ${selectedFeatures[feature.id] ? 'checked' : ''}`}>
                  <input
                    type="checkbox"
                    checked={!!selectedFeatures[feature.id]}
                    onChange={() => toggleFeature(feature.id)}
                  />
                  <span>{feature.name}</span>
                  <span className="price">+{feature.price.toLocaleString()} руб.</span>
                </label>
              ))}
            </div>
          </div>

          {/* Итоговая цена */}
          <div className="calculation-summary">
            <h3>Итого:</h3>
            <div className="total-price">
              {estimatedPrice.toLocaleString()} руб.
            </div>
            <button 
              className="quote-btn" 
              onClick={handleRequestQuote}
              disabled={!selectedGrillSize}
            >
              Запросить расчет
            </button>
          </div>
        </div>

        {/* Инфо блок */}
        <div className="calculator-info">
          <p><strong>Примечание:</strong> Данная стоимость является ориентировочной и может изменяться в зависимости от наличия компонентов на складе.</p>
        </div>
      </div>
    </section>
  );
};

export default CalculatorSection;
import React, { useState } from 'react';

const CalculatorSection = () => {
  const [selectedGrillSize, setSelectedGrillSize] = useState('');
  const [selectedFeatures, setSelectedFeatures] = useState({});
  const [estimatedPrice, setEstimatedPrice] = useState(0);

  // Размеры грилей (цена за базовую модель)
  const grillSizes = {
    'small': { name: 'Малый', price: 15000 },
    'medium': { name: 'Средний', price: 25000 },
    'large': { name: 'Большой', price: 35000 }
  };

  // Дополнительные опции и их цены
  const features = [
    { id: 'lid_insulation', name: 'Термоизоляция крышки', price: 2000 },
    { id: 'side_burner', name: 'Доп. горелка сбоку', price: 3500 },
    { id: 'smoker_box', name: 'Ящик для дыма', price: 1500 },
    { id: 'rotisserie', name: 'Шашлычница', price: 2500 },
    { id: 'grate_coating', name: 'Премиум покрытие решетки', price: 3000 }
  ];

  const handleSizeChange = (size) => {
    setSelectedGrillSize(size);
    // Сбрасываем опции при смене размера
    const newFeatures = {};
    features.forEach(f => newFeatures[f.id] = false);
    setSelectedFeatures(newFeatures);
  };

  const toggleFeature = (featureId) => {
    setSelectedFeatures(prev => ({
      ...prev,
      [featureId]: !prev[featureId]
    }));
  };

  // Расчет итоговой цены
  React.useEffect(() => {
    let total = 0;

    if (selectedGrillSize) {
      total += grillSizes[selectedGrillSize].price;
    }

    features.forEach(feature => {
      if (selectedFeatures[feature.id]) {
        total += feature.price;
      }
    });

    setEstimatedPrice(total);
  }, [selectedGrillSize, selectedFeatures]);

  const handleRequestQuote = () => {
    alert(`Спасибо за ваш запрос!\n\nВыбранный гриль: ${grillSizes[selectedGrillSize]?.name || 'Не выбран'}\nДополнительные опции: ${features.filter(f => selectedFeatures[f.id]).length} шт.\nОриентировочная цена: ${estimatedPrice.toLocaleString()} руб. \n\nНаш менеджер свяжется с вами в ближайшее время.`);
  };

  return (
    <section className="calculator-section" id="calculator">
      <div className="container">
        <h2>Расчет стоимости вашего гриля</h2>
        <p>Соберите свой идеальный гриль и узнайте ориентировочную стоимость</p>

        <div className="calculator-wrapper">
          {/* Выбор размера */}
          <div className="calculation-step">
            <h3>1. Выберите размер гриля</h3>
            <div className="size-options">
              {Object.entries(grillSizes).map(([key, size]) => (
                <button
                  key={key}
                  className={`size-btn ${selectedGrillSize === key ? 'active' : ''}`}
                  onClick={() => handleSizeChange(key)}
                >
                  {size.name} — {size.price.toLocaleString()} руб.
                </button>
              ))}
            </div>
          </div>

          {/* Дополнительные опции */}
          <div className="calculation-step">
            <h3>2. Выберите дополнительные опции</h3>
            <div className="features-list">
              {features.map(feature => (
                <label key={feature.id} className={`feature-label ${selectedFeatures[feature.id] ? 'checked' : ''}`}>
                  <input
                    type="checkbox"
                    checked={!!selectedFeatures[feature.id]}
                    onChange={() => toggleFeature(feature.id)}
                  />
                  <span>{feature.name}</span>
                  <span className="price">+{feature.price.toLocaleString()} руб.</span>
                </label>
              ))}
            </div>
          </div>

          {/* Итоговая цена */}
          <div className="calculation-summary">
            <h3>Итого:</h3>
            <div className="total-price">
              {estimatedPrice.toLocaleString()} руб.
            </div>
            <button 
              className="quote-btn" 
              onClick={handleRequestQuote}
              disabled={!selectedGrillSize}
            >
              Запросить расчет
            </button>
          </div>
        </div>

        {/* Инфо блок */}
        <div className="calculator-info">
          <p><strong>Примечание:</strong> Данная стоимость является ориентировочной и может изменяться в зависимости от наличия компонентов на складе.</p>
        </div>
      </div>
    </section>
  );
};

export default CalculatorSection;

import { useState } from 'react'
import Button from '../ui/Button'
import Input from '../ui/Input'
import Select from '../ui/Select'
import Textarea from '../ui/Textarea'

export default function CalculatorSection() {
  const [formData, setFormData] = useState({
    type: '',
    area: '',
    equipment: [],
    material: 'steel',
    installation: true,
    delivery: true
  })

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  const calculateTotal = () => {
    let total = 0
    
    if (formData.type === 'open') total += 150000
    else if (formData.type === 'closed') total += 250000
    else if (formData.type === 'hybrid') total += 350000
    
    const materialMultiplier = formData.material === 'hpl' ? 1.8 : 1.0
    total *= materialMultiplier
    
    if (formData.area) {
      total += formData.area * 40000
    }
    
    if (formData.installation) total += 25000
    if (formData.delivery) total += 5000
    
    return Math.round(total)
  }

  const handleSubmit = () => {
    console.log('Form data:', formData)
    console.log('Estimated cost:', calculateTotal())
  }



  return (
    <section id="calculator" className="py-20 bg-gradient-to-br from-primary via-red-700 to-secondary">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl md:text-4xl font-bold text-white text-center mb-4">
          Расчет стоимости гриль-кухни
        </h2>
        <p className="text-gray-200 text-center mb-12 max-w-2xl mx-auto">
          Рассчитайте примерную стоимость вашей будущей кухни с помощью нашего калькулятора
        </p>

        <form onSubmit={handleSubmit} className="space-y-8">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Column 1 */}
            <div className="lg:col-span-2 space-y-6">
              {/* Type Selection */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Тип гриль-кухни
                </label>
                <Select 
                  value={formData.type}
                  onChange={handleChange}
                  name="type"
                  options={[
                    { label: 'Открытая', value: 'open' },
                    { label: 'Закрытая', value: 'closed' },
                    { label: 'Комбинированная', value: 'hybrid' }
                  ]}
                />
              </div>

              {/* Material Selection */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Материал корпуса
                </label>
                <Select 
                  value={formData.material}
                  onChange={handleChange}
                  name="material"
                  options={[
                    { label: 'Сталь порошковая', value: 'steel' },
                    { label: 'Композит HPL', value: 'hpl' }
                  ]}
                />
              </div>

              {/* Area Input */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Площадь проекта (м²)
                </label>
                <Input 
                  type="number"
                  name="area"
                  value={formData.area}
                  onChange={handleChange}
                  placeholder="Например: 5"
                />
              </div>

              {/* Additional Options */}
              <div className="space-y-3">
                <label className="flex items-start gap-3 cursor-pointer">
                  <input 
                    type="checkbox"
                    name="installation"
                    checked={formData.installation}
                    onChange={handleChange}
                    className="mt-1 w-4 h-4 text-primary rounded focus:ring-primary"
                  />
                  <span className="text-sm text-gray-700">Монтаж под ключ (+25 000 ₽)</span>
                </label>

                <label className="flex items-start gap-3 cursor-pointer">
                  <input 
                    type="checkbox"
                    name="delivery"
                    checked={formData.delivery}
                    onChange={handleChange}
                    className="mt-1 w-4 h-4 text-primary rounded focus:ring-primary"
                  />
                  <span className="text-sm text-gray-700">Доставка (+5 000 ₽)</span>
                </label>
              </div>

              {/* Additional Info */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Дополнительные пожелания
                </label>
                <Textarea 
                  name="comments"
                  placeholder="Опишите ваши идеи, требования или особые пожелания..."
                  rows={3}
                />
              </div>
            </div>

            {/* Column 2 */}
            <div className="space-y-6">
              {/* Cost Summary Card */}
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h3 className="text-xl font-semibold text-gray-800 mb-4">Итоговая стоимость</h3>
                
                <div className="space-y-3 mb-6">
                  <div className="flex justify-between items-center py-2 border-b border-gray-100">
                    <span className="text-gray-600">Базовая цена:</span>
                    <span className="font-medium text-gray-900">
                      {formData.type ? calculateTotal() : 0.toLocaleString('ru-RU')} ₽
                    </span>
                  </div>
                </div>

                <Button 
                  type="submit"
                  variant="primary"
                  className="w-full py-3 text-lg"
                >
                  Заказать расчет
                </Button>
              </div>
            </div>
          </div>
        </form>
      </div>
    </section>
  )
}
import { useState } from 'react'
import Button from '../ui/Button'
import Input from '../ui/Input'
import Select from '../ui/Select'
import Textarea from '../ui/Textarea'

export default function CalculatorSection() {
  const [formData, setFormData] = useState({
    type: '',
    area: '',
    equipment: [],
    material: 'steel',
    installation: true,
    delivery: true
  })

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  const calculateTotal = () => {
    let total = 0
    
    if (formData.type === 'open') total += 150000
    else if (formData.type === 'closed') total += 250000
    else if (formData.type === 'hybrid') total += 350000
    
    const materialMultiplier = formData.material === 'hpl' ? 1.8 : 1.0
    total *= materialMultiplier
    
    if (formData.area) {
      total += formData.area * 40000
    }
    
    if (formData.installation) total += 25000
    if (formData.delivery) total += 5000
    
    return Math.round(total)
  }

  const handleSubmit = () => {
    console.log('Form data:', formData)
    console.log('Estimated cost:', calculateTotal())
  }


import { useState } from 'react'
import Button from '../ui/Button'
import Input from '../ui/Input'
import Select from '../ui/Select'
import Textarea from '../ui/Textarea'

export default function CalculatorSection() {
  const [formData, setFormData] = useState({
    type: '',
    area: '',
    equipment: [],
    material: 'steel',
    installation: true,
    delivery: true
  })

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  const calculateTotal = () => {
    let total = 0
    
    if (formData.type === 'open') total += 150000
    else if (formData.type === 'closed') total += 250000
    else if (formData.type === 'hybrid') total += 350000
    
    const materialMultiplier = formData.material === 'hpl' ? 1.8 : 1.0
    total *= materialMultiplier
    
    if (formData.area) {
      total += formData.area * 40000
    }
    
    if (formData.installation) total += 25000
    if (formData.delivery) total += 5000
    
    return Math.round(total)
  }

  const handleSubmit = () => {
    console.log('Form data:', formData)
    console.log('Estimated cost:', calculateTotal())
  }


import { useState } from 'react'
import Button from '../ui/Button'
import Input from '../ui/Input'
import Select from '../ui/Select'
import Textarea from '../ui/Textarea'

export default function CalculatorSection() {
  const [formData, setFormData] = useState({
    type: '',
    area: '',
    equipment: [],
    material: 'steel',
    installation: true,
    delivery: true
  })

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  const calculateTotal = () => {
    let total = 0
    
    if (formData.type === 'open') total += 150000
    else if (formData.type === 'closed') total += 250000
    else if (formData.type === 'hybrid') total += 350000
    
    const materialMultiplier = formData.material === 'hpl' ? 1.8 : 1.0
    total *= materialMultiplier
    
    if (formData.area) {
      total += formData.area * 40000
    }
    
    if (formData.installation) total += 25000
    if (formData.delivery) total += 5000
    
    return Math.round(total)
  }

  const handleSubmit = () => {
    console.log('Form data:', formData)
    console.log('Estimated cost:', calculateTotal())
  }


import { useState } from 'react'
import Button from '../ui/Button'
import Input from '../ui/Input'
import Select from '../ui/Select'
import Textarea from '../ui/Textarea'

export default function CalculatorSection() {
  const [formData, setFormData] = useState({
    type: '',
    area: '',
    equipment: [],
    material: 'steel',
    installation: true,
    delivery: true
  })

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  const calculateTotal = () => {
    let total = 0
    
    if (formData.type === 'open') total += 150000
    else if (formData.type === 'closed') total += 250000
    else if (formData.type === 'hybrid') total += 350000
    
    const materialMultiplier = formData.material === 'hpl' ? 1.8 : 1.0
    total *= materialMultiplier
    
    if (formData.area) {
      total += formData.area * 40000
    }
    
    if (formData.installation) total += 25000
    if (formData.delivery) total += 5000
    
    return Math.round(total)
  }

  const handleSubmit = () => {
    console.log('Form data:', formData)
    console.log('Estimated cost:', calculateTotal())
  }


import { useState } from 'react'
import Button from '../ui/Button'
import Input from '../ui/Input'
import Select from '../ui/Select'
import Textarea from '../ui/Textarea'

export default function CalculatorSection() {
  const [formData, setFormData] = useState({
    type: '',
    area: '',
    equipment: [],
    material: 'steel',
    installation: true,
    delivery: true
  })

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  const calculateTotal = () => {
    let total = 0
    
    if (formData.type === 'open') total += 150000
    else if (formData.type === 'closed') total += 250000
    else if (formData.type === 'hybrid') total += 350000
    
    const materialMultiplier = formData.material === 'hpl' ? 1.8 : 1.0
    total *= materialMultiplier
    
    if (formData.area) {
      total += formData.area * 40000
    }
    
    if (formData.installation) total += 25000
    if (formData.delivery) total += 5000
    
    return Math.round(total)
  }

  const handleSubmit = () => {
    console.log('Form data:', formData)
    console.log('Estimated cost:', calculateTotal())
  }



  return (
    <section id="calculator" className="py-20 bg-gradient-to-br from-primary via-red-700 to-secondary">
      <div className="max-w-7xl mx-auto px-4 md:px-6">
        <div className="text-center mb-12 text-white">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Калькулятор стоимости
          </h2>
          <p className="text-lg text-red-100 max-w-2xl mx-auto">
            Рассчитайте примерную стоимость вашей будущей гриль-кухни прямо сейчас
          </p>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 max-w-4xl mx-auto bg-white rounded-2xl shadow-2xl p-8 md:p-12">
            <div className="lg:col-span-2 space-y-6">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Тип гриль-кухни
                </label>
                <Select 
                  value={formData.type}
                  onChange={handleChange}
                  name="type"
                  options={[
                    { label: 'Открытая', value: 'open' },
                    { label: 'Закрытая', value: 'closed' },
                    { label: 'Комбинированная', value: 'hybrid' }
                  ]}
                />
              </div>



              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Материал корпуса
                </label>
                <Select 
                  value={formData.material}
                  onChange={handleChange}
                  name="material"
                  options={[
                    { label: 'Сталь порошковая', value: 'steel' },
                    { label: 'Композит HPL', value: 'hpl' }
                  ]}
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Площадь проекта (м²)
                </label>
                <Input 
                  type="number"
                  name="area"
                  value={formData.area || ''}
                  onChange={handleChange}
                  placeholder="Например: 5"
                />
              </div>



              <div className="space-y-3">
                <label className="flex items-start gap-3 cursor-pointer">
                  <input 
                    type="checkbox"
                    name="installation"
                    checked={formData.installation}
                    onChange={handleChange}
                    className="mt-1 w-4 h-4 text-primary rounded focus:ring-primary"
                  />
                  <span className="text-sm text-gray-700">Монтаж под ключ (+25 000 ₽)</span>
                </label>

                <label className="flex items-start gap-3 cursor-pointer">
                  <input 
                    type="checkbox"
                    name="delivery"
                    checked={formData.delivery}
                    onChange={handleChange}
                    className="mt-1 w-4 h-4 text-primary rounded focus:ring-primary"
                  />
                  <span className="text-sm text-gray-700">Доставка (+5 000 ₽)</span>
                </label>


            <div className="space-y-6">
              <div className="bg-gradient-to-br from-gray-50 to-white rounded-xl p-6 border border-gray-100">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Итого:</h3>
                
                {!formData.type && (
                  <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Оборудование
                    </label>
                    <Select 
                      value={formData.equipment[0] || ''}
                      onChange={handleChange}
                      name="equipment"
                      options={[
                        { label: 'Опции не выбраны', value: '' },
                        { label: 'Гриль-мангал', value: 'grill' },
                        { label: 'Шашлычница', value: 'shashlik' },
                        { label: 'Электрическая плита', value: 'electric_stove' },
                        { label: 'Холодильник', value: 'fridge' }
                      ]}
                    />
                  </div>
                )}


                <div className="space-y-2 text-sm">
                  <p className="text-gray-600">
                    <span className="font-semibold text-gray-900">Базовая стоимость:</span>{' '}
                    {formData.type ? (formData.type === 'open' ? 150 : formData.type === 'closed' ? 250 : 350) * 1000} ₽
                  </p>
                  
                  {formData.area && (
                    <p className="text-gray-600">
                      <span className="font-semibold text-gray-900">Площадь:</span>{' '}
                      {(formData.area * 40) * 1000} ₽
                    </p>
                  )}

                  {formData.installation && (
                    <p className="text-gray-600">
                      <span className="font-semibold text-gray-900">Монтаж:</span>{' '}
                      25 000 ₽
                    </p>
                  )}

                  {formData.delivery && (
                    <p className="text-gray-600">
                      <span className="font-semibold text-gray-900">Доставка:</span>{' '}
                      5 000 ₽
                    </p>
                  )}
                </div>

              </div>

                <div className="mt-4 pt-4 border-t border-gray-200">
                  <p className="text-xl font-bold text-primary">
                    {formData.type ? calculateTotal() : 0.toLocaleString()} ₽
                  </p>
                </div>

                <Button 
                  type="submit"
                  className="w-full mt-4 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-200 shadow-md hover:shadow-lg"
                >
                  Рассчитать стоимость
                </Button>


              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Дополнительные пожелания
                </label>
                <Textarea 
                  name="comments"
                  placeholder="Опишите ваши идеи, требования или особые пожелания..."
                  rows={3}
                />
              </div>
            </div>


                <p className="text-xs text-gray-500 mt-3 text-center">
                  *Это ориентировочная расчетная стоимость. Точную цену уточняйте у менеджера.
                </p>
              </div>
            </div>
          </div>
        </form>
      </div>
    </section>
  )
}

import { useState } from 'react'
import Button from '../ui/Button'
import Input from '../ui/Input'
import Select from '../ui/Select'
import Textarea from '../ui/Textarea'

export default function CalculatorSection() {
  const [formData, setFormData] = useState({
    type: '',
    area: '',
    equipment: [],
    material: 'steel',
    installation: true,
    delivery: true
  })

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  const calculateTotal = () => {
    let total = 0
    
    if (formData.type === 'open') total += 150000
    else if (formData.type === 'closed') total += 250000
    else if (formData.type === 'hybrid') total += 350000
    
    const materialMultiplier = formData.material === 'hpl' ? 1.8 : 1.0
    total *= materialMultiplier
    
    if (formData.area) {
      total += formData.area * 40000
    }
    
    if (formData.installation) total += 25000
    if (formData.delivery) total += 5000
    
    return Math.round(total)
  }

  const handleSubmit = () => {
    console.log('Form data:', formData)
    console.log('Estimated cost:', calculateTotal())
  }

import { useState } from 'react'
import Button from '../ui/Button'
import Input from '../ui/Input'
import Select from '../ui/Select'
import Textarea from '../ui/Textarea'

export default function CalculatorSection() {
  const [formData, setFormData] = useState({
    type: '',
    area: '',
    equipment: [],
    material: 'steel',
    installation: true,
    delivery: true
  })

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

import { useState } from 'react'
import Button from '../ui/Button'
import Input from '../ui/Input'
import Select from '../ui/Select'
import Textarea from '../ui/Textarea'

export default function CalculatorSection() {
  const [formData, setFormData] = useState({
    type: '',
    area: '',
    equipment: [],
    material: 'steel',
    installation: true,
    delivery: true
  })

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

import { useState } from 'react'
import Button from '../ui/Button'
import Input from '../ui/Input'
import Select from '../ui/Select'
import Textarea from '../ui/Textarea'

export default function CalculatorSection() {
  const [formData, setFormData] = useState({
    type: '',
    area: '',
    material: 'steel',
    installation: true,
    delivery: true
  })

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }



  return (
import { useState } from 'react'
import Button from '../ui/Button'
import Input from '../ui/Input'
import Select from '../ui/Select'
import Textarea from '../ui/Textarea'

export default function CalculatorSection() {
  const [formData, setFormData] = useState({
    type: '',
    area: '',
    equipment: [],
    material: 'steel',
    installation: true,
    delivery: true
  })

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  return (
    <section id="calculator" className="py-20 bg-gradient-to-br from-primary via-red-700 to-secondary">
      <div className="max-w-7xl mx-auto px-4 md:px-6">
        {/* Section Header */}
        <div className="text-center mb-12 text-white">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Калькулятор стоимости
          </h2>
          <p className="text-lg text-red-100 max-w-2xl mx-auto">
            Рассчитайте примерную стоимость вашей будущей гриль-кухни прямо сейчас
          </p>
        </div>

        {/* Calculator Form */}
        <form className="max-w-4xl mx-auto bg-white rounded-2xl shadow-2xl p-8 md:p-12" onSubmit={(e) => e.preventDefault()}>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Column 1 */}
            <div className="lg:col-span-2 space-y-6">
              {/* Type Selection */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Тип гриль-кухни
                </label>
                <Select 
                  value={formData.type}
                  onChange={handleChange}
                  name="type"
                  options={[
                    { label: 'Открытая', value: 'open' },
                    { label: 'Закрытая', value: 'closed' },
                    { label: 'Комбинированная', value: 'hybrid' }
                  ]}
                />
              </div>

              {/* Material Selection */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Материал корпуса
                </label>
                <Select 
                  value={formData.material}
                  onChange={handleChange}
                  name="material"
                  options={[
                    { label: 'Сталь порошковая', value: 'steel' },
                    { label: 'Композит HPL', value: 'hpl' }
                  ]}
                />
              </div>

              {/* Area Input */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Площадь проекта (м²)
                </label>
                <Input 
                  type="number"
                  name="area"
                  value={formData.area}
                  onChange={handleChange}
                  placeholder="Например: 5"
                />
              </div>

              {/* Additional Options */}
              <div className="space-y-3">
                <label className="flex items-start gap-3 cursor-pointer">
                  <input 
                    type="checkbox"
                    name="installation"
                    checked={formData.installation}
                    onChange={handleChange}
                    className="mt-1 w-4 h-4 text-primary rounded focus:ring-primary"
                  />
                  <span className="text-sm text-gray-700">Монтаж под ключ (+25 000 ₽)</span>
                </label>

                <label className="flex items-start gap-3 cursor-pointer">
                  <input 
                    type="checkbox"
                    name="delivery"
                    checked={formData.delivery}
                    onChange={handleChange}
                    className="mt-1 w-4 h-4 text-primary rounded focus:ring-primary"
                  />
                  <span className="text-sm text-gray-700">Доставка (+5 000 ₽)</span>
                </label>
              </div>

              {/* Additional Info */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Дополнительные пожелания
                </label>
                <Textarea 
                  name="comments"
                  placeholder="Опишите ваши идеи, требования или особые пожелания..."
                  rows={3}
                />
              </div>
            </div>

import { useState } from 'react'
import Button from '../ui/Button'
import Input from '../ui/Input'
import Select from '../ui/Select'
import Textarea from '../ui/Textarea'

export default function CalculatorSection() {
  const [formData, setFormData] = useState({
    type: '',
    area: '',
    equipment: [],
    material: 'steel',
    installation: true,
    delivery: true
  })

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  return (
import { useState } from 'react'
import Button from '../ui/Button'
import Input from '../ui/Input'
import Select from '../ui/Select'
import Textarea from '../ui/Textarea'

export default function CalculatorSection() {
  const [formData, setFormData] = useState({
    type: '',
    area: '',
    equipment: [],
    material: 'steel',
    installation: true,
    delivery: true
  })

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  return (
    <section id="calculator" className="py-20 bg-gradient-to-br from-primary via-red-700 to-secondary">
      <div className="max-w-7xl mx-auto px-4 md:px-6">
        {/* Section Header */}
        <div className="text-center mb-12 text-white">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Калькулятор стоимости
          </h2>
          <p className="text-lg text-red-100 max-w-2xl mx-auto">
            Рассчитайте примерную стоимость вашей будущей гриль-кухни прямо сейчас
          </p>
        </div>

        {/* Calculator Form */}
        <form className="max-w-4xl mx-auto bg-white rounded-2xl shadow-2xl p-8 md:p-12" onSubmit={(e) => e.preventDefault()}>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Column 1 */}
            <div className="lg:col-span-2 space-y-6">
              {/* Type Selection */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Тип гриль-кухни
                </label>
                <Select 
                  value={formData.type}
                  onChange={handleChange}
                  name="type"
                  options={[
                    { label: 'Открытая', value: 'open' },
                    { label: 'Закрытая', value: 'closed' },
                    { label: 'Комбинированная', value: 'hybrid' }
                  ]}
                />
              </div>

              {/* Material Selection */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Материал корпуса
                </label>
                <Select 
                  value={formData.material}
                  onChange={handleChange}
                  name="material"
                  options={[
                    { label: 'Сталь порошковая', value: 'steel' },
                    { label: 'Композит HPL', value: 'hpl' }
                  ]}
                />
              </div>

              {/* Area Input */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Площадь проекта (м²)
                </label>
                <Input 
                  type="number"
                  name="area"
                  value={formData.area}
                  onChange={handleChange}
                  placeholder="Например: 5"
                />
              </div>

              {/* Additional Options */}
              <div className="space-y-3">
                <label className="flex items-start gap-3 cursor-pointer">
                  <input 
                    type="checkbox"
                    name="installation"
                    checked={formData.installation}
                    onChange={handleChange}
                    className="mt-1 w-4 h-4 text-primary rounded focus:ring-primary"
                  />
                  <span className="text-sm text-gray-700">Монтаж под ключ (+25 000 ₽)</span>
                </label>

                <label className="flex items-start gap-3 cursor-pointer">
                  <input 
                    type="checkbox"
                    name="delivery"
                    checked={formData.delivery}
                    onChange={handleChange}
                    className="mt-1 w-4 h-4 text-primary rounded focus:ring-primary"
                  />
                  <span className="text-sm text-gray-700">Доставка (+5 000 ₽)</span>
                </label>
              </div>

              {/* Additional Info */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Дополнительные пожелания
                </label>
                <Textarea 
                  name="comments"
                  placeholder="Опишите ваши идеи, требования или особые пожелания..."
                  rows={3}
                />
              </div>
            </div>

      <div className="max-w-7xl mx-auto px-4 md:px-6">
import { useState } from 'react'
import Button from '../ui/Button'
import Input from '../ui/Input'
import Select from '../ui/Select'
import Textarea from '../ui/Textarea'

export default function CalculatorSection() {
  const [formData, setFormData] = useState({
    type: '',
    area: '',
    equipment: [],
    material: 'steel',
    installation: true,
    delivery: true
  })

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  return (
        {/* Section Header */}
        <div className="text-center mb-12 text-white">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Калькулятор стоимости
          </h2>
          <p className="text-lg text-red-100 max-w-2xl mx-auto">
            Рассчитайте примерную стоимость вашей будущей гриль-кухни прямо сейчас
          </p>
        </div>

        {/* Calculator Form */}
        <form className="max-w-4xl mx-auto bg-white rounded-2xl shadow-2xl p-8 md:p-12" onSubmit={(e) => e.preventDefault()}>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Column 1 */}
            <div className="lg:col-span-2 space-y-6">
              {/* Type Selection */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Тип гриль-кухни
                </label>
                <Select 
                  value={formData.type}
                  onChange={handleChange}
                  name="type"
                  options={[
                    { label: 'Открытая', value: 'open' },
                    { label: 'Закрытая', value: 'closed' },
                    { label: 'Комбинированная', value: 'hybrid' }
                  ]}
                />
              </div>

              {/* Material Selection */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Материал корпуса
                </label>
                <Select 
                  value={formData.material}
                  onChange={handleChange}
                  name="material"
                  options={[
                    { label: 'Сталь порошковая', value: 'steel' },
                    { label: 'Композит HPL', value: 'hpl' }
                  ]}
                />
              </div>

              {/* Area Input */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Площадь проекта (м²)
                </label>
                <Input 
                  type="number"
                  name="area"
                  value={formData.area}
                  onChange={handleChange}
                  placeholder="Например: 5"
                />
              </div>

              {/* Additional Options */}
              <div className="space-y-3">
                <label className="flex items-start gap-3 cursor-pointer">
                  <input 
                    type="checkbox"
                    name="installation"
                    checked={formData.installation}
                    onChange={handleChange}
                    className="mt-1 w-4 h-4 text-primary rounded focus:ring-primary"
                  />
                  <span className="text-sm text-gray-700">Монтаж под ключ (+25 000 ₽)</span>
                </label>

                <label className="flex items-start gap-3 cursor-pointer">
                  <input 
                    type="checkbox"
                    name="delivery"
                    checked={formData.delivery}
                    onChange={handleChange}
                    className="mt-1 w-4 h-4 text-primary rounded focus:ring-primary"
                  />
                  <span className="text-sm text-gray-700">Доставка (+5 000 ₽)</span>
                </label>
              </div>

              {/* Additional Info */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Дополнительные пожелания
                </label>
                <Textarea 
                  name="comments"
                  placeholder="Опишите ваши идеи, требования или особые пожелания..."
                  rows={3}
                />
              </div>
            </div>

    <section id="calculator" className="py-20 bg-gradient-to-br from-primary via-red-700 to-secondary">