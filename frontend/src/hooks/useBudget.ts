import { useState, useEffect, useCallback } from 'react';
import api from '../api/client';
import { Budget } from '../types/models';

export function useBudget(projectId: number | null) {
  const [budget, setBudget] = useState<Budget | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchBudget = useCallback(async (id: number) => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get<Budget>(`/budgets/${id}`);
      setBudget(response.data);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch budget');
      setBudget(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (projectId !== null) {
      fetchBudget(projectId);
    } else {
      setBudget(null);
    }
  }, [projectId, fetchBudget]);

  return { budget, loading, error, fetchBudget };
}