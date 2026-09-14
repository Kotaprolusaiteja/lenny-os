import React, { useState } from 'react';
import { ChatMetadata } from '../types';

export const TransparencyCard: React.FC<{ metadata: ChatMetadata }> = ({ metadata }) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="transparency-card">
      <div className="transparency-header" onClick={() => setIsOpen(!isOpen)}>
        <span className="transparency-title">HOW THIS ANSWER WAS BUILT</span>
        <span>{isOpen ? '−' : '+'}</span>
      </div>
      {isOpen && (
        <div className="transparency-content">
          <div className="transparency-item">
            <span className="transparency-icon">✓</span>
            <span>{metadata.retrieval_count} items retrieved</span>
          </div>
          <div className="transparency-item">
            <span className="transparency-icon">✓</span>
            <span>{metadata.source_count} sources used</span>
          </div>
          <div className="transparency-item">
            <span className="transparency-icon">✓</span>
            <span>{metadata.chunks_retrieved} chunks processed</span>
          </div>
          <div className="transparency-item">
            <span className="transparency-icon">✓</span>
            <span>Provider: {metadata.provider}</span>
          </div>
          <div className="transparency-item">
            <span className="transparency-icon">✓</span>
            <span>Model: {metadata.model}</span>
          </div>
          <div className="transparency-item">
            <span className="transparency-icon">✓</span>
            <span>Latency: {metadata.latency_ms}ms</span>
          </div>
        </div>
      )}
    </div>
  );
};
