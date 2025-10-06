import React from 'react';
import { X, Calendar, ExternalLink } from 'lucide-react';
import type { NewsItem } from '../types';

interface NewsModalProps {
  news: NewsItem | null;
  isOpen: boolean;
  onClose: () => void;
}

const NewsModal: React.FC<NewsModalProps> = ({ news, isOpen, onClose }) => {
  if (!isOpen || !news) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-900 rounded-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          {/* Header */}
          <div className="flex justify-between items-start mb-6">
            <div className="flex-1">
              <h2 className="text-2xl font-bold text-white mb-2">{news.title}</h2>
              <div className="flex items-center space-x-4 text-sm text-gray-400">
                <div className="flex items-center space-x-1">
                  <Calendar className="w-4 h-4" />
                  <span>{new Date(news.publishedAt).toLocaleDateString('ru-RU')}</span>
                </div>
                <div className="flex items-center space-x-1">
                  <ExternalLink className="w-4 h-4" />
                  <span>{news.source}</span>
                </div>
              </div>
            </div>
            <button
              onClick={onClose}
              className="p-2 text-gray-400 hover:text-white transition-colors"
            >
              <X className="w-6 h-6" />
            </button>
          </div>

          {/* Sentiment Badge */}
          <div className="mb-6">
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${
              news.sentiment === 'positive' 
                ? 'bg-green-900 text-green-300'
                : news.sentiment === 'negative'
                ? 'bg-red-900 text-red-300'
                : 'bg-gray-800 text-gray-300'
            }`}>
              {news.sentiment === 'positive' ? 'Позитивная новость' : 
               news.sentiment === 'negative' ? 'Негативная новость' : 'Нейтральная новость'}
            </span>
          </div>

          {/* Summary */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-white mb-3">Краткое содержание</h3>
            <p className="text-gray-300 leading-relaxed">{news.summary}</p>
          </div>

          {/* Full Content */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-white mb-3">Полный текст</h3>
            <div className="prose prose-invert max-w-none">
              <p className="text-gray-300 leading-relaxed whitespace-pre-line">
                {news.content}
              </p>
            </div>
          </div>

          {/* Actions */}
          <div className="flex justify-end space-x-4 pt-6 border-t border-gray-800">
            <button
              onClick={onClose}
              className="px-6 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-700 transition-colors"
            >
              Закрыть
            </button>
            <button className="btn-primary">
              Поделиться
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NewsModal;
