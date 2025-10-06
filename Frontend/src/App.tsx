import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import DataUploadPage from './pages/DataUploadPage';
import StocksPage from './pages/StocksPage';
import StockDetailPage from './pages/StockDetailPage';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<DataUploadPage />} />
          <Route path="/stocks" element={<StocksPage />} />
          <Route path="/stocks/:id" element={<StockDetailPage />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
