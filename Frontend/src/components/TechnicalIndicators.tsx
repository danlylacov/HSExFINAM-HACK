import React, { useState } from 'react';
import { TrendingUp, TrendingDown, Activity, BarChart3 } from 'lucide-react';

interface TechnicalIndicatorsProps {
  symbol: string;
}

const TechnicalIndicators: React.FC<TechnicalIndicatorsProps> = ({ symbol: _symbol }) => {
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

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-white flex items-center space-x-2">
          <BarChart3 className="w-5 h-5" />
          <span>Технический анализ</span>
        </h3>
        
        <div className="flex space-x-1">
          <button
            onClick={() => setActiveTab('indicators')}
            className={`px-3 py-1 rounded text-sm transition-colors ${
              activeTab === 'indicators'
                ? 'bg-orange-500 text-white'
                : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
            }`}
          >
            Индикаторы
          </button>
          <button
            onClick={() => setActiveTab('patterns')}
            className={`px-3 py-1 rounded text-sm transition-colors ${
              activeTab === 'patterns'
                ? 'bg-orange-500 text-white'
                : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
            }`}
          >
            Паттерны
          </button>
        </div>
      </div>

      {activeTab === 'indicators' && (
        <div className="space-y-4">
          {indicators.map((indicator, index) => (
            <div key={index} className="flex items-center justify-between p-3 bg-gray-800 rounded-lg">
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
        <div className="space-y-4">
          {patterns.map((pattern, index) => (
            <div key={index} className="flex items-center justify-between p-3 bg-gray-800 rounded-lg">
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
      <div className="mt-6 p-4 bg-gradient-to-r from-orange-500/10 to-purple-600/10 rounded-lg border border-orange-500/20">
        <div className="flex items-center justify-between">
          <div>
            <h4 className="text-white font-semibold mb-1">Общий сигнал</h4>
            <p className="text-gray-400 text-sm">На основе технического анализа</p>
          </div>
          <div className="text-right">
            <div className="flex items-center space-x-2 text-green-400">
              <TrendingUp className="w-5 h-5" />
              <span className="font-semibold">Покупка</span>
            </div>
            <div className="text-xs text-gray-500 mt-1">Сила: 78%</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TechnicalIndicators;
