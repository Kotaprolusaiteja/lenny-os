import React from 'react';

interface EmptyStateProps {
  onSelectPrompt: (prompt: string) => void;
}

const PROMPTS = [
  {
    title: 'Growth Strategy',
    icon: '📈',
    prompt: 'What does Lenny say about creating a viral loop?'
  },
  {
    title: 'Product Management',
    icon: '🎯',
    prompt: 'How to transition from IC to Product Manager?'
  },
  {
    title: 'Go-to-Market',
    icon: '🚀',
    prompt: 'Summarize best practices for launching a B2B product.'
  },
  {
    title: 'Leadership',
    icon: '🤝',
    prompt: 'What are the key traits of successful product leaders?'
  }
];

export const EmptyState: React.FC<EmptyStateProps> = ({ onSelectPrompt }) => {
  return (
    <div className="empty-state">
      <h1 className="editorial-heading display-1 empty-title">
        TURN PRODUCT{'\n'}WISDOM INTO{'\n'}YOUR NEXT MOVE.
      </h1>
      <p className="body empty-subtitle">
        Search across hundreds of episodes, get actionable insights, and turn them into execution plans instantly.
      </p>
      
      <div className="prompt-grid">
        {PROMPTS.map((item, i) => (
          <button 
            key={i} 
            className="prompt-card"
            onClick={() => onSelectPrompt(item.prompt)}
          >
            <span className="prompt-icon">{item.icon}</span>
            <span className="prompt-text">{item.title}</span>
            <span className="label" style={{ color: 'var(--text-secondary)' }}>{item.prompt}</span>
          </button>
        ))}
      </div>
    </div>
  );
};
