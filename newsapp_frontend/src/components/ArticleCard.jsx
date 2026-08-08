import React, { useState } from 'react';
import { ChevronDown, ChevronUp, ExternalLink, Image as ImageIcon } from 'lucide-react';

const ArticleCard = ({ article }) => {
  const [expanded, setExpanded] = useState(false);
  const [imageError, setImageError] = useState(false);

  const handleImageError = (e) => {
    if (!imageError) {
      setImageError(true);
      e.target.src = `https://picsum.photos/seed/${article.id}/800/450`;
    }
  };

  const handleAccordionClick = () => {
    if (!expanded) {
      fetch(`http://127.0.0.1:8000/articles/${article.id}/track?action_type=READ`, { method: 'POST' }).catch(err => console.error(err));
    }
    setExpanded(!expanded);
  };

  // Fallbacks if data is missing
  const title = article.title || 'Untitled Article';
  const sourceName = article.source || 'TECH NEWS';
  const dateStr = article.published_at ? new Date(article.published_at).toLocaleDateString(undefined, {
    year: 'numeric', month: 'short', day: 'numeric'
  }) : 'Unknown Date';
  
  const summary = article.summary || '';
  const eli5 = article.eli5_summary || article.summary || 'No ELI5 summary available.';

  return (
    <article className="article-card">
      <div className="article-image-container">
        <img 
          src={article.image_url || `https://picsum.photos/seed/${article.id}/800/450`} 
          alt={title} 
          className="article-image" 
          onError={handleImageError} 
        />
      </div>

      <div className="article-content">
        <div className="card-header">
        <span className="source-badge">{sourceName}</span>
        <span className="publish-date">{dateStr}</span>
      </div>
      
      <h3 className="article-title">
        <a 
          href={article.url} 
          target="_blank" 
          rel="noopener noreferrer" 
          className="article-title-link"
          onClick={() => fetch(`http://127.0.0.1:8000/articles/${article.id}/track?action_type=VIEW`, { method: 'POST' }).catch(err => console.error(err))}
        >
          {title}
        </a>
      </h3>
      
      {summary && (
        <div className="summary-text" style={{ marginBottom: '1rem', color: '#94a3b8' }}>
          {summary}
        </div>
      )}
      
      <div className="accordion">
        <div 
          className="accordion-header"
          onClick={handleAccordionClick}
        >
          <span>ELI5 Summary</span>
          {expanded ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
        </div>
        <div className={`accordion-content ${expanded ? 'expanded' : ''}`}>
          <div className="eli5-text">
            {eli5.split('\n').map((line, idx) => (
              <div key={idx}>{line}</div>
            ))}
          </div>
        </div>
      </div>
      </div>
    </article>
  );
};

export default ArticleCard;
