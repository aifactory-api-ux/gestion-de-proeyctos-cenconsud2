import { useState, useEffect, useCallback } from 'react';
import api from '../api/client';
import { Project } from '../types/models';

export function useProjects() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchProjects = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get<Project[]>('/projects');
      setProjects(response.data);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch projects');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchProjects();
  }, [fetchProjects]);

  const getProject = (id: number): Project | undefined => {
    return projects.find(p => p.id === id);
  };

  return { projects, loading, error, fetchProjects, getProject };
}