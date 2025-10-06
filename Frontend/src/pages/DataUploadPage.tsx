import React, { useState, useCallback } from 'react';
import { Upload, FileText, CheckCircle, Download, Calendar } from 'lucide-react';
import { Link } from 'react-router-dom';

interface UploadedFile {
  name: string;
  size: number;
  type: string;
  content: string;
}

const DataUploadPage: React.FC = () => {
  const [stocksFile, setStocksFile] = useState<UploadedFile | null>(null);
  const [newsFile, setNewsFile] = useState<UploadedFile | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [processingStatus, setProcessingStatus] = useState<string>('');

  const handleFileUpload = useCallback((file: File, type: 'stocks' | 'news') => {
    if (!file.name.toLowerCase().endsWith('.csv')) {
      alert('Пожалуйста, выберите CSV файл');
      return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
      const content = e.target?.result as string;
      const uploadedFile: UploadedFile = {
        name: file.name,
        size: file.size,
        type: file.type,
        content
      };

      if (type === 'stocks') {
        setStocksFile(uploadedFile);
      } else {
        setNewsFile(uploadedFile);
      }
    };
    reader.readAsText(file);
  }, []);

  const handleStocksFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFileUpload(file, 'stocks');
    }
  };

  const handleNewsFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFileUpload(file, 'news');
    }
  };

  const processFiles = async () => {
    if (!stocksFile || !newsFile) {
      alert('Пожалуйста, загрузите оба файла');
      return;
    }

    setIsProcessing(true);
    setProcessingStatus('Обработка файлов...');

    try {
      // Симуляция обработки файлов
      await new Promise(resolve => setTimeout(resolve, 2000));
      setProcessingStatus('Анализ данных...');
      await new Promise(resolve => setTimeout(resolve, 1500));
      setProcessingStatus('Создание прогнозов...');
      await new Promise(resolve => setTimeout(resolve, 2000));
      setProcessingStatus('Готово!');
      
      // Здесь можно добавить логику для обработки CSV файлов
      console.log('Stocks file:', stocksFile);
      console.log('News file:', newsFile);
      
    } catch (error) {
      setProcessingStatus('Ошибка при обработке файлов');
    } finally {
      setIsProcessing(false);
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="min-h-screen py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-white mb-4">
            Загрузка данных
          </h1>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto">
            Загрузите CSV файлы с котировками акций и новостями для анализа и прогнозирования
          </p>
        </div>

        {/* Upload Sections */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Stocks File Upload */}
          <div className="card">
            <div className="flex items-center space-x-3 mb-6">
              <div className="w-12 h-12 bg-orange-500/20 rounded-lg flex items-center justify-center">
                <FileText className="w-6 h-6 text-orange-500" />
              </div>
              <div>
                <h2 className="text-xl font-semibold text-white">Котировки акций</h2>
                <p className="text-gray-400 text-sm">CSV файл с историческими данными</p>
              </div>
            </div>

            <div className="space-y-4">
              <div className="border-2 border-dashed border-gray-700 rounded-lg p-6 text-center hover:border-gray-600 transition-colors">
                <input
                  type="file"
                  accept=".csv"
                  onChange={handleStocksFileChange}
                  className="hidden"
                  id="stocks-upload"
                />
                <label
                  htmlFor="stocks-upload"
                  className="cursor-pointer flex flex-col items-center space-y-2"
                >
                  <Upload className="w-8 h-8 text-gray-400" />
                  <span className="text-gray-400">
                    {stocksFile ? 'Изменить файл' : 'Выберите CSV файл'}
                  </span>
                </label>
              </div>

              {stocksFile && (
                <div className="flex items-center space-x-3 p-3 bg-green-900/20 border border-green-800 rounded-lg">
                  <CheckCircle className="w-5 h-5 text-green-400 flex-shrink-0" />
                  <div className="flex-1 min-w-0">
                    <p className="text-white font-medium truncate">{stocksFile.name}</p>
                    <p className="text-gray-400 text-sm">{formatFileSize(stocksFile.size)}</p>
                  </div>
                </div>
              )}

              <div className="text-xs text-gray-500">
                <p>Ожидаемый формат:</p>
                <p>symbol,date,open,high,low,close,volume</p>
              </div>
            </div>
          </div>

          {/* News File Upload */}
          <div className="card">
            <div className="flex items-center space-x-3 mb-6">
              <div className="w-12 h-12 bg-purple-600/20 rounded-lg flex items-center justify-center">
                <Calendar className="w-6 h-6 text-purple-600" />
              </div>
              <div>
                <h2 className="text-xl font-semibold text-white">Новости</h2>
                <p className="text-gray-400 text-sm">CSV файл с новостями за период</p>
              </div>
            </div>

            <div className="space-y-4">
              <div className="border-2 border-dashed border-gray-700 rounded-lg p-6 text-center hover:border-gray-600 transition-colors">
                <input
                  type="file"
                  accept=".csv"
                  onChange={handleNewsFileChange}
                  className="hidden"
                  id="news-upload"
                />
                <label
                  htmlFor="news-upload"
                  className="cursor-pointer flex flex-col items-center space-y-2"
                >
                  <Upload className="w-8 h-8 text-gray-400" />
                  <span className="text-gray-400">
                    {newsFile ? 'Изменить файл' : 'Выберите CSV файл'}
                  </span>
                </label>
              </div>

              {newsFile && (
                <div className="flex items-center space-x-3 p-3 bg-green-900/20 border border-green-800 rounded-lg">
                  <CheckCircle className="w-5 h-5 text-green-400 flex-shrink-0" />
                  <div className="flex-1 min-w-0">
                    <p className="text-white font-medium truncate">{newsFile.name}</p>
                    <p className="text-gray-400 text-sm">{formatFileSize(newsFile.size)}</p>
                  </div>
                </div>
              )}

              <div className="text-xs text-gray-500">
                <p>Ожидаемый формат:</p>
                <p>title,content,date,sentiment,symbol</p>
              </div>
            </div>
          </div>
        </div>

        {/* Processing Status */}
        {isProcessing && (
          <div className="card mb-8">
            <div className="flex items-center space-x-3">
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-orange-500"></div>
              <span className="text-white">{processingStatus}</span>
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button
            onClick={processFiles}
            disabled={!stocksFile || !newsFile || isProcessing}
            className="btn-primary px-8 py-3 text-lg disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isProcessing ? 'Обработка...' : 'Начать анализ'}
          </button>
          
          <Link
            to="/stocks"
            className="btn-secondary px-8 py-3 text-lg text-center"
          >
            Перейти к акциям
          </Link>
        </div>

        {/* Sample Files Download */}
        <div className="mt-12 card">
          <h3 className="text-lg font-semibold text-white mb-4">Примеры файлов</h3>
          <p className="text-gray-400 mb-4">
            Скачайте примеры файлов для понимания требуемого формата
          </p>
          <div className="flex flex-col sm:flex-row gap-4">
            <button 
              onClick={() => window.open('/sample_stocks.csv', '_blank')}
              className="btn-secondary flex items-center justify-center space-x-2"
            >
              <Download className="w-4 h-4" />
              <span>Пример котировок</span>
            </button>
            <button 
              onClick={() => window.open('/sample_news.csv', '_blank')}
              className="btn-secondary flex items-center justify-center space-x-2"
            >
              <Download className="w-4 h-4" />
              <span>Пример новостей</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DataUploadPage;
