import { useState, useCallback, useEffect } from 'react';
import { Session } from '../types';
import { api } from '../services/api';

export function useSessions() {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const loadSessions = useCallback(async () => {
    setIsLoading(true);
    try {
      const data = await api.getSessions();
      setSessions(data || []);
      if (data.length > 0 && !activeSessionId) {
        setActiveSessionId(data[0].id);
      }
    } catch (error) {
      console.error('Failed to load sessions', error);
    } finally {
      setIsLoading(false);
    }
  }, [activeSessionId]);

  useEffect(() => {
    loadSessions();
  }, [loadSessions]);

  const createSession = useCallback(async (title?: string) => {
    try {
      const newSession = await api.createSession(title);
      setSessions(prev => [newSession, ...prev]);
      setActiveSessionId(newSession.id);
      return newSession;
    } catch (error) {
      console.error('Failed to create session', error);
      throw error;
    }
  }, []);

  const deleteSession = useCallback(async (id: string) => {
    try {
      await api.deleteSession(id);
      setSessions(prev => prev.filter(s => s.id !== id));
      if (activeSessionId === id) {
        setActiveSessionId(null);
      }
    } catch (error) {
      console.error('Failed to delete session', error);
    }
  }, [activeSessionId]);

  return {
    sessions,
    activeSessionId,
    setActiveSessionId,
    isLoading,
    loadSessions,
    createSession,
    deleteSession
  };
}
