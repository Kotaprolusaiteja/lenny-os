import { useState, useCallback } from 'react';
import { Message, Artifact } from '../types';
import { api } from '../services/api';

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentArtifact, setCurrentArtifact] = useState<Artifact | null>(null);

  const loadSession = useCallback(async (sessionId: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const session = await api.getSession(sessionId);
      setMessages(session.messages || []);
      
      // Find latest artifact if exists
      const latestWithArtifact = [...(session.messages || [])].reverse().find(m => m.artifact);
      if (latestWithArtifact?.artifact) {
        setCurrentArtifact(latestWithArtifact.artifact);
      } else {
        setCurrentArtifact(null);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load session');
    } finally {
      setIsLoading(false);
    }
  }, []);

  const sendMessage = useCallback(async (sessionId: string, content: string) => {
    if (!content.trim()) return;
    
    const tempUserMsg: Message = {
      id: Date.now().toString(),
      role: 'user',
      content,
      created_at: new Date().toISOString()
    };
    
    setMessages(prev => [...prev, tempUserMsg]);
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await api.chat(sessionId, content);
      
      const assistantMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.answer,
        sources: response.sources,
        metadata: response.metadata,
        artifact: response.artifact,
        wisdom_action: response.wisdom_action,
        insight_map: response.insight_map,
        created_at: new Date().toISOString()
      };
      
      setMessages(prev => [...prev, assistantMsg]);
      
      if (response.artifact) {
        setCurrentArtifact(response.artifact);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to send message');
      // Optionally remove temp message here
    } finally {
      setIsLoading(false);
    }
  }, []);

  const clearMessages = useCallback(() => {
    setMessages([]);
    setCurrentArtifact(null);
    setError(null);
  }, []);

  return {
    messages,
    isLoading,
    error,
    currentArtifact,
    setCurrentArtifact,
    sendMessage,
    loadSession,
    clearMessages
  };
}
