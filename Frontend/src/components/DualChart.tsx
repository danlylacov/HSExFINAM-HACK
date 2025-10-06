import React, { useRef, useEffect, useState, useCallback } from 'react';
import { ChevronLeft, ChevronRight, ZoomIn, ZoomOut, RotateCcw } from 'lucide-react';
import type { ForecastSettings } from '../types';

interface CandleData {
  time: number;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

interface DualChartProps {
  forecastSettings: ForecastSettings;
}

const DualChart: React.FC<DualChartProps> = ({ 
  forecastSettings
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [historicalCandles, setHistoricalCandles] = useState<CandleData[]>([]);
  const [forecastCandles, setForecastCandles] = useState<CandleData[]>([]);
  const [zoom, setZoom] = useState(1);
  const [offset, setOffset] = useState(0);

  // Генерация моковых данных свечей (только дневные)
  const generateCandleData = useCallback((count: number, startTime?: number): CandleData[] => {
    const data: CandleData[] = [];
    const baseTime = startTime || Date.now() - count * 24 * 60 * 60 * 1000; // день назад
    let currentPrice = 100 + Math.random() * 20;

    for (let i = 0; i < count; i++) {
      const time = baseTime + i * 24 * 60 * 60 * 1000; // каждый день
      const volatility = 0.02;
      const change = (Math.random() - 0.5) * volatility;
      
      const open = currentPrice;
      const close = open * (1 + change);
      const high = Math.max(open, close) * (1 + Math.random() * 0.01);
      const low = Math.min(open, close) * (1 - Math.random() * 0.01);
      const volume = Math.floor(Math.random() * 1000000) + 100000;

      data.push({
        time,
        open: Number(open.toFixed(2)),
        high: Number(high.toFixed(2)),
        low: Number(low.toFixed(2)),
        close: Number(close.toFixed(2)),
        volume,
      });

      currentPrice = close;
    }

    return data;
  }, []);

  // Генерация прогнозных данных (дневные свечи)
  const generateForecastData = useCallback((historicalData: CandleData[], days: number): CandleData[] => {
    if (historicalData.length === 0) return [];
    
    const lastCandle = historicalData[historicalData.length - 1];
    const forecastData: CandleData[] = [];
    let currentPrice = lastCandle.close;
    
    // Используем тренд последних данных для прогноза
    const recentTrend = historicalData.slice(-10).reduce((sum, candle, index, arr) => {
      if (index === 0) return 0;
      return sum + (candle.close - arr[index - 1].close) / arr[index - 1].close;
    }, 0) / 9;

    for (let i = 0; i < days; i++) {
      const time = lastCandle.time + (i + 1) * 24 * 60 * 60 * 1000; // следующий день
      const trendFactor = recentTrend * 0.7; // Смягчаем тренд
      const volatility = 0.015; // Меньшая волатильность для прогноза
      const change = trendFactor + (Math.random() - 0.5) * volatility;
      
      const open = currentPrice;
      const close = open * (1 + change);
      const high = Math.max(open, close) * (1 + Math.random() * 0.005);
      const low = Math.min(open, close) * (1 - Math.random() * 0.005);
      const volume = Math.floor(Math.random() * 800000) + 80000; // Меньший объем

      forecastData.push({
        time,
        open: Number(open.toFixed(2)),
        high: Number(high.toFixed(2)),
        low: Number(low.toFixed(2)),
        close: Number(close.toFixed(2)),
        volume,
      });

      currentPrice = close;
    }

    return forecastData;
  }, []);

  // Загрузка данных
  useEffect(() => {
    const loadData = async () => {
      const historicalData = generateCandleData(100);
      setHistoricalCandles(historicalData);
      
      // Автоматически генерируем прогноз
      const forecastData = generateForecastData(historicalData, forecastSettings.forecastDays);
      setForecastCandles(forecastData);
    };
    loadData();
  }, [generateCandleData, generateForecastData, forecastSettings.forecastDays]);

  // Отрисовка графика
  const drawChart = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas || historicalCandles.length === 0) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * window.devicePixelRatio;
    canvas.height = rect.height * window.devicePixelRatio;
    ctx.scale(window.devicePixelRatio, window.devicePixelRatio);

    const width = rect.width;
    const height = rect.height;
    const padding = { top: 20, right: 60, bottom: 40, left: 60 };
    const chartWidth = width - padding.left - padding.right;
    const chartHeight = height - padding.top - padding.bottom;

    // Очистка canvas
    ctx.fillStyle = '#000000';
    ctx.fillRect(0, 0, width, height);

    // Объединяем исторические данные и прогноз
    const allData = [...historicalCandles, ...forecastCandles];
    const historicalCount = historicalCandles.length;
    
    // Данные для отображения
    const visibleCandles = Math.floor(chartWidth / (8 * zoom));
    const startIndex = Math.max(0, allData.length - visibleCandles - offset);
    const endIndex = Math.min(allData.length, startIndex + visibleCandles);
    const visibleData = allData.slice(startIndex, endIndex);

    if (visibleData.length === 0) return;

    // Находим min/max цены
    const prices = visibleData.flatMap(c => [c.high, c.low]);
    const minPrice = Math.min(...prices);
    const maxPrice = Math.max(...prices);
    const priceRange = maxPrice - minPrice;
    const pricePadding = priceRange * 0.1;

    // Функция для преобразования цены в Y координату
    const priceToY = (price: number) => {
      return padding.top + chartHeight - ((price - minPrice + pricePadding) / (priceRange + pricePadding * 2)) * chartHeight;
    };

    // Функция для преобразования индекса в X координату
    const indexToX = (index: number) => {
      return padding.left + (index / (visibleData.length - 1)) * chartWidth;
    };

    // Отрисовка сетки
    ctx.strokeStyle = '#2A2A2A';
    ctx.lineWidth = 1;
    
    // Горизонтальные линии
    for (let i = 0; i <= 5; i++) {
      const y = padding.top + (chartHeight / 5) * i;
      ctx.beginPath();
      ctx.moveTo(padding.left, y);
      ctx.lineTo(padding.left + chartWidth, y);
      ctx.stroke();
    }

    // Вертикальные линии
    for (let i = 0; i <= 10; i++) {
      const x = padding.left + (chartWidth / 10) * i;
      ctx.beginPath();
      ctx.moveTo(x, padding.top);
      ctx.lineTo(x, padding.top + chartHeight);
      ctx.stroke();
    }

    // Отрисовка свечей
    visibleData.forEach((candle, index) => {
      const x = indexToX(index);
      const candleWidth = Math.max(2, chartWidth / visibleData.length * 0.8);
      const isGreen = candle.close >= candle.open;
      
      // Определяем, является ли свеча прогнозной
      const isForecast = startIndex + index >= historicalCount;
      
      // Цвета для исторических и прогнозных данных
      const colors = isForecast 
        ? {
            green: '#8B5CF6', // Фиолетовый для прогноза роста
            red: '#F59E0B',   // Оранжевый для прогноза падения
            wick: isGreen ? '#8B5CF6' : '#F59E0B'
          }
        : {
            green: '#22C55E',
            red: '#DC2626',
            wick: isGreen ? '#22C55E' : '#DC2626'
          };

      // Тень свечи
      ctx.strokeStyle = colors.wick;
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(x, priceToY(candle.high));
      ctx.lineTo(x, priceToY(candle.low));
      ctx.stroke();

      // Тело свечи
      const bodyHeight = Math.abs(priceToY(candle.close) - priceToY(candle.open));
      const bodyY = Math.min(priceToY(candle.open), priceToY(candle.close));
      
      ctx.fillStyle = isGreen ? colors.green : colors.red;
      ctx.fillRect(x - candleWidth/2, bodyY, candleWidth, Math.max(1, bodyHeight));

      // Граница тела свечи
      ctx.strokeStyle = isGreen ? colors.green : colors.red;
      ctx.lineWidth = 1;
      ctx.strokeRect(x - candleWidth/2, bodyY, candleWidth, Math.max(1, bodyHeight));
    });

    // Отрисовка подписей цен
    ctx.fillStyle = '#9CA3AF';
    ctx.font = '12px Arial';
    ctx.textAlign = 'right';
    
    for (let i = 0; i <= 5; i++) {
      const price = minPrice + pricePadding + (priceRange + pricePadding * 2) * (1 - i / 5);
      const y = padding.top + (chartHeight / 5) * i;
      ctx.fillText(price.toFixed(2), padding.left - 10, y + 4);
    }

    // Отрисовка временных меток
    ctx.textAlign = 'center';
    const timeStep = Math.max(1, Math.floor(visibleData.length / 5));
    for (let i = 0; i < visibleData.length; i += timeStep) {
      const candle = visibleData[i];
      const x = indexToX(i);
      const date = new Date(candle.time);
      ctx.fillText(
        date.toLocaleDateString('ru-RU', { day: '2-digit', month: '2-digit' }),
        x,
        height - padding.bottom + 20
      );
    }

    // Линия разделения между историческими данными и прогнозом
    if (forecastCandles.length > 0) {
      const forecastStartIndex = historicalCount - startIndex;
      if (forecastStartIndex >= 0 && forecastStartIndex < visibleData.length) {
        const x = indexToX(forecastStartIndex);
        ctx.strokeStyle = '#F59E0B';
        ctx.lineWidth = 2;
        ctx.setLineDash([5, 5]);
        ctx.beginPath();
        ctx.moveTo(x, padding.top);
        ctx.lineTo(x, padding.top + chartHeight);
        ctx.stroke();
        ctx.setLineDash([]);
        
        // Подпись "Прогноз"
        ctx.fillStyle = '#F59E0B';
        ctx.font = 'bold 12px Arial';
        ctx.textAlign = 'left';
        ctx.fillText('Прогноз', x + 5, padding.top + 15);
      }
    }
  }, [historicalCandles, forecastCandles, zoom, offset]);

  // Отрисовка графика
  useEffect(() => {
    drawChart();
  }, [drawChart]);


  const resetZoom = () => {
    setZoom(1);
    setOffset(0);
  };

  const zoomIn = () => {
    setZoom(prev => Math.min(prev * 1.2, 5));
  };

  const zoomOut = () => {
    setZoom(prev => Math.max(prev / 1.2, 0.5));
  };

  const moveLeft = () => {
    setOffset(prev => Math.min(prev + 10, 100));
  };

  const moveRight = () => {
    setOffset(prev => Math.max(prev - 10, 0));
  };

  return (
    <div className="space-y-6">
      {/* Controls */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center space-x-4">
          <span className="text-gray-400 text-sm">Дневные свечи</span>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={moveLeft}
            className="p-2 text-gray-400 hover:text-white transition-colors"
            title="Влево"
          >
            <ChevronLeft className="w-4 h-4" />
          </button>
          <button
            onClick={zoomOut}
            className="p-2 text-gray-400 hover:text-white transition-colors"
            title="Уменьшить"
          >
            <ZoomOut className="w-4 h-4" />
          </button>
          <button
            onClick={resetZoom}
            className="p-2 text-gray-400 hover:text-white transition-colors"
            title="Сброс"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
          <button
            onClick={zoomIn}
            className="p-2 text-gray-400 hover:text-white transition-colors"
            title="Увеличить"
          >
            <ZoomIn className="w-4 h-4" />
          </button>
          <button
            onClick={moveRight}
            className="p-2 text-gray-400 hover:text-white transition-colors"
            title="Вправо"
          >
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Combined Chart */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-white">График с прогнозом</h3>
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-green-500 rounded-full"></div>
              <span className="text-sm text-gray-400">Исторические данные</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-purple-500 rounded-full"></div>
              <span className="text-sm text-gray-400">Прогноз роста</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-orange-500 rounded-full"></div>
              <span className="text-sm text-gray-400">Прогноз падения</span>
            </div>
          </div>
        </div>
        <div className="relative">
          <canvas
            ref={canvasRef}
            className="w-full h-96 bg-black rounded-lg"
            style={{ cursor: 'crosshair' }}
          />
        </div>
      </div>


    </div>
  );
};

export default DualChart;
