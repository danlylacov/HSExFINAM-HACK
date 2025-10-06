import React from 'react';
import { Link } from 'react-router-dom';
import { TrendingUp, TrendingDown } from 'lucide-react';
import type { Stock } from '../types';
import { formatPrice, formatChange, formatChangePercent } from '../utils';

interface StockCardProps {
  stock: Stock;
}

const StockCard: React.FC<StockCardProps> = ({ stock }) => {
  const isPositive = stock.change >= 0;

  return (
    <Link to={`/stocks/${stock.id}`} className="block group">
      <div className="card hover:border-orange-500/50 transition-all duration-200 group-hover:scale-105">
        <div className="mb-4">
          <div className="flex items-center space-x-3 mb-3">
            <div className="w-12 h-12 rounded-lg bg-gray-800 flex items-center justify-center overflow-hidden flex-shrink-0">
              <img
                src={stock.logo}
                alt={stock.name}
                className="w-8 h-8 object-contain"
                onError={(e) => {
                  const target = e.target as HTMLImageElement;
                  target.style.display = 'none';
                  target.nextElementSibling?.classList.remove('hidden');
                }}
              />
              <div className="w-8 h-8 bg-gradient-to-r from-orange-500 to-purple-600 rounded flex items-center justify-center text-white font-bold text-sm hidden">
                {stock.symbol.charAt(0)}
              </div>
            </div>
            <div className="min-w-0 flex-1">
              <h3 className="text-white font-semibold text-lg">{stock.symbol}</h3>
              <p className="text-gray-400 text-sm">{stock.name}</p>
            </div>
          </div>
          
          <div className="flex items-center justify-between">
            <div className="text-white font-bold text-lg">{formatPrice(stock.currentPrice)}</div>
            <div className={`flex items-center space-x-1 text-sm ${
              isPositive ? 'text-green-400' : 'text-red-400'
            }`}>
              {isPositive ? (
                <TrendingUp className="w-4 h-4" />
              ) : (
                <TrendingDown className="w-4 h-4" />
              )}
              <span>{formatChange(stock.change)}</span>
              <span>({formatChangePercent(stock.changePercent)})</span>
            </div>
          </div>
        </div>
        
        <div className="flex justify-between text-sm text-gray-400">
          <div className="truncate">
            <span className="text-gray-500">Объем:</span>
            <span className="ml-1">{stock.volume.toLocaleString()}</span>
          </div>
          <div className="truncate ml-2">
            <span className="text-gray-500">Кап:</span>
            <span className="ml-1">${(stock.marketCap / 1e9).toFixed(1)}B</span>
          </div>
        </div>
      </div>
    </Link>
  );
};

export default StockCard;
