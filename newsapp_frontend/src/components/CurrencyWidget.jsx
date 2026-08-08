import React, { useState, useEffect, useMemo } from 'react';
import axios from 'axios';
import { RefreshCw, ArrowRightLeft } from 'lucide-react';

const MAJOR_CURRENCIES = ['USD', 'EUR', 'GBP', 'INR', 'JPY', 'AUD', 'CAD', 'CHF', 'CNY'];

const CurrencyWidget = () => {
  const [rates, setRates] = useState({});
  const [loading, setLoading] = useState(true);
  
  // Converter state
  const [baseCurrency, setBaseCurrency] = useState('USD');
  const [targetCurrency, setTargetCurrency] = useState('INR');
  const [amount, setAmount] = useState(1);

  useEffect(() => {
    const fetchRates = async () => {
      try {
        const response = await axios.get('https://open.er-api.com/v6/latest/USD');
        if (response.data && response.data.rates) {
          setRates(response.data.rates);
        }
      } catch (err) {
        console.error("Error fetching currency rates:", err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchRates();
    const interval = setInterval(fetchRates, 60000 * 60); // refresh every hour
    return () => clearInterval(interval);
  }, []);

  // Generate ticker items
  const tickerItems = useMemo(() => {
    if (!rates || !rates['INR']) return [];
    
    const inr = rates['INR'];
    const items = [];
    
    if (rates['USD']) items.push({ label: '1 USD', value: `= ₹${(inr / rates['USD']).toFixed(2)}` });
    if (rates['EUR']) items.push({ label: '1 EUR', value: `= ₹${(inr / rates['EUR']).toFixed(2)}` });
    if (rates['GBP']) items.push({ label: '1 GBP', value: `= ₹${(inr / rates['GBP']).toFixed(2)}` });
    if (rates['JPY']) items.push({ label: '100 JPY', value: `= ₹${((100 / rates['JPY']) * inr).toFixed(2)}` });
    if (rates['AED']) items.push({ label: '1 AED', value: `= ₹${(inr / rates['AED']).toFixed(2)}` });
    if (rates['CAD']) items.push({ label: '1 CAD', value: `= ₹${(inr / rates['CAD']).toFixed(2)}` });
    if (rates['AUD']) items.push({ label: '1 AUD', value: `= ₹${(inr / rates['AUD']).toFixed(2)}` });
    
    return items;
  }, [rates]);

  // Converter logic
  const convertedAmount = useMemo(() => {
    if (!rates[baseCurrency] || !rates[targetCurrency] || !amount) return '0.00';
    const amountInUSD = amount / rates[baseCurrency];
    return (amountInUSD * rates[targetCurrency]).toFixed(2);
  }, [amount, baseCurrency, targetCurrency, rates]);

  const handleSwap = () => {
    setBaseCurrency(targetCurrency);
    setTargetCurrency(baseCurrency);
  };

  if (loading) {
    return <div className="currency-widget-loading"><RefreshCw className="spinner" size={20} /> Loading currencies...</div>;
  }

  // Duplicate elements for seamless CSS marquee
  const displayItems = [...tickerItems, ...tickerItems, ...tickerItems, ...tickerItems];

  return (
    <div className="currency-widget-container">
      {/* Horizontal Ticker Bar */}
      <div className="currency-ticker-wrapper">
        <div className="currency-ticker-content">
          {displayItems.map((item, idx) => (
            <div key={idx} className="currency-ticker-item">
              <span className="currency-label">{item.label}</span>
              <span className="currency-value">{item.value}</span>
            </div>
          ))}
        </div>
      </div>
      
      {/* Compact Converter */}
      <div className="currency-converter-card">
        <div className="converter-header">
          <span>Live Converter</span>
        </div>
        <div className="converter-body">
          <input 
            type="number" 
            className="converter-input" 
            value={amount} 
            onChange={(e) => setAmount(Number(e.target.value))} 
            min="0"
            step="any"
          />
          <select 
            className="converter-select" 
            value={baseCurrency} 
            onChange={(e) => setBaseCurrency(e.target.value)}
          >
            {MAJOR_CURRENCIES.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
          
          <button className="swap-btn" onClick={handleSwap} title="Swap currencies">
            <ArrowRightLeft size={16} />
          </button>
          
          <div className="converted-result">{convertedAmount}</div>
          <select 
            className="converter-select" 
            value={targetCurrency} 
            onChange={(e) => setTargetCurrency(e.target.value)}
          >
            {MAJOR_CURRENCIES.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </div>
      </div>
    </div>
  );
};

export default CurrencyWidget;
