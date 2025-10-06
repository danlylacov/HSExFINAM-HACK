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

interface TradingChartProps {
  symbol: string;
  forecastSettings: ForecastSettings;
  onForecastComplete?: (forecastData: any[]) => void;
  onForecastRequest?: () => void;
}

const TradingChart: React.FC<TradingChartProps> = ({ 
  symbol, 
  forecastSettings, 
  onForecastComplete,
  onForecastRequest
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [candles, setCandles] = useState<CandleData[]>([]);
  const [forecastCandles, setForecastCandles] = useState<CandleData[]>([]);
  const [timeframe, setTimeframe] = useState<'1m' | '5m' | '15m' | '1h' | '4h' | '1d'>('1h');
  const [zoom, setZoom] = useState(1);
  const [offset, setOffset] = useState(0);
  const [hoveredCandle, setHoveredCandle] = useState<CandleData | null>(null);

  // Генерация моковых данных свечей
  const generateCandleData = useCallback((count: number, startTime?: number): CandleData[] => {
    const data: CandleData[] = [];
    const baseTime = startTime || Date.now() - count * 60 * 60 * 1000; // час назад
    let currentPrice = 100 + Math.random() * 20;

    for (let i = 0; i < count; i++) {
      const time = baseTime + i * 60 * 60 * 1000; // каждый час
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

  // Загрузка данных
  useEffect(() => {
    const loadData = async () => {
      const historicalData = generateCandleData(100);
      setCandles(historicalData);
    };
    loadData();
  }, [generateCandleData, timeframe]);

  // Отрисовка графика
  const drawChart = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas || candles.length === 0) return;

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

    // Данные для отображения
    const allData = [...candles, ...forecastCandles];
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
      const openY = priceToY(candle.open);
      const closeY = priceToY(candle.close);
      const highY = priceToY(candle.high);
      const lowY = priceToY(candle.low);

      const isGreen = candle.close >= candle.open;
      
      // Определяем, является ли свеча прогнозной
      const isForecast = index + startIndex >= candles.length;
      
      // Цвета для исторических и прогнозных данных
      const color = isForecast 
        ? (isGreen ? '#FF6F20' : '#FF8F00') // Оранжевые цвета для прогноза
        : (isGreen ? '#26a69a' : '#ef5350'); // Зеленые/красные для истории

      // Тень (wick)
      ctx.strokeStyle = color;
      ctx.lineWidth = isForecast ? 2 : 1; // Более толстая линия для прогноза
      ctx.setLineDash(isForecast ? [5, 5] : []); // Пунктирная линия для прогноза
      ctx.beginPath();
      ctx.moveTo(x, highY);
      ctx.lineTo(x, lowY);
      ctx.stroke();
      ctx.setLineDash([]); // Сброс пунктира

      // Тело свечи
      const bodyTop = Math.min(openY, closeY);
      const bodyHeight = Math.abs(closeY - openY);
      
      if (bodyHeight > 0) {
        ctx.fillStyle = color;
        ctx.globalAlpha = isForecast ? 0.7 : 1.0; // Полупрозрачность для прогноза
        ctx.fillRect(x - candleWidth/2, bodyTop, candleWidth, bodyHeight);
        ctx.globalAlpha = 1.0; // Сброс прозрачности
      } else {
        // Doji - горизонтальная линия
        ctx.strokeStyle = color;
        ctx.lineWidth = isForecast ? 2 : 1;
        ctx.setLineDash(isForecast ? [5, 5] : []);
        ctx.beginPath();
        ctx.moveTo(x - candleWidth/2, openY);
        ctx.lineTo(x + candleWidth/2, openY);
        ctx.stroke();
        ctx.setLineDash([]);
      }

      // Граница свечи
      ctx.strokeStyle = color;
      ctx.lineWidth = 1;
      ctx.strokeRect(x - candleWidth/2, bodyTop, candleWidth, bodyHeight);
    });

    // Отрисовка прогноза
    if (forecastCandles.length > 0) {
      const forecastStartIndex = visibleData.length;
      forecastCandles.forEach((candle, index) => {
        const x = indexToX(forecastStartIndex + index);
        const candleWidth = Math.max(2, chartWidth / visibleData.length * 0.8);
        const openY = priceToY(candle.open);
        const closeY = priceToY(candle.close);
        const highY = priceToY(candle.high);
        const lowY = priceToY(candle.low);

        const isGreen = candle.close >= candle.open;
        const color = isGreen ? '#FF6F20' : '#693EFE';

        // Тень (wick) - пунктирная
        ctx.strokeStyle = color;
        ctx.lineWidth = 1;
        ctx.setLineDash([5, 5]);
        ctx.beginPath();
        ctx.moveTo(x, highY);
        ctx.lineTo(x, lowY);
        ctx.stroke();

        // Тело свечи
        const bodyTop = Math.min(openY, closeY);
        const bodyHeight = Math.abs(closeY - openY);
        
        if (bodyHeight > 0) {
          ctx.fillStyle = color + '80'; // полупрозрачность
          ctx.fillRect(x - candleWidth/2, bodyTop, candleWidth, bodyHeight);
        }

        ctx.setLineDash([]);
      });
    }

    // Отрисовка подписей цен
    ctx.fillStyle = '#FFFFFF';
    ctx.font = '12px Inter';
    ctx.textAlign = 'right';
    
    for (let i = 0; i <= 5; i++) {
      const price = maxPrice - (priceRange / 5) * i;
      const y = padding.top + (chartHeight / 5) * i;
      ctx.fillText(price.toFixed(2), padding.left - 10, y + 4);
    }

    // Отрисовка времени
    ctx.textAlign = 'center';
    ctx.fillStyle = '#A0A0A0';
    ctx.font = '10px Inter';
    
    const timeStep = Math.max(1, Math.floor(visibleData.length / 8));
    for (let i = 0; i < visibleData.length; i += timeStep) {
      const x = indexToX(i);
      const time = new Date(visibleData[i].time);
      const timeStr = time.toLocaleTimeString('ru-RU', { 
        hour: '2-digit', 
        minute: '2-digit' 
      });
      ctx.fillText(timeStr, x, height - 10);
    }

    // Отрисовка информации о свече при наведении
    if (hoveredCandle) {
      const index = visibleData.findIndex(c => c.time === hoveredCandle.time);
      if (index !== -1) {
        const x = indexToX(index);
        
        // Вертикальная линия
        ctx.strokeStyle = '#FF6F20';
        ctx.lineWidth = 1;
        ctx.setLineDash([5, 5]);
        ctx.beginPath();
        ctx.moveTo(x, padding.top);
        ctx.lineTo(x, padding.top + chartHeight);
        ctx.stroke();
        ctx.setLineDash([]);

        // Информационная панель
        const infoWidth = 200;
        const infoHeight = 120;
        const infoX = Math.min(x + 10, width - infoWidth - 10);
        const infoY = padding.top + 10;

        ctx.fillStyle = 'rgba(0, 0, 0, 0.9)';
        ctx.fillRect(infoX, infoY, infoWidth, infoHeight);

        ctx.strokeStyle = '#FF6F20';
        ctx.lineWidth = 1;
        ctx.strokeRect(infoX, infoY, infoWidth, infoHeight);

        ctx.fillStyle = '#FFFFFF';
        ctx.font = 'bold 12px Inter';
        ctx.textAlign = 'left';
        ctx.fillText(`${symbol}`, infoX + 10, infoY + 20);

        ctx.font = '10px Inter';
        ctx.fillText(`O: ${hoveredCandle.open.toFixed(2)}`, infoX + 10, infoY + 40);
        ctx.fillText(`H: ${hoveredCandle.high.toFixed(2)}`, infoX + 10, infoY + 55);
        ctx.fillText(`L: ${hoveredCandle.low.toFixed(2)}`, infoX + 10, infoY + 70);
        ctx.fillText(`C: ${hoveredCandle.close.toFixed(2)}`, infoX + 10, infoY + 85);
        ctx.fillText(`V: ${hoveredCandle.volume.toLocaleString()}`, infoX + 10, infoY + 100);

        const change = hoveredCandle.close - hoveredCandle.open;
        const changePercent = (change / hoveredCandle.open) * 100;
        ctx.fillStyle = change >= 0 ? '#26a69a' : '#ef5350';
        ctx.fillText(`${change >= 0 ? '+' : ''}${changePercent.toFixed(2)}%`, infoX + 10, infoY + 115);
      }
    }
  }, [candles, forecastCandles, zoom, offset, hoveredCandle, symbol]);

  // Обработка мыши
  const handleMouseMove = useCallback((e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;

    const padding = { left: 60, right: 60 };
    const chartWidth = rect.width - padding.left - padding.right;
    const visibleCandles = Math.floor(chartWidth / (8 * zoom));
    const startIndex = Math.max(0, candles.length - visibleCandles - offset);
    const endIndex = Math.min(candles.length, startIndex + visibleCandles);
    const visibleData = candles.slice(startIndex, endIndex);

    if (visibleData.length === 0) return;

    const candleIndex = Math.floor(((x - padding.left) / chartWidth) * visibleData.length);
    if (candleIndex >= 0 && candleIndex < visibleData.length) {
      setHoveredCandle(visibleData[candleIndex]);
    } else {
      setHoveredCandle(null);
    }
  }, [candles, zoom, offset]);

  const handleMouseDown = useCallback((e: React.MouseEvent<HTMLCanvasElement>) => {
    // Простая навигация по клику
    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const padding = { left: 60, right: 60 };
    const chartWidth = rect.width - padding.left - padding.right;
    
    if (x < padding.left) {
      setOffset(prev => Math.max(0, prev - 5));
    } else if (x > padding.left + chartWidth) {
      setOffset(prev => prev + 5);
    }
  }, []);

  const handleMouseUp = useCallback(() => {
    // Пустая функция для совместимости
  }, []);

  // Обработка колесика мыши для зума
  const handleWheel = useCallback((e: React.WheelEvent<HTMLCanvasElement>) => {
    e.preventDefault();
    const delta = e.deltaY > 0 ? 0.1 : -0.1;
    setZoom(prev => Math.max(0.5, Math.min(3, prev + delta)));
  }, []);

  // Прогнозирование
  const handleForecast = async () => {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Generate forecast data starting from the last candle
    const lastCandle = candles[candles.length - 1];
    const forecastData: CandleData[] = [];
    
    for (let i = 1; i <= forecastSettings.forecastDays; i++) {
      const basePrice = lastCandle.close;
      const volatility = 0.02; // 2% volatility
      const trend = (Math.random() - 0.5) * 0.01; // Small trend
      
      const open = basePrice * (1 + trend * i + (Math.random() - 0.5) * volatility);
      const close = open * (1 + (Math.random() - 0.5) * volatility);
      const high = Math.max(open, close) * (1 + Math.random() * volatility * 0.5);
      const low = Math.min(open, close) * (1 - Math.random() * volatility * 0.5);
      
      const time = new Date(lastCandle.time);
      time.setDate(time.getDate() + i);
      
      forecastData.push({
        time: time.getTime(),
        open: Math.max(0, open),
        high: Math.max(0, high),
        low: Math.max(0, low),
        close: Math.max(0, close),
        volume: Math.floor(Math.random() * 1000000) + 500000
      });
    }
    
    setForecastCandles(forecastData);
    
    // Перерисовываем график с прогнозом
    setTimeout(() => {
      drawChart();
    }, 100);
    
    onForecastComplete?.(forecastData);
  };

  // Отрисовка при изменении данных
  useEffect(() => {
    drawChart();
  }, [drawChart]);

  // Экспортируем функцию прогнозирования для внешнего использования
  useEffect(() => {
    if (onForecastRequest) {
      // Создаем глобальную функцию для доступа извне
      (window as any).triggerForecast = handleForecast;
    }
  }, [onForecastRequest, handleForecast]);

  // Обработка изменения размера окна
  useEffect(() => {
    const handleResize = () => {
      drawChart();
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [drawChart]);

  const timeframes = [
    { value: '1m', label: '1 мин' },
    { value: '5m', label: '5 мин' },
    { value: '15m', label: '15 мин' },
    { value: '1h', label: '1 час' },
    { value: '4h', label: '4 часа' },
    { value: '1d', label: '1 день' },
  ];

  return (
    <div className="card">
      {/* Заголовок и элементы управления */}
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-xl font-semibold text-white">
          График {symbol}
        </h3>
        
        <div className="flex items-center space-x-4">
          {/* Временные интервалы */}
          <div className="flex space-x-1">
            {timeframes.map((tf) => (
              <button
                key={tf.value}
                onClick={() => setTimeframe(tf.value as any)}
                className={`px-3 py-1 rounded text-sm transition-colors ${
                  timeframe === tf.value
                    ? 'bg-orange-500 text-white'
                    : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                }`}
              >
                {tf.label}
              </button>
            ))}
          </div>

          {/* Навигация */}
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setOffset(prev => Math.max(0, prev - 10))}
              className="p-2 bg-gray-800 text-gray-300 hover:bg-gray-700 rounded transition-colors"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            
            <button
              onClick={() => setOffset(prev => prev + 10)}
              className="p-2 bg-gray-800 text-gray-300 hover:bg-gray-700 rounded transition-colors"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>

          {/* Зум */}
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setZoom(prev => Math.max(0.5, prev - 0.1))}
              className="p-2 bg-gray-800 text-gray-300 hover:bg-gray-700 rounded transition-colors"
            >
              <ZoomOut className="w-4 h-4" />
            </button>
            
            <span className="text-sm text-gray-400 min-w-12 text-center">
              {Math.round(zoom * 100)}%
            </span>
            
            <button
              onClick={() => setZoom(prev => Math.min(3, prev + 0.1))}
              className="p-2 bg-gray-800 text-gray-300 hover:bg-gray-700 rounded transition-colors"
            >
              <ZoomIn className="w-4 h-4" />
            </button>
          </div>

          {/* Сброс */}
          <button
            onClick={() => {
              setZoom(1);
              setOffset(0);
            }}
            className="p-2 bg-gray-800 text-gray-300 hover:bg-gray-700 rounded transition-colors"
            title="Сбросить вид"
          >
            <RotateCcw className="w-4 h-4" />
          </button>

        </div>
      </div>

      {/* Canvas для графика */}
      <div className="relative">
        <canvas
          ref={canvasRef}
          className="w-full h-96 bg-gray-900 rounded-lg cursor-crosshair"
          onMouseMove={handleMouseMove}
          onMouseDown={handleMouseDown}
          onMouseUp={handleMouseUp}
          onMouseLeave={handleMouseUp}
          onWheel={handleWheel}
        />
        
        {/* Скролл для листания графика */}
        <div className="mt-4">
          <div className="flex items-center space-x-4">
            <span className="text-sm text-gray-400">Позиция:</span>
            <div className="flex-1 bg-gray-800 rounded-full h-2 relative">
              <div 
                className="bg-orange-500 h-2 rounded-full transition-all duration-200"
                style={{ 
                  width: `${Math.min(100, Math.max(0, (offset / Math.max(1, candles.length - 50)) * 100))}%` 
                }}
              ></div>
            </div>
            <input
              type="range"
              min="0"
              max={Math.max(0, candles.length - 50)}
              value={offset}
              onChange={(e) => setOffset(parseInt(e.target.value))}
              className="w-32 h-2 bg-gray-800 rounded-lg appearance-none cursor-pointer slider"
            />
          </div>
          <div className="flex justify-between text-xs text-gray-500 mt-2">
            <span>Начало</span>
            <span>Конец</span>
          </div>
        </div>
        
        {/* Легенда */}
        <div className="absolute top-4 left-4 flex space-x-4 text-xs">
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-green-500"></div>
            <span className="text-gray-400">Исторические данные</span>
          </div>
          {forecastCandles.length > 0 && (
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-orange-500"></div>
              <span className="text-gray-400">Прогноз</span>
            </div>
          )}
        </div>
      </div>

      {/* Информация */}
      <div className="mt-4 text-sm text-gray-400">
        <p>
          Используется {forecastSettings.trainingDays} дней данных для обучения модели {forecastSettings.model.toUpperCase()}
        </p>
        {forecastCandles.length > 0 && (
          <p className="text-orange-500 mt-2">
            ✓ Прогноз на {forecastSettings.forecastDays} дней готов
          </p>
        )}
        <p className="mt-2 text-xs">
          Используйте колесико мыши для зума, перетаскивание для навигации
        </p>
      </div>
    </div>
  );
};

export default TradingChart;
