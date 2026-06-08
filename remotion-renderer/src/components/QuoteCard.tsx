import React from 'react';
import './Poster.css';

interface QuoteCardProps {
  heroTitle?: string;
  quoteText?: string;
  quoteAttribution?: string;
}

export const QuoteCard: React.FC<QuoteCardProps> = ({
  heroTitle = 'Prudentia',
  quoteText = "She’s a healthy mare who laps up the testing conditions. She knows the track and knows how to win there.",
  quoteAttribution = 'ANDREW SCOTT TRAINER, WEXFORD STABLES',
}) => {
  return (
    <div className="quote-card-overlay">
      {/* Top Left Editorial Header */}
      <div className="quote-hero-header">
        <div className="header-block">
          <span className="category-tag">TRAINER COMMENT</span>
          {heroTitle && <h1 className="hero-main-title">{heroTitle}</h1>}
        </div>
      </div>

      {/* Floating Translucent Glass Panel */}
      <div className="quote-floating-panel">
        <div className="quote-container">
          <p className="quote-text-body">
            “{quoteText}”
          </p>

          {quoteAttribution && (
            <div className="quote-attribution-row">
              <div className="quote-attribution-line" />
              <p className="quote-attribution">{quoteAttribution}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
