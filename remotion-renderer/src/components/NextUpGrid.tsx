import React from 'react';
import './Poster.css';

interface NextUpGridProps {
  contextTag?: string;
  heroTitle?: string;
  // Event 1 details
  event1Date?: string;
  event1Location?: string;
  event1Detail?: string;
  // Event 2 details (Optional)
  event2Date?: string;
  event2Location?: string;
  event2Detail?: string;
  // Fallbacks for traditional single-race layout
  columnCount?: number;
  col1Primary?: string;
  col1Sublabel?: string;
  col2Primary?: string;
  col2Sublabel?: string;
}

export const NextUpGrid: React.FC<NextUpGridProps> = ({
  contextTag = 'NEXT UP...',
  heroTitle = 'Prudentia',
  event1Date,
  event1Location,
  event1Detail,
  event2Date,
  event2Location,
  event2Detail,
  columnCount = 2,
  col1Primary = 'MASA HASHIZUME',
  col1Sublabel = 'CONFIRMED JOCKEY',
  col2Primary = 'TE RAPA',
  col2Sublabel = 'THIS WEEKEND',
}) => {
  // Determine if we should show the multi-event schedule or the single-event telemetry
  const isMultiEvent = Boolean(event1Date && event1Location);
  const displayContextTag = contextTag.replace(/:/g, '...').trim() || 'NEXT UP...';

  return (
    <div className="next-up-overlay">
      {/* Top Left Branding & Category */}
      <div className="header-block">
        <span className="category-tag">{displayContextTag}</span>
        <h1 className="hero-main-title">{heroTitle}</h1>
      </div>

      {isMultiEvent ? (
        /* Layout 2B: Multi-Event Glass Card (Right-aligned Schedule) */
        <div className="multi-event-card">
          {/* Event 1 */}
          <div className="event-row">
            <div className="event-date-text">{event1Date}</div>
            <div className="event-details-meta">
              <span className="event-track">{event1Location}</span>
              {event1Detail && (
                <>
                  <span className="event-separator">|</span>
                  <span className="event-desc">{event1Detail}</span>
                </>
              )}
            </div>
          </div>

          {/* Elegant row divider line if there's a second event */}
          {event2Date && <div className="event-row-divider" />}

          {/* Event 2 */}
          {event2Date && (
            <div className="event-row">
              <div className="event-date-text">{event2Date}</div>
              <div className="event-details-meta">
                <span className="event-track">{event2Location}</span>
                {event2Detail && (
                  <>
                    <span className="event-separator">|</span>
                    <span className="event-desc">{event2Detail}</span>
                  </>
                )}
              </div>
            </div>
          )}
        </div>
      ) : (
        /* Layout 2A: Classic Single-Event Slender Telemetry Bar (Bottom horizontal block) */
        <div className="classic-telemetry-bar">
          {/* Column 1 */}
          <div className="telemetry-col">
            <div className="telemetry-primary">{col1Primary}</div>
            <div className="telemetry-sublabel">{col1Sublabel}</div>
          </div>

          {/* Column 2 */}
          {columnCount === 2 && col2Primary && (
            <div className="telemetry-col">
              <div className="telemetry-primary">{col2Primary}</div>
              <div className="telemetry-sublabel">{col2Sublabel}</div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
