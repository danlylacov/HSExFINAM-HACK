import React, { useState } from 'react';
import type { ForecastSettings } from '../types';

interface StockChartProps {
  symbol: string;
  forecastSettings: ForecastSettings;
  onForecastComplete?: (forecastData: any[]) => void;
}

const StockChart: React.FC<StockChartProps> = ({ 
  symbol, 
  forecastSettings, 
  onForecastComplete 
}) => {
  const [isLoading, setIsLoading] = useState(false);
  const [hasForecast, setHasForecast] = useState(false);

  const handleForecast = async () => {
    setIsLoading(true);

    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Generate mock forecast data
    const forecastData = Array.from({ length: forecastSettings.forecastDays }, (_, i) => ({
      time: new Date(Date.now() + (i + 1) * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
      value: 100 + Math.random() * 20 - 10 + i * 0.5,
    }));

    setIsLoading(false);
    setHasForecast(true);
    onForecastComplete?.(forecastData);
  };

  return (
    <div className="card">
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-xl font-semibold text-white">
          График {symbol}
        </h3>
        <button
          onClick={handleForecast}
          disabled={isLoading}
          className="btn-primary flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? (
            <>
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
              <span>Прогнозирование...</span>
            </>
          ) : (
            <>
              <span>Спрогнозировать</span>
            </>
          )}
        </button>
      </div>
      
      {/* Mock Chart */}
      <div className="w-full h-96 bg-gray-800 rounded-lg flex items-center justify-center relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-gray-800 to-gray-900"></div>
        
        {/* Mock Chart Lines */}
        <div className="relative w-full h-full">
          {/* Historical data line */}
          <svg className="absolute inset-0 w-full h-full" viewBox="0 0 400 300">
            <polyline
              points="20,250 60,200 100,180 140,160 180,140 220,120 260,100 300,80 340,60 380,40"
              fill="none"
              stroke="#26a69a"
              strokeWidth="2"
            />
            
            {/* Forecast line */}
            {hasForecast && (
              <polyline
                points="380,40 400,30 420,25 440,20 460,15 480,10 500,5"
                fill="none"
                stroke="#FF6F20"
                strokeWidth="2"
                strokeDasharray="5,5"
              />
            )}
            
            {/* Grid lines */}
            {Array.from({ length: 6 }, (_, i) => (
              <line
                key={i}
                x1="20"
                y1={50 + i * 50}
                x2="500"
                y2={50 + i * 50}
                stroke="#2A2A2A"
                strokeWidth="1"
              />
            ))}
            
            {Array.from({ length: 10 }, (_, i) => (
              <line
                key={i}
                x1={20 + i * 50}
                y1="20"
                x2={20 + i * 50}
                y2="280"
                stroke="#2A2A2A"
                strokeWidth="1"
              />
            ))}
          </svg>
          
          {/* Chart labels */}
          <div className="absolute bottom-4 left-4 text-xs text-gray-400">
            Исторические данные
          </div>
          {hasForecast && (
            <div className="absolute bottom-4 right-4 text-xs text-primary-orange">
              Прогноз
            </div>
          )}
        </div>
        
        {/* Loading overlay */}
        {isLoading && (
          <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center">
            <div className="text-center">
              <div className="w-8 h-8 border-2 border-primary-orange border-t-transparent rounded-full animate-spin mx-auto mb-2"></div>
              <p className="text-white text-sm">Генерация прогноза...</p>
            </div>
          </div>
        )}
      </div>
      
      <div className="mt-4 text-sm text-gray-400">
        <p>
          Используется {forecastSettings.trainingDays} дней данных для обучения модели {forecastSettings.model.toUpperCase()}
        </p>
        {hasForecast && (
          <p className="text-primary-orange mt-2">
            ✓ Прогноз на {forecastSettings.forecastDays} дней готов
          </p>
        )}
      </div>
    </div>
  );
};

export default StockChart;
