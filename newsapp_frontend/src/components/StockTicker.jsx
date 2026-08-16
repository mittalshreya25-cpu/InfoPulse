import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

const StockTicker = () => {
  const [quotes, setQuotes] = useState([]);
  const [loading, setLoading] = useState(true);

  const symbols = '^GSPC,^IXIC,^NSEI,^BSESN,BTC-USD';
  
  // Mapping for cleaner display names
  const nameMap = {
    '^GSPC': 'S&P 500',
    '^IXIC': 'NASDAQ',
    '^NSEI': 'NIFTY 50',
    '^BSESN': 'SENSEX',
    'BTC-USD': 'BTC/USD'
  };

  useEffect(() => {
    const fetchQuotes = async () => {
      try {
        // Fetching from our own reliable backend instead of a flaky public proxy
        const response = await axios.get(`${API_BASE_URL}/stocks`);
        const results = response.data || [];
        
        if (results.length > 0) {
          setQuotes(results);
        } else {
          loadMockData();
        }
      } catch (err) {
        console.error("Error fetching stock data, using mock data:", err);
        loadMockData();
      } finally {
        setLoading(false);
      }
    };

    fetchQuotes();
    
    // Refresh every 60 seconds
    const interval = setInterval(fetchQuotes, 60000);
    return () => clearInterval(interval);
  }, []);

  const loadMockData = () => {
    setQuotes([
      { symbol: '^GSPC', regularMarketPrice: 5123.45, regularMarketChangePercent: 0.85 },
      { symbol: '^IXIC', regularMarketPrice: 16234.12, regularMarketChangePercent: -1.2 },
      { symbol: '^NSEI', regularMarketPrice: 22456.70, regularMarketChangePercent: 0.45 },
      { symbol: '^BSESN', regularMarketPrice: 73890.10, regularMarketChangePercent: 0.55 },
      { symbol: 'BTC-USD', regularMarketPrice: 65432.10, regularMarketChangePercent: 2.34 }
    ]);
  };

  if (loading) {
    return <div className="ticker-wrapper"><div className="ticker-loading">Loading market data...</div></div>;
  }

  // Duplicate items to create a seamless scrolling loop
  const displayItems = [...quotes, ...quotes, ...quotes, ...quotes];

  return (
    <div className="ticker-wrapper">
      <div className="ticker-content">
        {displayItems.map((quote, idx) => {
          const isPositive = quote.regularMarketChangePercent > 0;
          const isNegative = quote.regularMarketChangePercent < 0;
          const displayName = nameMap[quote.symbol] || quote.symbol;
          const price = quote.regularMarketPrice?.toFixed(2) || '0.00';
          const change = quote.regularMarketChangePercent?.toFixed(2) || '0.00';

          return (
            <div key={`${quote.symbol}-${idx}`} className="ticker-item">
              <span className="ticker-name">{displayName}</span>
              <span className="ticker-price">{price}</span>
              <span className={`ticker-change ${isPositive ? 'positive' : isNegative ? 'negative' : 'neutral'}`}>
                {isPositive ? <TrendingUp size={14} /> : isNegative ? <TrendingDown size={14} /> : <Minus size={14} />}
                {isPositive ? '+' : ''}{change}%
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default StockTicker;
