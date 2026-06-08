import React from 'react';
import './Poster.css';

interface RaceDetailsUpdateProps {
  contextTag?: string; // e.g. "RACE UPDATE STATUS..."
  heroTitle?: string;  // e.g. "Prudentia"
  metric1Value?: string; // e.g. "1ST"
  metric1Label?: string; // e.g. "PLACING"
  metric2Value?: string; // e.g. "MASA HASHIZUME"
  metric2Label?: string; // e.g. "CONFIRMED JOCKEY"
  metric3Value?: string; // e.g. "TE RAPA"
  metric3Label?: string; // e.g. "TRACK"
  metric4Value?: string; // e.g. "1200 METERS"
  metric4Label?: string; // e.g. "DISTANCE"
  metric5Value?: string; // e.g. "1:10.24"
  metric5Label?: string; // e.g. "WINNING TIME"
  metric6Value?: string; // e.g. "1.5 LENGTHS"
  metric6Label?: string; // e.g. "WINNING MARGIN"
}

export const RaceDetailsUpdate: React.FC<RaceDetailsUpdateProps> = ({
  contextTag = 'RACE UPDATE...',
  heroTitle = 'Prudentia',
  metric1Value = '1ST PLACE',
  metric1Label = 'RESULT',
  metric2Value = 'MASA HASHIZUME',
  metric2Label = 'CONFIRMED JOCKEY',
  metric3Value = 'TE RAPA',
  metric3Label = 'TRACK LOCATION',
  metric4Value = '1200 METERS',
  metric4Label = 'DISTANCE',
  metric5Value = '1:10.24',
  metric5Label = 'WINNING TIME',
  metric6Value = '1.5 LENGTHS',
  metric6Label = 'MARGIN',
}) => {
  const displayContextTag = contextTag.replace(/:/g, '...').trim() || 'RACE UPDATE...';

  // Filter out metrics that are completely empty
  const metrics = [
    { value: metric1Value, label: metric1Label },
    { value: metric2Value, label: metric2Label },
    { value: metric3Value, label: metric3Label },
    { value: metric4Value, label: metric4Label },
    { value: metric5Value, label: metric5Label },
    { value: metric6Value, label: metric6Label },
  ].filter(m => m.value && m.label);

  return (
    <div className="race-details-overlay">
      {/* Top Left Branding & Category */}
      <div className="header-block">
        <span className="category-tag">{displayContextTag}</span>
        <h1 className="hero-main-title">{heroTitle}</h1>
      </div>

      {/* Luxury Telemetry Metric Grid */}
      <div className="metrics-glass-grid">
        {metrics.map((metric, idx) => {
          const isLongValue = metric.value.length > 16;
          
          // Identify place results (e.g. 1st, Winner, Placing) for gold highlight
          const isHighlight = 
            metric.label.toUpperCase().includes('RESULT') || 
            metric.label.toUpperCase().includes('PLACE') || 
            metric.value.toUpperCase().includes('1ST') || 
            metric.value.toUpperCase().includes('WIN');
          
          return (
            <div 
              key={idx} 
              className={`metrics-cell ${isHighlight ? 'highlight-result-cell' : ''}`}
            >
              <span className="metrics-cell-label">{metric.label}</span>
              <span className={`metrics-cell-value ${isLongValue ? 'long-metric-value' : ''}`}>
                {metric.value}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
