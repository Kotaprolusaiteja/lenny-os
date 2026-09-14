import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { Theme, KnowledgeSource } from '../types';

export const KnowledgeLibrary: React.FC<{ onClose: () => void }> = ({ onClose }) => {
  const [themes, setThemes] = useState<Theme[]>([]);
  const [sources, setSources] = useState<KnowledgeSource[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      api.getThemes().catch(() => []),
      api.getSources().catch(() => [])
    ]).then(([t, s]) => {
      setThemes(t);
      setSources(s);
      setLoading(false);
    });
  }, []);

  return (
    <div className="overlay" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h2 className="modal-title">Knowledge Library</h2>
          <button className="btn btn-ghost btn-icon" onClick={onClose}>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
          </button>
        </div>
        
        <div className="modal-body">
          {loading ? (
            <div style={{ textAlign: 'center', padding: '40px' }}><div className="spinner" style={{ margin: '0 auto' }}></div></div>
          ) : themes.length === 0 && sources.length === 0 ? (
            <div className="empty-state">
              <h3 className="h4">Knowledge base not indexed yet.</h3>
              <p className="body" style={{ color: 'var(--text-secondary)' }}>Run the backend indexing script to populate the library.</p>
            </div>
          ) : (
            <div>
              <h3 className="h4" style={{ marginBottom: '16px' }}>Indexed Themes</h3>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginBottom: '32px' }}>
                {themes.map((t, i) => (
                  <span key={i} className="theme-tag">
                    {t.name} ({t.source_count})
                  </span>
                ))}
              </div>
              
              <h3 className="h4" style={{ marginBottom: '16px' }}>Sources</h3>
              <ul style={{ listStyle: 'none', padding: 0 }}>
                {sources.map(s => (
                  <li key={s.id} style={{ padding: '12px 0', borderBottom: '1px solid var(--border-light)' }}>
                    <div style={{ fontWeight: 500 }}>{s.episode_title}</div>
                    <div className="body-sm" style={{ color: 'var(--text-secondary)' }}>
                      {s.guest && `Guest: ${s.guest} • `} {s.chunk_count} chunks indexed
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
