import React, { useState, useEffect, useMemo } from 'react';
import axios from 'axios';
import { Loader2, AlertCircle } from 'lucide-react';
import ArticleCard from './components/ArticleCard';
import StockTicker from './components/StockTicker';
import CurrencyWidget from './components/CurrencyWidget';
import Starfield from './components/Starfield';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

function App() {
  const [articles, setArticles] = useState([]);
  const [trending, setTrending] = useState([]);
  const [categories, setCategories] = useState([
    'All',
    'AI Research',
    'Tech News',
    'Startups',
    'Politics & Geopolitics',
    'Markets & Forex'
  ]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedCategory, setSelectedCategory] = useState('All');

  const fetchTrending = async () => {
    try {
      const trendRes = await axios.get(`${API_BASE_URL}/articles/trending`);
      if (trendRes.data) setTrending(trendRes.data);
    } catch (err) {
      console.error("Error fetching trending:", err);
    }
  };

  useEffect(() => {
    // Initial fetch of categories and trending
    const fetchInitialData = async () => {
      try {
        const catRes = await axios.get(`${API_BASE_URL}/articles/categories`);
        if (catRes.data && catRes.data.length > 0) {
          const fetchedCats = catRes.data.filter(c => c !== 'All');
          setCategories(['All', ...fetchedCats]);
        }
      } catch (err) {
        console.error("Error fetching categories:", err);
      }
      fetchTrending();
    };
    fetchInitialData();

    const intervalId = setInterval(() => {
      fetchTrending();
    }, 60000);

    return () => clearInterval(intervalId);
  }, []);

  useEffect(() => {
    fetchArticles();
    
    const intervalId = setInterval(() => {
      fetchArticles(true);
    }, 60000);

    return () => clearInterval(intervalId);
  }, [selectedCategory]);

  const fetchArticles = async (isBackground = false) => {
    if (!isBackground) {
      setLoading(true);
      setError(null);
    }
    try {
      let url = `${API_BASE_URL}/articles/`;
      if (selectedCategory !== 'All') {
        url += `?category=${encodeURIComponent(selectedCategory)}`;
      }
      const response = await axios.get(url);
      setArticles(response.data);
    } catch (err) {
      console.error("Error fetching articles:", err);
      if (!isBackground) {
        setError("Failed to load articles.");
      }
    } finally {
      if (!isBackground) {
        setLoading(false);
      }
    }
  };

  const handleCategoryClick = (cat) => {
    setSelectedCategory(cat);
    const element = document.getElementById('news-feed');
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const filteredArticles = useMemo(() => {
    if (selectedCategory === "All") return articles;
    return articles.filter(a => a.category?.toLowerCase() === selectedCategory.toLowerCase());
  }, [selectedCategory, articles]);

  return (
    <div className="app-viewport">
      <div className="custom-space-layer">
        <Starfield />
        <div className="custom-earth"></div>
      </div>
      
      <StockTicker />

      <header className="brand-overlay-centered" style={{ margin: '3rem 0 2rem 0' }}>
        <h1 className="brand-title" style={{ margin: 0 }}>INFOPULSE</h1>
        <span className="live-badge">LIVE</span>
      </header>

      <div className="content-grid">
        {/* Left Column */}
        <aside className="filter-sidebar">
          <h3 style={{ color: 'var(--primary-accent)', fontSize: '0.85rem', fontWeight: 700, letterSpacing: '0.15em', marginTop: 0, textTransform: 'uppercase', marginBottom: '1.5rem' }}>GENRES</h3>
          <div className="category-list" style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {categories.map((cat, idx) => (
              <button
                key={idx}
                className={`pill ${selectedCategory === cat ? 'active' : ''}`}
                onClick={() => handleCategoryClick(cat)}
                style={{ textAlign: 'left', width: '100%' }}
              >
                {cat}
              </button>
            ))}
          </div>
        </aside>

        {/* Center Column */}
        <main className="news-column" id="news-feed">
          <div style={{ marginBottom: '2rem', borderBottom: '1px solid rgba(134, 252, 136, 0.2)', paddingBottom: '1rem' }}>
            <h2 style={{ fontSize: '1.5rem', fontWeight: 600, margin: 0, color: 'var(--text-main)' }}>LATEST INTEL</h2>
          </div>
          
          {loading ? (
            <div className="status-message">
              <Loader2 className="spinner" size={40} />
              <p>Gathering the latest intelligence...</p>
            </div>
          ) : error ? (
            <div className="status-message" style={{ color: '#ef4444' }}>
              <AlertCircle size={40} />
              <p>{error}</p>
            </div>
          ) : filteredArticles.length === 0 ? (
            <div className="status-message">
              <p>No articles found in {selectedCategory}.</p>
            </div>
          ) : (
            <div className="articles-grid">
              {filteredArticles.map((article) => (
                <ArticleCard key={article.id} article={article} />
              ))}
            </div>
          )}
        </main>

        {/* Right Column */}
        <aside className="trending-sidebar">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
            <h3 style={{ color: 'var(--primary-accent)', fontSize: '0.85rem', fontWeight: 700, letterSpacing: '0.15em', margin: 0, textTransform: 'uppercase' }}>TRENDING NEWS</h3>
            <a href="#" style={{ color: 'var(--primary-accent)', textDecoration: 'none', fontSize: '0.75rem', fontWeight: 700 }}>SEE ALL</a>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
            {trending.length > 0 ? trending.map((item) => (
              <a 
                key={item.id} 
                href={item.url} 
                target="_blank" 
                rel="noopener noreferrer" 
                style={{ textDecoration: 'none', color: 'inherit', display: 'flex', gap: '0.75rem', alignItems: 'flex-start' }}
                onClick={() => fetch(`${API_BASE_URL}/articles/${item.id}/track?action_type=VIEW`, { method: 'POST' })}
              >
                <span style={{ display: 'inline-block', width: '6px', height: '6px', background: 'var(--primary-accent)', borderRadius: '50%', marginTop: '0.4rem', flexShrink: 0 }}></span>
                <span style={{ fontSize: '0.9rem', lineHeight: 1.4, color: 'var(--text-main)' }}>{item.title}</span>
              </a>
            )) : (
              <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>No trending news currently.</p>
            )}
          </div>
        </aside>
      </div>

      <div style={{ marginTop: '2rem' }}>
        <CurrencyWidget />
      </div>
    </div>
  );
}

export default App;
