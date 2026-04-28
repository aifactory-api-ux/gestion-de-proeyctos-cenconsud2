import api from './client';
import { ForecastRequest, ForecastResponse } from '../types/models';

export async function getForecast(request: ForecastRequest): Promise<ForecastResponse> {
  const response = await api.post<ForecastResponse>('/forecast', request);
  return response.data;
}