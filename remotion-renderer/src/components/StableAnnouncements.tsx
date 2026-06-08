import React from 'react';
import './Poster.css';

interface StableAnnouncementsProps {
  contextTag?: string; // Main announcement tag, e.g. "Other Stable News..."
  announcement1Title?: string;
  announcement1Desc?: string;
  announcement2Title?: string;
  announcement2Desc?: string;
  announcement3Title?: string;
  announcement3Desc?: string;
}

export const StableAnnouncements: React.FC<StableAnnouncementsProps> = ({
  contextTag = 'STABLE UPDATES...',
  announcement1Title = 'Hottathanafantasy',
  announcement1Desc = 'BACK IN TRAINING. READY FOR HER MID-WINTER CAMPAIGN "FIT, STRONG, THE ULTIMATE PROFESSIONAL" - KYLIE BAX',
  announcement2Title = 'I Stole a Manolo',
  announcement2Desc = "LISTING SOON: EXCEPTIONAL PROSPECT BY SATONO ALADDIN, SON OF DEEP IMPACT. PEDIGREE DOESN'T GET BETTER THEN THIS",
  announcement3Title = 'Turn Me Loose x Yearn Filly',
  announcement3Desc = "RECENTLY SECURED AND COMING SOON IN TRAINING AT STEPHEN GRAY RACING. IT DOESN'T GET MORE EXCITING THAN THIS.",
}) => {
  // Helpers to highlight key phrases in the description
  const highlightText = (text: string) => {
    if (!text) return '';
    
    // Highlight specific terms in luxury pale gold dynamically
    const termsToHighlight = [
      'BACK IN TRAINING',
      'MID-WINTER CAMPAIGN',
      'FIT, STRONG, THE ULTIMATE PROFESSIONAL',
      'LISTING SOON:',
      'SON OF DEEP IMPACT',
      'PEDIGREE DOESN\'T GET BETTER THEN THIS',
      'COMING SOON',
      'STEPHEN GRAY RACING',
      'IT DOESN\'T GET MORE EXCITING THAN THIS',
      'SHARES AVAILABLE'
    ];

    let highlighted = text;
    termsToHighlight.forEach(term => {
      const regex = new RegExp(`(${term})`, 'gi');
      highlighted = highlighted.replace(regex, '<strong>$1</strong>');
    });

    return <span dangerouslySetInnerHTML={{ __html: highlighted }} />;
  };

  const displayContextTag = contextTag.replace(/:/g, '...').trim() || 'STABLE NEWS...';

  return (
    <div className="announcements-overlay">
      {/* Top Left Branding & Category */}
      <div className="announcements-header">
        <div className="header-block">
          <span className="category-tag">{displayContextTag}</span>
          <h1 className="hero-main-title">Evolution Stables</h1>
        </div>
      </div>

      {/* Floating Glass Announcement Panel */}
      <div className="announcements-glass-panel">
        {/* Segment 1 */}
        {announcement1Title && (
          <div className="announcement-item">
            <h2 className="announcement-item-title">{announcement1Title}</h2>
            <p className="announcement-item-desc">{highlightText(announcement1Desc)}</p>
          </div>
        )}

        {/* Divider 1 */}
        {announcement1Title && announcement2Title && (
          <div className="announcement-item-divider" />
        )}

        {/* Segment 2 */}
        {announcement2Title && (
          <div className="announcement-item">
            <h2 className="announcement-item-title">{announcement2Title}</h2>
            <p className="announcement-item-desc">{highlightText(announcement2Desc)}</p>
          </div>
        )}

        {/* Divider 2 */}
        {announcement2Title && announcement3Title && (
          <div className="announcement-item-divider" />
        )}

        {/* Segment 3 */}
        {announcement3Title && (
          <div className="announcement-item">
            <h2 className="announcement-item-title">{announcement3Title}</h2>
            <p className="announcement-item-desc">{highlightText(announcement3Desc)}</p>
          </div>
        )}
      </div>
    </div>
  );
};
