import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { TrendingUp, User, LogIn, LogOut } from 'lucide-react';
import AuthModal from './AuthModal';
import type { User as UserType } from '../types';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const location = useLocation();
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const [user, setUser] = useState<UserType | null>(null);

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  const handleLogin = (email: string, _password: string) => {
    // Simulate login
    setUser({
      id: '1',
      email,
      name: email.split('@')[0],
    });
  };

  const handleRegister = (name: string, email: string, _password: string) => {
    // Simulate registration
    setUser({
      id: '1',
      email,
      name,
    });
  };

  const handleLogout = () => {
    setUser(null);
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="bg-gray-900 border-b border-gray-800 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <Link to="/" className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-r from-orange-500 to-purple-600 rounded-lg flex items-center justify-center">
                <TrendingUp className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-white">Back2Back Forecast.AI</span>
            </Link>

            {/* Navigation */}
            <nav className="hidden md:flex space-x-8">
              <Link
                to="/"
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  isActive('/') 
                    ? 'text-orange-500 bg-gray-800' 
                    : 'text-gray-300 hover:text-white hover:bg-gray-800'
                }`}
              >
                Загрузка данных
              </Link>
              <Link
                to="/stocks"
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  isActive('/stocks') 
                    ? 'text-orange-500 bg-gray-800' 
                    : 'text-gray-300 hover:text-white hover:bg-gray-800'
                }`}
              >
                Акции
              </Link>
            </nav>

            {/* User Actions */}
            <div className="flex items-center space-x-4">
              {user ? (
                <>
                  <div className="flex items-center space-x-2 text-gray-300">
                    <User className="w-5 h-5" />
                    <span className="hidden sm:block">{user.name}</span>
                  </div>
                  <button 
                    onClick={handleLogout}
                    className="flex items-center space-x-2 text-gray-400 hover:text-white transition-colors"
                  >
                    <LogOut className="w-4 h-4" />
                    <span className="hidden sm:block">Выйти</span>
                  </button>
                </>
              ) : (
                <button 
                  onClick={() => setIsAuthModalOpen(true)}
                  className="btn-primary flex items-center space-x-2"
                >
                  <LogIn className="w-4 h-4" />
                  <span>Войти</span>
                </button>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1">
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 border-t border-gray-800 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="col-span-1 md:col-span-2">
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-8 h-8 bg-gradient-to-r from-orange-500 to-purple-600 rounded-lg flex items-center justify-center">
                  <TrendingUp className="w-5 h-5 text-white" />
                </div>
                <span className="text-xl font-bold text-white">Back2Back Forecast.AI</span>
              </div>
              <p className="text-gray-400 text-sm max-w-md">
                Интеллектуальная система прогнозирования цен на финансовые инструменты с использованием передовых алгоритмов машинного обучения.
              </p>
            </div>
            
            <div>
              <h3 className="text-white font-semibold mb-4">Продукт</h3>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Акции</a></li>
                <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Прогнозы</a></li>
                <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Аналитика</a></li>
                <li><a href="#" className="text-gray-400 hover:text-white transition-colors">API</a></li>
              </ul>
            </div>
            
            <div>
              <h3 className="text-white font-semibold mb-4">Поддержка</h3>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Документация</a></li>
                <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Контакты</a></li>
                <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Статус</a></li>
                <li><a href="#" className="text-gray-400 hover:text-white transition-colors">FAQ</a></li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-gray-800 mt-8 pt-8 text-center">
            <p className="text-gray-400 text-sm">
              © 2024 Back2Back Forecast.AI. Все права защищены.
            </p>
          </div>
        </div>
      </footer>

      {/* Auth Modal */}
      <AuthModal
        isOpen={isAuthModalOpen}
        onClose={() => setIsAuthModalOpen(false)}
        onLogin={handleLogin}
        onRegister={handleRegister}
      />
    </div>
  );
};

export default Layout;
