import React from 'react';
import { HealthStatus } from '../types';

export const StatusIndicator: React.FC<{ health: HealthStatus | null }> = ({ health }) => {
  if (!health) {
    return (
      <div className="status-indicator">
        <div className="status-dot loading"></div>
        Connecting...
      </div>
    );
  }

  const isOnline = health.status === 'ok' && health.llm_available && health.embedding_available;
  
  return (
    <div className="status-indicator" title={`Database: ${health.database ? 'OK' : 'Error'} | Sources: ${health.indexed_sources}`}>
      <div className={`status-dot ${isOnline ? 'online' : 'offline'}`}></div>
      {health.llm_provider.toUpperCase()} · {isOnline ? 'Ready' : 'Offline'}
    </div>
  );
};
