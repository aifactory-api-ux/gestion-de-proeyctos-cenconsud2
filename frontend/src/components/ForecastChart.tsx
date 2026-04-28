import React from 'react';
import { ForecastResponse } from '../types/models';
import { formatCurrency, formatDateTime } from '../utils/format';

interface ForecastChartProps {
  forecast: ForecastResponse | null;
}

export function ForecastChart({ forecast }: ForecastChartProps) {
  if (!forecast) {
    return null;
  }

  return (
    <div style={{ padding: '15px', backgroundColor: '#f9f9f9', borderRadius: '8px', marginBottom: '15px' }}>
      <h3>Forecast Analysis</h3>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px' }}>
        <div>
          <p><strong>Project ID:</strong> {forecast.project_id}</p>
          <p><strong>Forecasted Cost:</strong> {formatCurrency(forecast.forecasted_cost)}</p>
        </div>
        <div>
          <p><strong>Confidence:</strong> {(forecast.confidence * 100).toFixed(1)}%</p>
          <p><strong>Generated:</strong> {formatDateTime(forecast.generated_at)}</p>
        </div>
      </div>
      <div style={{ marginTop: '15px' }}>
        <div style={{
          backgroundColor: '#17a2b8',
          color: 'white',
          padding: '20px',
          borderRadius: '8px',
          textAlign: 'center',
        }}>
          <p style={{ fontSize: '24px', margin: 0 }}>{formatCurrency(forecast.forecasted_cost)}</p>
          <small>Predicted Cost</small>
        </div>
      </div>
    </div>
  );
}