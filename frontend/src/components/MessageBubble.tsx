import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Message } from '../types';
import { SourceCard } from './SourceCard';
import { TransparencyCard } from './TransparencyCard';
import { WisdomAction } from './WisdomAction';
import { InsightMapComp } from './InsightMap';
import { ChallengeThinking } from './ChallengeThinking';

interface MessageBubbleProps {
  message: Message;
  onChallenge: () => void;
  onCreatePlan: () => void;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({
  message,
  onChallenge,
  onCreatePlan
}) => {
  const isUser = message.role === 'user';

  return (
    <div className={`message-row ${isUser ? 'user' : 'assistant'}`}>
      <div className="message-bubble">
        {isUser ? (
          <div>{message.content}</div>
        ) : (
          <>
            <div className="markdown-content">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {message.content}
              </ReactMarkdown>
            </div>
            
            <div className="meta-cards-container">
              {message.sources && message.sources.length > 0 && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                  <div className="label">Sources</div>
                  {message.sources.map((src, i) => (
                    <SourceCard key={i} source={src} />
                  ))}
                </div>
              )}

              {message.insight_map && (
                <div style={{ marginTop: '16px' }}>
                  <InsightMapComp insightMap={message.insight_map} />
                </div>
              )}

              {message.wisdom_action && (
                <div style={{ marginTop: '16px' }}>
                  <WisdomAction wisdomAction={message.wisdom_action} onCreatePlan={onCreatePlan} />
                </div>
              )}

              {message.metadata && (
                <div style={{ marginTop: '16px' }}>
                  <TransparencyCard metadata={message.metadata} />
                </div>
              )}
              
              <div style={{ marginTop: '16px' }}>
                <ChallengeThinking onChallenge={onChallenge} />
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};
