import React, { useState, useMemo } from 'react';
import { Search, Filter, TrendingUp, TrendingDown } from 'lucide-react';
import StockCard from '../components/StockCard';
import { mockStocks } from '../data/mockData';

const StocksPage: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState<'name' | 'price' | 'change' | 'volume'>('name');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');
  const [filterBy, setFilterBy] = useState<'all' | 'gainers' | 'losers'>('all');

  const filteredAndSortedStocks = useMemo(() => {
    let filtered = mockStocks.filter((stock) => {
      const matchesSearch = stock.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           stock.symbol.toLowerCase().includes(searchTerm.toLowerCase());
      
      let matchesFilter = true;
      if (filterBy === 'gainers') {
        matchesFilter = stock.change > 0;
      } else if (filterBy === 'losers') {
        matchesFilter = stock.change < 0;
      }
      
      return matchesSearch && matchesFilter;
    });

    filtered.sort((a, b) => {
      let aValue: number | string;
      let bValue: number | string;

      switch (sortBy) {
        case 'name':
          aValue = a.name;
          bValue = b.name;
          break;
        case 'price':
          aValue = a.currentPrice;
          bValue = b.currentPrice;
          break;
        case 'change':
          aValue = a.changePercent;
          bValue = b.changePercent;
          break;
        case 'volume':
          aValue = a.volume;
          bValue = b.volume;
          break;
        default:
          aValue = a.name;
          bValue = b.name;
      }

      if (typeof aValue === 'string' && typeof bValue === 'string') {
        return sortOrder === 'asc' 
          ? aValue.localeCompare(bValue)
          : bValue.localeCompare(aValue);
      } else {
        return sortOrder === 'asc' 
          ? (aValue as number) - (bValue as number)
          : (bValue as number) - (aValue as number);
      }
    });

    return filtered;
  }, [searchTerm, sortBy, sortOrder, filterBy]);

  const handleSort = (field: typeof sortBy) => {
    if (sortBy === field) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(field);
      setSortOrder('asc');
    }
  };

  return (
    <div className="min-h-screen py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-4">Акции</h1>
          <p className="text-gray-400 text-lg">
            Отслеживайте и анализируйте акции ведущих компаний мира
          </p>
        </div>

        {/* Filters and Search */}
        <div className="mb-8 space-y-4">
          {/* Search */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Поиск по названию или символу..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="input-field w-full pl-10 pr-4 py-3"
            />
          </div>

          {/* Filters */}
          <div className="flex flex-wrap gap-4 items-center">
            <div className="flex items-center space-x-2">
              <Filter className="w-5 h-5 text-gray-400" />
              <span className="text-gray-400">Фильтр:</span>
            </div>
            
            <button
              onClick={() => setFilterBy('all')}
              className={`px-4 py-2 rounded-lg transition-colors ${
                filterBy === 'all'
                  ? 'bg-orange-500 text-white'
                  : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
              }`}
            >
              Все
            </button>
            
            <button
              onClick={() => setFilterBy('gainers')}
              className={`px-4 py-2 rounded-lg transition-colors flex items-center space-x-1 ${
                filterBy === 'gainers'
                  ? 'bg-green-600 text-white'
                  : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
              }`}
            >
              <TrendingUp className="w-4 h-4" />
              <span>Рост</span>
            </button>
            
            <button
              onClick={() => setFilterBy('losers')}
              className={`px-4 py-2 rounded-lg transition-colors flex items-center space-x-1 ${
                filterBy === 'losers'
                  ? 'bg-red-600 text-white'
                  : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
              }`}
            >
              <TrendingDown className="w-4 h-4" />
              <span>Падение</span>
            </button>
          </div>

          {/* Sort Options */}
          <div className="flex flex-wrap gap-2 items-center">
            <span className="text-gray-400">Сортировка:</span>
            {[
              { key: 'name', label: 'Название' },
              { key: 'price', label: 'Цена' },
              { key: 'change', label: 'Изменение' },
              { key: 'volume', label: 'Объем' },
            ].map(({ key, label }) => (
              <button
                key={key}
                onClick={() => handleSort(key as typeof sortBy)}
                className={`px-3 py-1 rounded-md text-sm transition-colors ${
                  sortBy === key
                    ? 'bg-purple-600 text-white'
                    : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                }`}
              >
                {label}
                {sortBy === key && (
                  <span className="ml-1">
                    {sortOrder === 'asc' ? '↑' : '↓'}
                  </span>
                )}
              </button>
            ))}
          </div>
        </div>

        {/* Results Count */}
        <div className="mb-6">
          <p className="text-gray-400">
            Найдено акций: <span className="text-white font-semibold">{filteredAndSortedStocks.length}</span>
          </p>
        </div>

        {/* Stocks Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {filteredAndSortedStocks.map((stock) => (
            <StockCard key={stock.id} stock={stock} />
          ))}
        </div>

        {/* Empty State */}
        {filteredAndSortedStocks.length === 0 && (
          <div className="text-center py-12">
            <div className="w-24 h-24 bg-gray-800 rounded-full flex items-center justify-center mx-auto mb-4">
              <Search className="w-12 h-12 text-gray-400" />
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">Акции не найдены</h3>
            <p className="text-gray-400">
              Попробуйте изменить параметры поиска или фильтры
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default StocksPage;
