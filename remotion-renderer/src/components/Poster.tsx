import React from 'react';
import { staticFile } from 'remotion';
import './Poster.css';

// Import layout components
import { QuoteCard } from './QuoteCard';
import { NextUpGrid } from './NextUpGrid';
import { StableAnnouncements } from './StableAnnouncements';
import { RaceDetailsUpdate } from './RaceDetailsUpdate';

export interface PosterProps {
  layoutType?: 'quote' | 'next_up' | 'announcement' | 'race_details';
  contextTag?: string;
  heroTitle?: string;
  columnCount?: number;
  col1Primary?: string;
  col1Sublabel?: string;
  col2Primary?: string;
  col2Sublabel?: string;
  imageSrc?: string;
  imageScale?: number;
  imageFocusX?: number;
  imageFocusY?: number;

  // Layout 1: Quote Card
  quoteText?: string;
  quoteAttribution?: string;

  // Layout 2: Next Up & Grid
  event1Date?: string;
  event1Location?: string;
  event1Detail?: string;
  event2Date?: string;
  event2Location?: string;
  event2Detail?: string;

  // Layout 3: Stable Announcements
  announcement1Title?: string;
  announcement1Desc?: string;
  announcement2Title?: string;
  announcement2Desc?: string;
  announcement3Title?: string;
  announcement3Desc?: string;

  // Layout 4: Race Details Update
  metric1Value?: string;
  metric1Label?: string;
  metric2Value?: string;
  metric2Label?: string;
  metric3Value?: string;
  metric3Label?: string;
  metric4Value?: string;
  metric4Label?: string;
  metric5Value?: string;
  metric5Label?: string;
  metric6Value?: string;
  metric6Label?: string;
}

export const Poster: React.FC<PosterProps> = ({
  layoutType = 'next_up',
  contextTag = 'NEXT UP...',
  heroTitle = 'Prudentia',
  columnCount = 2,
  col1Primary = 'MASA HASHIZUME',
  col1Sublabel = 'CONFIRMED JOCKEY',
  col2Primary = 'TE RAPA',
  col2Sublabel = 'THIS WEEKEND',
  imageSrc = '',
  imageScale = 1.0,
  imageFocusX = 50,
  imageFocusY = 50,

  // Layout 1
  quoteText,
  quoteAttribution,

  // Layout 2
  event1Date,
  event1Location,
  event1Detail,
  event2Date,
  event2Location,
  event2Detail,

  // Layout 3
  announcement1Title,
  announcement1Desc,
  announcement2Title,
  announcement2Desc,
  announcement3Title,
  announcement3Desc,

  // Layout 4
  metric1Value,
  metric1Label,
  metric2Value,
  metric2Label,
  metric3Value,
  metric3Label,
  metric4Value,
  metric4Label,
  metric5Value,
  metric5Label,
  metric6Value,
  metric6Label,
}) => {
  // Resolve image source safely for both remote URLs and local public files in headless Remotion
  const getResolvedImageSrc = (src: string) => {
    if (!src) return '';
    if (src.startsWith('http://') || src.startsWith('https://') || src.startsWith('data:')) {
      return src;
    }
    const cleanSrc = src.startsWith('/') ? src.substring(1) : src;
    return staticFile(cleanSrc);
  };

  // Render specific layout archetype contents
  const renderLayoutContent = () => {
    switch (layoutType) {
      case 'quote':
        return (
          <QuoteCard
            heroTitle={heroTitle}
            quoteText={quoteText}
            quoteAttribution={quoteAttribution}
          />
        );
      case 'announcement':
        return (
          <StableAnnouncements
            contextTag={contextTag}
            announcement1Title={announcement1Title}
            announcement1Desc={announcement1Desc}
            announcement2Title={announcement2Title}
            announcement2Desc={announcement2Desc}
            announcement3Title={announcement3Title}
            announcement3Desc={announcement3Desc}
          />
        );
      case 'race_details':
        return (
          <RaceDetailsUpdate
            contextTag={contextTag}
            heroTitle={heroTitle}
            metric1Value={metric1Value}
            metric1Label={metric1Label}
            metric2Value={metric2Value}
            metric2Label={metric2Label}
            metric3Value={metric3Value}
            metric3Label={metric3Label}
            metric4Value={metric4Value}
            metric4Label={metric4Label}
            metric5Value={metric5Value}
            metric5Label={metric5Label}
            metric6Value={metric6Value}
            metric6Label={metric6Label}
          />
        );
      case 'next_up':
      default:
        return (
          <NextUpGrid
            contextTag={contextTag}
            heroTitle={heroTitle}
            event1Date={event1Date}
            event1Location={event1Location}
            event1Detail={event1Detail}
            event2Date={event2Date}
            event2Location={event2Location}
            event2Detail={event2Detail}
            columnCount={columnCount}
            col1Primary={col1Primary}
            col1Sublabel={col1Sublabel}
            col2Primary={col2Primary}
            col2Sublabel={col2Sublabel}
          />
        );
    }
  };

  return (
    <div className="poster-canvas" id="poster-render-target">
      {/* Z-0 Stack: CSS/SVG Fractal Noise Grain Overlay */}
      <div className="grain-layer" />

      {/* Z-1: Action Lens Image Frame */}
      <div className="action-lens-wrapper">
        {imageSrc ? (
          <img 
            src={getResolvedImageSrc(imageSrc)} 
            alt="Action Lens Shot" 
            className="action-lens-image"
            style={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
              transform: `translate(-50%, -50%) scale(${imageScale})`,
              left: `${imageFocusX}%`,
              top: `${imageFocusY}%`
            }}
          />
        ) : (
          <div style={{
            width: '100%',
            height: '100%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            backgroundColor: '#000000',
            color: '#333',
            fontSize: '28px',
            fontWeight: 500
          }}>
            No Action Lens Photo
          </div>
        )}
      </div>

      {/* Z-2: Dual-Gradient Vignette & Fade Overlay */}
      <div className="vignette-overlay" />

      {/* Z-3+: Layout specific overlays */}
      {renderLayoutContent()}

      {/* Z-6: Brand Anchor (Monogram SVG in bottom-right) */}
      {layoutType !== 'announcement' && (
        <div className="brand-anchor-wrapper">
          <svg xmlns="http://www.w3.org/2000/svg" id="Layer_1" viewBox="-10.00 -10.00 127.78 114.41">
            <path d="M85.38,15.12c-1.96-2.03-4.1-3.89-6.38-5.55h0c-.87-.64-1.83-1.28-2.91-1.96h0C68.13,2.63,58.94,0,49.51,0,22.21,0,0,21.82,0,48.64c0,19.79,12.04,37.46,30.68,44.99,0,0,1.47,.59,2.37,.78l14.15-24.51,19.8,17.29L107.78,15.12h-22.4Zm-7.62,29.2l-13.67,24.16-11.69-9.3,5.72-10.28,2.43,1.12c-2.25-3.1-4.71-9.52-4.73-13.31l-25.3,43.82c-11.55-6.55-18.77-18.59-18.77-31.9-.01-20.33,16.93-36.89,37.76-36.89,7.23,0,14.26,2.01,20.34,5.82,.85,.53,1.58,1.02,2.23,1.5h0c2.31,1.68,4.42,3.63,6.28,5.78l1.76,2.03h14.26l-12.13,9.55-4.48,7.92v-.02Z" />
          </svg>
        </div>
      )}
    </div>
  );
};
