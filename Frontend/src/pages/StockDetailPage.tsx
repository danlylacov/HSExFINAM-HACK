import React, { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, TrendingUp, TrendingDown, Calendar, BarChart3 } from 'lucide-react';
import DualChart from '../components/DualChart';
import TechnicalIndicatorsModal from '../components/TechnicalIndicatorsModal';
import NewsModal from '../components/NewsModal';
import { mockStocks, mockNews } from '../data/mockData';
import type { ForecastSettings, NewsItem } from '../types';
import { formatPrice, formatChange, formatChangePercent, formatVolume, formatMarketCap } from '../utils';

const StockDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [forecastSettings, setForecastSettings] = useState<ForecastSettings>({
    trainingDays: 30,
    forecastDays: 7,
    model: 'lstm',
  });
  const [selectedNews, setSelectedNews] = useState<NewsItem | null>(null);
  const [isNewsModalOpen, setIsNewsModalOpen] = useState(false);
  const [isIndicatorsModalOpen, setIsIndicatorsModalOpen] = useState(false);

  const stock = mockStocks.find(s => s.id === id);
  const relatedNews = mockNews.filter(news => 
    news.title.toLowerCase().includes(stock?.symbol.toLowerCase() || '') ||
    news.title.toLowerCase().includes(stock?.name.toLowerCase() || '')
  );

  const handleNewsClick = (news: NewsItem) => {
    setSelectedNews(news);
    setIsNewsModalOpen(true);
  };

  const handleCloseNewsModal = () => {
    setIsNewsModalOpen(false);
    setSelectedNews(null);
  };

  if (!stock) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-white mb-4">Акция не найдена</h1>
          <Link to="/stocks" className="btn-primary">
            Вернуться к списку акций
          </Link>
        </div>
      </div>
    );
  }

  const isPositive = stock.change >= 0;

  return (
    <div className="min-h-screen py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Back Button */}
        <Link 
          to="/stocks" 
          className="inline-flex items-center space-x-2 text-gray-400 hover:text-white transition-colors mb-6"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Назад к списку акций</span>
        </Link>

        {/* Stock Header */}
        <div className="card mb-8">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between">
            <div className="flex items-center space-x-4 mb-4 lg:mb-0">
              <div className="w-16 h-16 rounded-lg bg-gray-800 flex items-center justify-center overflow-hidden">
                <img
                  src={stock.logo}
                  alt={stock.name}
                  className="w-12 h-12 object-contain"
                  onError={(e) => {
                    const target = e.target as HTMLImageElement;
                    target.style.display = 'none';
                    target.nextElementSibling?.classList.remove('hidden');
                  }}
                />
                <div className="w-12 h-12 bg-gradient-to-r from-orange-500 to-purple-600 rounded flex items-center justify-center text-white font-bold text-lg hidden">
                  {stock.symbol.charAt(0)}
                </div>
              </div>
              
              <div>
                <h1 className="text-3xl font-bold text-white">{stock.symbol}</h1>
                <p className="text-gray-400 text-lg">{stock.name}</p>
              </div>
            </div>

            <div className="text-right">
              <div className="text-4xl font-bold text-white mb-2">
                {formatPrice(stock.currentPrice)}
              </div>
              <div className={`flex items-center justify-end space-x-2 text-lg ${
                isPositive ? 'text-green-400' : 'text-red-400'
              }`}>
                {isPositive ? (
                  <TrendingUp className="w-5 h-5" />
                ) : (
                  <TrendingDown className="w-5 h-5" />
                )}
                <span>{formatChange(stock.change)}</span>
                <span>({formatChangePercent(stock.changePercent)})</span>
              </div>
            </div>
          </div>

          {/* Stock Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-8 pt-8 border-t border-gray-800">
            <div>
              <div className="text-gray-400 text-sm mb-1">Объем торгов</div>
              <div className="text-white font-semibold">{formatVolume(stock.volume)}</div>
            </div>
            <div>
              <div className="text-gray-400 text-sm mb-1">Рыночная капитализация</div>
              <div className="text-white font-semibold">{formatMarketCap(stock.marketCap)}</div>
            </div>
            <div>
              <div className="text-gray-400 text-sm mb-1">52-недельный максимум</div>
              <div className="text-white font-semibold">{formatPrice(stock.currentPrice * 1.2)}</div>
            </div>
            <div>
              <div className="text-gray-400 text-sm mb-1">52-недельный минимум</div>
              <div className="text-white font-semibold">{formatPrice(stock.currentPrice * 0.8)}</div>
            </div>
          </div>
        </div>

        {/* Description */}
        {stock.description && (
          <div className="card mb-8">
            <h2 className="text-xl font-semibold text-white mb-4">О компании</h2>
            <p className="text-gray-400 leading-relaxed">{stock.description}</p>
          </div>
        )}

        {/* Chart and Forecast Settings */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
          <div className="lg:col-span-2">
            <DualChart 
              forecastSettings={forecastSettings}
            />
            
            {/* Кнопки под графиком */}
            <div className="mt-4">
              <button
                onClick={() => setIsIndicatorsModalOpen(true)}
                className="btn-secondary flex items-center justify-center space-x-2 w-full"
              >
                <BarChart3 className="w-4 h-4" />
                <span>Показать индикаторы</span>
              </button>
            </div>
          </div>
          
          <div className="card">
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-white">Настройки прогноза</h3>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm text-gray-400 mb-2">
                  Интервал прогноза (дни)
                </label>
                <input
                  type="number"
                  min="1"
                  max="20"
                  value={forecastSettings.forecastDays}
                  onChange={(e) => setForecastSettings(prev => ({
                    ...prev,
                    forecastDays: parseInt(e.target.value) || 7
                  }))}
                  className="input-field w-full"
                />
              </div>
            </div>

          </div>
        </div>

        {/* News Section */}
        <div className="card">
          <h2 className="text-xl font-semibold text-white mb-6 flex items-center space-x-2">
            <Calendar className="w-5 h-5" />
            <span>Новости</span>
          </h2>
          
          {relatedNews.length > 0 ? (
            <div className="space-y-4">
              {relatedNews.map((news) => (
                <div 
                  key={news.id} 
                  className="border border-gray-800 rounded-lg p-4 hover:border-gray-700 transition-colors cursor-pointer"
                  onClick={() => handleNewsClick(news)}
                >
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="text-white font-medium hover:text-orange-500 transition-colors">{news.title}</h3>
                    <span className={`px-2 py-1 rounded-full text-xs ${
                      news.sentiment === 'positive' 
                        ? 'bg-green-900 text-green-300'
                        : news.sentiment === 'negative'
                        ? 'bg-red-900 text-red-300'
                        : 'bg-gray-800 text-gray-300'
                    }`}>
                      {news.sentiment === 'positive' ? 'Позитивно' : 
                       news.sentiment === 'negative' ? 'Негативно' : 'Нейтрально'}
                    </span>
                  </div>
                  <p className="text-gray-400 text-sm mb-2">{news.summary}</p>
                  <div className="flex justify-between items-center text-xs text-gray-500">
                    <span>{news.source}</span>
                    <span>{new Date(news.publishedAt).toLocaleDateString('ru-RU')}</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <Calendar className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-400">Новости по данной акции не найдены</p>
            </div>
          )}
        </div>
      </div>

      {/* News Modal */}
      <NewsModal
        news={selectedNews}
        isOpen={isNewsModalOpen}
        onClose={handleCloseNewsModal}
      />

      {/* Technical Indicators Modal */}
      <TechnicalIndicatorsModal
        isOpen={isIndicatorsModalOpen}
        onClose={() => setIsIndicatorsModalOpen(false)}
        symbol={stock.symbol}
      />
    </div>
  );
};

export default StockDetailPage;
