import React, { useState } from 'react';

export const Ship30Studio: React.FC<{ onGenerate: (topic: string) => void }> = ({ onGenerate }) => {
  const [topic, setTopic] = useState('');

  return (
    <div className="ship30-studio" style={{ padding: 'var(--space-4)', borderTop: '1px solid var(--border-light)', background: 'var(--bg-primary)' }}>
      <div className="label" style={{ marginBottom: '8px' }}>SHIP 30 STUDIO</div>
      <p className="body-sm" style={{ color: 'var(--text-secondary)', marginBottom: '12px' }}>
        Generate a 30-day content plan or learning curriculum based on Lenny's archives.
      </p>
      <div style={{ display: 'flex', gap: '8px' }}>
        <input 
          type="text" 
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          placeholder="Topic (e.g. B2B Sales)"
          style={{ flex: 1, padding: '8px', border: '1px solid var(--border-light)', borderRadius: '4px' }}
        />
        <button 
          className="btn btn-primary"
          onClick={() => { if(topic) onGenerate(topic); }}
          disabled={!topic}
        >
          Generate
        </button>
      </div>
    </div>
  );
};
