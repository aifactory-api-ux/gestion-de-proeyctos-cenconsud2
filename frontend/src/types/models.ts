export interface Project {
  id: number;
  name: string;
  description?: string;
  start_date: string;
  end_date: string;
  manager_id: number;
  status: string;
}

export interface Budget {
  id: number;
  project_id: number;
  allocated_amount: number;
  spent_amount: number;
  forecasted_amount: number;
  last_updated: string;
}

export interface ForecastRequest {
  project_id: number;
}

export interface ForecastResponse {
  project_id: number;
  forecasted_cost: number;
  confidence: number;
  generated_at: string;
}

export interface User {
  id: number;
  email: string;
  full_name: string;
  role: string;
}

export interface ErrorResponse {
  detail: string;
}