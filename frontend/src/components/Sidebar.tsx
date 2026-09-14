import React from 'react';
import { Session } from '../types';
import { cn } from '../lib/utils';

interface SidebarProps {
  sessions: Session[];
  activeSessionId: string | null;
  onNewChat: () => void;
  onSelectSession: (id: string) => void;
  onDeleteSession: (id: string) => void;
  onShowKnowledge: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  sessions,
  activeSessionId,
  onNewChat,
  onSelectSession,
  onDeleteSession,
  onShowKnowledge
}) => {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="sidebar-brand">
          <span style={{ color: 'var(--accent)' }}>✦</span>
          LENNY OS
        </div>
        <button 
          className="btn btn-primary" 
          style={{ width: '100%', justifyContent: 'flex-start' }}
          onClick={onNewChat}
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
          New Chat
        </button>
      </div>
      
      <div className="sidebar-content">
        <div className="label" style={{ margin: 'var(--space-4) var(--space-3) var(--space-2)' }}>Recent Sessions</div>
        
        {sessions.map(session => (
          <div 
            key={session.id} 
            className={cn('session-item', activeSessionId === session.id && 'active')}
            onClick={() => onSelectSession(session.id)}
          >
            <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
              {session.title || 'New Chat'}
            </span>
            <button 
              className="btn btn-ghost-inverse btn-icon delete-btn"
              onClick={(e) => {
                e.stopPropagation();
                onDeleteSession(session.id);
              }}
              title="Delete session"
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
            </button>
          </div>
        ))}
      </div>
      
      <div className="sidebar-footer">
        <button 
          className="btn btn-ghost-inverse" 
          style={{ width: '100%', justifyContent: 'flex-start' }}
          onClick={onShowKnowledge}
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>
          Knowledge Library
        </button>
      </div>
    </aside>
  );
};
