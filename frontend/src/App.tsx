import React, { useState, useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import { ChatPanel } from './components/ChatPanel';
import { ArtifactViewer } from './components/ArtifactViewer';
import { KnowledgeLibrary } from './components/KnowledgeLibrary';
import { StatusIndicator } from './components/StatusIndicator';
import { Ship30Studio } from './components/Ship30Studio';
import { ErrorBoundary } from './components/ErrorBoundary';
import { useSessions } from './hooks/useSessions';
import { useChat } from './hooks/useChat';
import { useHealth } from './hooks/useHealth';

function AppContent() {
  const { 
    sessions, 
    activeSessionId, 
    setActiveSessionId, 
    createSession, 
    deleteSession 
  } = useSessions();
  
  const { 
    messages, 
    isLoading: isChatLoading, 
    error: chatError, 
    currentArtifact,
    setCurrentArtifact,
    sendMessage,
    loadSession,
    clearMessages
  } = useChat();
  
  const { health } = useHealth();
  
  const [showKnowledge, setShowKnowledge] = useState(false);

  useEffect(() => {
    if (activeSessionId) {
      loadSession(activeSessionId);
    } else {
      clearMessages();
    }
  }, [activeSessionId, loadSession, clearMessages]);

  const handleNewChat = async () => {
    try {
      await createSession('New Chat');
    } catch (e) {
      console.error(e);
    }
  };

  const handleSelectPrompt = async (prompt: string) => {
    let targetSessionId = activeSessionId;
    if (!targetSessionId) {
      const session = await createSession('New Chat');
      targetSessionId = session.id;
    }
    sendMessage(targetSessionId, prompt);
  };

  return (
    <div className="app-layout">
      <Sidebar 
        sessions={sessions}
        activeSessionId={activeSessionId}
        onNewChat={handleNewChat}
        onSelectSession={setActiveSessionId}
        onDeleteSession={deleteSession}
        onShowKnowledge={() => setShowKnowledge(true)}
      />
      
      <main className="main-content">
        <div style={{ display: 'flex', flexDirection: 'column', width: '100%', height: '100%' }}>
          <header className="chat-header">
            <div style={{ fontWeight: 600 }}>Product Wisdom</div>
            <StatusIndicator health={health} />
          </header>
          
          <div style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>
            <ChatPanel 
              messages={messages}
              isLoading={isChatLoading}
              error={chatError}
              onSendMessage={sendMessage}
              onSelectPrompt={handleSelectPrompt}
              activeSessionId={activeSessionId}
            />
            
            {currentArtifact && (
              <ArtifactViewer 
                artifact={currentArtifact} 
                onClose={() => setCurrentArtifact(null)} 
              />
            )}
          </div>
        </div>
      </main>

      {showKnowledge && <KnowledgeLibrary onClose={() => setShowKnowledge(false)} />}
    </div>
  );
}

export default function App() {
  return (
    <ErrorBoundary>
      <AppContent />
    </ErrorBoundary>
  );
}
