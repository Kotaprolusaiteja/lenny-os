import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Artifact } from '../types';

interface Props {
  artifact: Artifact;
  onClose: () => void;
}

export const ArtifactViewer: React.FC<Props> = ({ artifact, onClose }) => {
  const [tab, setTab] = useState<'preview' | 'markdown' | 'html'>('preview');

  return (
    <div className="artifact-panel">
      <div className="artifact-header">
        <div className="artifact-title">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
          {artifact.title}
        </div>
        
        <div className="artifact-tabs">
          <button 
            className={`artifact-tab ${tab === 'preview' ? 'active' : ''}`}
            onClick={() => setTab('preview')}
          >
            Preview
          </button>
          <button 
            className={`artifact-tab ${tab === 'markdown' ? 'active' : ''}`}
            onClick={() => setTab('markdown')}
          >
            {artifact.type === 'html' ? 'Code' : 'Markdown'}
          </button>
          {artifact.type === 'html' && (
            <button 
              className={`artifact-tab ${tab === 'html' ? 'active' : ''}`}
              onClick={() => setTab('html')}
            >
              Result
            </button>
          )}
        </div>
        
        <button className="btn btn-ghost btn-icon" onClick={onClose}>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
        </button>
      </div>
      
      <div className="artifact-content">
        {tab === 'preview' && (
          <div className="artifact-preview markdown-content">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {artifact.content}
            </ReactMarkdown>
          </div>
        )}
        
        {tab === 'markdown' && (
          <pre className="artifact-code">
            {artifact.content}
          </pre>
        )}
        
        {tab === 'html' && artifact.type === 'html' && (
          <iframe 
            srcDoc={artifact.content}
            title={artifact.title}
            className="artifact-iframe"
            sandbox="allow-scripts"
          />
        )}
      </div>
    </div>
  );
};
