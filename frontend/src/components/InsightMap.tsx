import React from 'react';
import { InsightMap } from '../types';

export const InsightMapComp: React.FC<{ insightMap: InsightMap }> = ({ insightMap }) => {
  return (
    <div className="insight-map-card">
      <div className="label">Insight Map</div>
      <div className="insight-topic">{insightMap.topic}</div>
      
      <div className="insight-themes">
        {insightMap.themes.map((theme, i) => (
          <span key={i} className="theme-tag">{theme}</span>
        ))}
      </div>
      
      {insightMap.episodes && insightMap.episodes.length > 0 && (
        <div style={{ marginBottom: '16px', fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
          <strong>Across {insightMap.episodes.length} episodes:</strong> {insightMap.episodes.join(', ')}
        </div>
      )}
      
      <div className="insight-takeaway">
        {insightMap.takeaway}
      </div>
    </div>
  );
};
