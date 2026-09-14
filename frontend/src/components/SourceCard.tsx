import React from 'react';
import { Source } from '../types';

export const SourceCard: React.FC<{ source: Source }> = ({ source }) => {
  return (
    <div className="source-card">
      <div className="source-card-header">
        <span className="source-guest">{source.guest || 'Lenny Rachitsky'}</span>
        <span className="source-relevance">{(source.relevance * 100).toFixed(0)}% match</span>
      </div>
      <div className="source-episode">{source.episode}</div>
      <div className="source-snippet">"{source.content_snippet}"</div>
    </div>
  );
};
