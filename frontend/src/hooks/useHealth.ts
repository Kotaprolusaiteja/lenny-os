import { useState, useEffect } from 'react';
import { HealthStatus } from '../types';
import { api } from '../services/api';

export function useHealth(pollIntervalMs = 30000) {
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    let mounted = true;
    
    const checkHealth = async () => {
      try {
        const data = await api.health();
        if (mounted) {
          setHealth(data);
          setIsLoading(false);
        }
      } catch (error) {
        if (mounted) {
          setHealth(null);
          setIsLoading(false);
        }
      }
    };
    
    checkHealth();
    
    const interval = setInterval(checkHealth, pollIntervalMs);
    
    return () => {
      mounted = false;
      clearInterval(interval);
    };
  }, [pollIntervalMs]);

  return { health, isLoading };
}
