import React, { useState } from 'react';
import { X, TrendingUp, TrendingDown, Activity, BarChart3 } from 'lucide-react';

interface TechnicalIndicatorsModalProps {
  isOpen: boolean;
  onClose: () => void;
  symbol: string;
}

const TechnicalIndicatorsModal: React.FC<TechnicalIndicatorsModalProps> = ({ 
  isOpen, 
  onClose, 
  symbol: _symbol 
}) => {
  const [activeTab, setActiveTab] = useState<'indicators' | 'patterns'>('indicators');

  // Моковые данные для технических индикаторов
  const indicators = [
    {
      name: 'RSI (14)',
      value: 65.4,
      signal: 'neutral',
      description: 'Индекс относительной силы'
    },
    {
      name: 'MACD',
      value: 2.1,
      signal: 'bullish',
      description: 'Схождение-расхождение скользящих средних'
    },
    {
      name: 'SMA (20)',
      value: 175.2,
      signal: 'bullish',
      description: 'Простая скользящая средняя за 20 периодов'
    },
    {
      name: 'EMA (50)',
      value: 172.8,
      signal: 'bullish',
      description: 'Экспоненциальная скользящая средняя за 50 периодов'
    },
    {
      name: 'Bollinger Bands',
      value: 'Верхняя полоса',
      signal: 'neutral',
      description: 'Полосы Боллинджера'
    },
    {
      name: 'Volume',
      value: 'Высокий',
      signal: 'bullish',
      description: 'Объем торгов'
    }
  ];

  const patterns = [
    {
      name: 'Hammer',
      signal: 'bullish',
      confidence: 85,
      description: 'Молот - разворотный паттерн'
    },
    {
      name: 'Doji',
      signal: 'neutral',
      confidence: 70,
      description: 'Доджи - неопределенность'
    },
    {
      name: 'Engulfing',
      signal: 'bullish',
      confidence: 90,
      description: 'Поглощение - сильный сигнал'
    },
    {
      name: 'Triangle',
      signal: 'neutral',
      confidence: 75,
      description: 'Треугольник - консолидация'
    }
  ];

  const getSignalColor = (signal: string) => {
    switch (signal) {
      case 'bullish':
        return 'text-green-400';
      case 'bearish':
        return 'text-red-400';
      default:
        return 'text-yellow-400';
    }
  };

  const getSignalIcon = (signal: string) => {
    switch (signal) {
      case 'bullish':
        return <TrendingUp className="w-4 h-4" />;
      case 'bearish':
        return <TrendingDown className="w-4 h-4" />;
      default:
        return <Activity className="w-4 h-4" />;
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-900 rounded-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          {/* Header */}
          <div className="flex justify-between items-center mb-6">
            <div className="flex items-center space-x-2">
              <BarChart3 className="w-6 h-6 text-orange-500" />
              <h2 className="text-2xl font-bold text-white">Технический анализ</h2>
            </div>
            <button
              onClick={onClose}
              className="p-2 text-gray-400 hover:text-white transition-colors"
            >
              <X className="w-6 h-6" />
            </button>
          </div>

          {/* Tabs */}
          <div className="flex space-x-1 mb-6">
            <button
              onClick={() => setActiveTab('indicators')}
              className={`px-4 py-2 rounded-lg transition-colors ${
                activeTab === 'indicators'
                  ? 'bg-orange-500 text-white'
                  : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
              }`}
            >
              Индикаторы
            </button>
            <button
              onClick={() => setActiveTab('patterns')}
              className={`px-4 py-2 rounded-lg transition-colors ${
                activeTab === 'patterns'
                  ? 'bg-orange-500 text-white'
                  : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
              }`}
            >
              Паттерны
            </button>
          </div>

          {/* Content */}
          {activeTab === 'indicators' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
              {indicators.map((indicator, index) => (
                <div key={index} className="flex items-center justify-between p-4 bg-gray-800 rounded-lg">
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-1">
                      <span className="text-white font-medium">{indicator.name}</span>
                      <div className={`flex items-center space-x-1 ${getSignalColor(indicator.signal)}`}>
                        {getSignalIcon(indicator.signal)}
                      </div>
                    </div>
                    <p className="text-gray-400 text-sm">{indicator.description}</p>
                  </div>
                  <div className="text-right">
                    <div className={`font-semibold ${getSignalColor(indicator.signal)}`}>
                      {typeof indicator.value === 'number' ? indicator.value.toFixed(2) : indicator.value}
                    </div>
                    <div className="text-xs text-gray-500 capitalize">
                      {indicator.signal === 'bullish' ? 'Бычий' : 
                       indicator.signal === 'bearish' ? 'Медвежий' : 'Нейтральный'}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'patterns' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
              {patterns.map((pattern, index) => (
                <div key={index} className="flex items-center justify-between p-4 bg-gray-800 rounded-lg">
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-1">
                      <span className="text-white font-medium">{pattern.name}</span>
                      <div className={`flex items-center space-x-1 ${getSignalColor(pattern.signal)}`}>
                        {getSignalIcon(pattern.signal)}
                      </div>
                    </div>
                    <p className="text-gray-400 text-sm">{pattern.description}</p>
                  </div>
                  <div className="text-right">
                    <div className="text-white font-semibold">
                      {pattern.confidence}%
                    </div>
                    <div className="text-xs text-gray-500">Уверенность</div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Общий сигнал */}
          <div className="p-6 bg-gradient-to-r from-orange-500/10 to-purple-600/10 rounded-lg border border-orange-500/20">
            <div className="flex items-center justify-between">
              <div>
                <h4 className="text-white font-semibold mb-1">Общий сигнал</h4>
                <p className="text-gray-400 text-sm">На основе технического анализа</p>
              </div>
              <div className="text-right">
                <div className="flex items-center space-x-2 text-green-400">
                  <TrendingUp className="w-6 h-6" />
                  <span className="font-semibold text-lg">Покупка</span>
                </div>
                <div className="text-sm text-gray-500 mt-1">Сила: 78%</div>
              </div>
            </div>
          </div>

          {/* Actions */}
          <div className="flex justify-end space-x-4 mt-6 pt-6 border-t border-gray-800">
            <button
              onClick={onClose}
              className="px-6 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-700 transition-colors"
            >
              Закрыть
            </button>
            <button className="btn-primary">
              Применить к графику
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TechnicalIndicatorsModal;
