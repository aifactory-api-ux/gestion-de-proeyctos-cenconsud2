import { useState, useEffect, useCallback } from 'react';
import { getForecast } from '../api/forecast';
import { ForecastRequest, ForecastResponse } from '../types/models';

export function useForecast(projectId: number | null) {
  const [forecast, setForecast] = useState<ForecastResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchForecast = useCallback(async (id: number) => {
    setLoading(true);
    setError(null);
    try {
      const request: ForecastRequest = { project_id: id };
      const response = await getForecast(request);
      setForecast(response);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch forecast');
      setForecast(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    setForecast(null);
  }, [projectId]);

  return { forecast, loading, error, fetchForecast };
}