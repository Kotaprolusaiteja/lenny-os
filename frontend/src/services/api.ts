import { Session, SessionDetail, ChatResponse, HealthStatus, Theme, KnowledgeSource } from '../types';

const API_BASE = '/api';

async function fetchApi<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  });
  
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.message || errorData.error?.message || `API Error: ${response.status}`);
  }
  
  return response.json();
}

export const api = {
  health: () => fetchApi<HealthStatus>('/health'),
  
  createSession: (title?: string) => 
    fetchApi<Session>('/sessions', { 
      method: 'POST', 
      body: JSON.stringify({ title }) 
    }),
    
  getSessions: () => fetchApi<Session[]>('/sessions'),
  
  getSession: (id: string) => fetchApi<SessionDetail>(`/sessions/${id}`),
  
  deleteSession: (id: string) => 
    fetchApi<void>(`/sessions/${id}`, { method: 'DELETE' }),
    
  chat: (sessionId: string, content: string) => 
    fetchApi<ChatResponse>(`/chat`, {
      method: 'POST',
      body: JSON.stringify({ session_id: sessionId, message: content })
    }),
    
  getThemes: () => fetchApi<Theme[]>('/knowledge/themes'),
  
  getSources: () => fetchApi<KnowledgeSource[]>('/knowledge/sources'),
};
