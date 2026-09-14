export interface Source {
  episode: string;
  guest: string;
  source: string;
  relevance: number;
  content_snippet: string;
}

export interface Artifact {
  id: string;
  type: 'markdown' | 'html';
  title: string;
  content: string;
  created_at: string;
}

export interface WisdomAction {
  evidence_suggests: string;
  what_it_means: string;
  what_to_do_next: string;
}

export interface InsightMap {
  topic: string;
  themes: string[];
  episodes: string[];
  takeaway: string;
}

export interface ChatMetadata {
  retrieval_count: number;
  source_count: number;
  latency_ms: number;
  chunks_retrieved: number;
  provider: string;
  model: string;
}

export interface ChatResponse {
  answer: string;
  sources: Source[];
  provider: string;
  model: string;
  metadata: ChatMetadata;
  artifact?: Artifact;
  wisdom_action?: WisdomAction;
  insight_map?: InsightMap;
}

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: Source[];
  metadata?: ChatMetadata;
  artifact?: Artifact;
  wisdom_action?: WisdomAction;
  insight_map?: InsightMap;
  created_at: string;
}

export interface Session {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
  message_count: number;
}

export interface SessionDetail {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
  messages: Message[];
}

export interface HealthStatus {
  status: string;
  database: boolean;
  llm_provider: string;
  llm_available: boolean;
  embedding_available: boolean;
  indexed_sources: number;
  indexed_chunks: number;
}

export interface Theme {
  name: string;
  description: string;
  source_count: number;
}

export interface KnowledgeSource {
  id: string;
  episode_title: string;
  guest?: string;
  episode_number?: number;
  source_url?: string;
  date?: string;
  chunk_count: number;
}

export interface AppError {
  error: {
    code: string;
    message: string;
  };
}
