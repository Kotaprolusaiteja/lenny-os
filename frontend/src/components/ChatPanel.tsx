import React, { useState, useRef, useEffect } from 'react';
import { Message } from '../types';
import { EmptyState } from './EmptyState';
import { MessageBubble } from './MessageBubble';

interface ChatPanelProps {
  messages: Message[];
  isLoading: boolean;
  error: string | null;
  onSendMessage: (sessionId: string, content: string) => void;
  onSelectPrompt: (prompt: string) => void;
  activeSessionId: string | null;
}

export const ChatPanel: React.FC<ChatPanelProps> = ({
  messages,
  isLoading,
  error,
  onSendMessage,
  onSelectPrompt,
  activeSessionId
}) => {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading || !activeSessionId) return;
    onSendMessage(activeSessionId, input);
    setInput('');
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="chat-panel">
      {messages.length === 0 ? (
        <EmptyState onSelectPrompt={onSelectPrompt} />
      ) : (
        <div className="messages-container">
          <div className="messages-inner">
            {messages.map((msg) => (
              <MessageBubble 
                key={msg.id} 
                message={msg} 
                onChallenge={() => {}}
                onCreatePlan={() => {}}
              />
            ))}
            
            {isLoading && (
              <div className="message-row assistant">
                <div className="message-bubble">
                  <div className="typing-indicator">
                    <div className="typing-dot"></div>
                    <div className="typing-dot"></div>
                    <div className="typing-dot"></div>
                  </div>
                </div>
              </div>
            )}
            
            {error && (
              <div style={{ color: 'red', textAlign: 'center', margin: 'var(--space-4) 0' }}>
                Error: {error}
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>
      )}

      <div className="chat-input-wrapper">
        <form className="chat-input-container" onSubmit={handleSubmit}>
          <textarea
            className="chat-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask anything about product & growth..."
            disabled={isLoading || !activeSessionId}
            rows={1}
          />
          <button 
            type="submit" 
            className="chat-send-btn"
            disabled={!input.trim() || isLoading || !activeSessionId}
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
          </button>
        </form>
      </div>
    </div>
  );
};
