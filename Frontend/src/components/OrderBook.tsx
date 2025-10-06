import React, { useState, useEffect } from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';

interface OrderBookProps {
  symbol: string;
}

interface OrderBookEntry {
  price: number;
  amount: number;
  total: number;
}

const OrderBook: React.FC<OrderBookProps> = ({ symbol }) => {
  const [bids, setBids] = useState<OrderBookEntry[]>([]);
  const [asks, setAsks] = useState<OrderBookEntry[]>([]);
  const [spread, setSpread] = useState(0);

  // Генерация моковых данных для ордербука
  useEffect(() => {
    const generateOrderBook = () => {
      const basePrice = 175.43;
      const bidEntries: OrderBookEntry[] = [];
      const askEntries: OrderBookEntry[] = [];
      
      let bidTotal = 0;
      let askTotal = 0;

      // Генерация заявок на покупку (bids)
      for (let i = 0; i < 10; i++) {
        const price = basePrice - (i + 1) * 0.01;
        const amount = Math.random() * 1000 + 100;
        bidTotal += amount;
        
        bidEntries.push({
          price: Number(price.toFixed(2)),
          amount: Number(amount.toFixed(2)),
          total: Number(bidTotal.toFixed(2))
        });
      }

      // Генерация заявок на продажу (asks)
      for (let i = 0; i < 10; i++) {
        const price = basePrice + (i + 1) * 0.01;
        const amount = Math.random() * 1000 + 100;
        askTotal += amount;
        
        askEntries.push({
          price: Number(price.toFixed(2)),
          amount: Number(amount.toFixed(2)),
          total: Number(askTotal.toFixed(2))
        });
      }

      setBids(bidEntries);
      setAsks(askEntries);
      setSpread(Number((askEntries[0].price - bidEntries[0].price).toFixed(2)));
    };

    generateOrderBook();
    
    // Обновление данных каждые 2 секунды
    const interval = setInterval(generateOrderBook, 2000);
    return () => clearInterval(interval);
  }, [symbol]);

  const formatPrice = (price: number) => {
    return price.toFixed(2);
  };

  const formatAmount = (amount: number) => {
    return amount.toFixed(2);
  };

  const getMaxTotal = () => {
    const maxBid = Math.max(...bids.map(b => b.total));
    const maxAsk = Math.max(...asks.map(a => a.total));
    return Math.max(maxBid, maxAsk);
  };

  const maxTotal = getMaxTotal();

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-white">Стакан заявок</h3>
        <div className="text-sm text-gray-400">
          Спред: <span className="text-orange-500 font-semibold">{formatPrice(spread)}</span>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        {/* Заявки на продажу (Asks) */}
        <div>
          <div className="flex items-center space-x-2 mb-3">
            <TrendingUp className="w-4 h-4 text-red-400" />
            <h4 className="text-red-400 font-semibold text-sm">Продажа</h4>
          </div>
          
          <div className="space-y-1">
            {asks.slice().reverse().map((ask, index) => (
              <div key={index} className="relative group">
                <div 
                  className="flex justify-between items-center py-1 px-2 rounded text-xs hover:bg-gray-800 transition-colors cursor-pointer"
                  style={{
                    background: `linear-gradient(to right, rgba(239, 83, 80, 0.1) ${(ask.total / maxTotal) * 100}%, transparent ${(ask.total / maxTotal) * 100}%)`
                  }}
                >
                  <div className="text-red-400 font-mono">
                    {formatPrice(ask.price)}
                  </div>
                  <div className="text-gray-300 font-mono">
                    {formatAmount(ask.amount)}
                  </div>
                </div>
                
                {/* Tooltip */}
                <div className="absolute right-full top-0 mr-2 bg-gray-900 text-white text-xs p-2 rounded shadow-lg opacity-0 group-hover:opacity-100 transition-opacity z-10">
                  <div>Цена: {formatPrice(ask.price)}</div>
                  <div>Объем: {formatAmount(ask.amount)}</div>
                  <div>Накопленный: {formatAmount(ask.total)}</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Заявки на покупку (Bids) */}
        <div>
          <div className="flex items-center space-x-2 mb-3">
            <TrendingDown className="w-4 h-4 text-green-400" />
            <h4 className="text-green-400 font-semibold text-sm">Покупка</h4>
          </div>
          
          <div className="space-y-1">
            {bids.map((bid, index) => (
              <div key={index} className="relative group">
                <div 
                  className="flex justify-between items-center py-1 px-2 rounded text-xs hover:bg-gray-800 transition-colors cursor-pointer"
                  style={{
                    background: `linear-gradient(to right, rgba(38, 166, 154, 0.1) ${(bid.total / maxTotal) * 100}%, transparent ${(bid.total / maxTotal) * 100}%)`
                  }}
                >
                  <div className="text-green-400 font-mono">
                    {formatPrice(bid.price)}
                  </div>
                  <div className="text-gray-300 font-mono">
                    {formatAmount(bid.amount)}
                  </div>
                </div>
                
                {/* Tooltip */}
                <div className="absolute left-full top-0 ml-2 bg-gray-900 text-white text-xs p-2 rounded shadow-lg opacity-0 group-hover:opacity-100 transition-opacity z-10">
                  <div>Цена: {formatPrice(bid.price)}</div>
                  <div>Объем: {formatAmount(bid.amount)}</div>
                  <div>Накопленный: {formatAmount(bid.total)}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Статистика */}
      <div className="mt-6 pt-4 border-t border-gray-800">
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <div className="text-gray-400 mb-1">Лучшая цена покупки</div>
            <div className="text-green-400 font-semibold">
              {bids.length > 0 ? formatPrice(bids[0].price) : 'N/A'}
            </div>
          </div>
          <div>
            <div className="text-gray-400 mb-1">Лучшая цена продажи</div>
            <div className="text-red-400 font-semibold">
              {asks.length > 0 ? formatPrice(asks[0].price) : 'N/A'}
            </div>
          </div>
        </div>
      </div>

      {/* Информация */}
      <div className="mt-4 text-xs text-gray-500">
        <p>Данные обновляются в реальном времени</p>
        <p>Объемы показаны в логарифмическом масштабе</p>
      </div>
    </div>
  );
};

export default OrderBook;
