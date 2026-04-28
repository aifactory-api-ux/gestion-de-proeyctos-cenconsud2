import { Budget } from '../types/models';
import { formatCurrency, formatDateTime } from '../utils/format';

interface BudgetSummaryProps {
  budget: Budget | null;
}

export function BudgetSummary({ budget }: BudgetSummaryProps) {
  if (!budget) {
    return <p>No budget data available.</p>;
  }

  const spentPercentage = (budget.spent_amount / budget.allocated_amount) * 100;
  const forecastPercentage = (budget.forecasted_amount / budget.allocated_amount) * 100;

  return (
    <div style={{ padding: '15px', backgroundColor: '#f9f9f9', borderRadius: '8px', marginBottom: '15px' }}>
      <h3>Budget Summary</h3>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px' }}>
        <div>
          <p><strong>Allocated:</strong> {formatCurrency(budget.allocated_amount)}</p>
          <p><strong>Spent:</strong> {formatCurrency(budget.spent_amount)}</p>
          <p><strong>Forecasted:</strong> {formatCurrency(budget.forecasted_amount)}</p>
        </div>
        <div>
          <p><strong>Spent %:</strong> {spentPercentage.toFixed(1)}%</p>
          <p><strong>Forecast %:</strong> {forecastPercentage.toFixed(1)}%</p>
          <p><strong>Last Updated:</strong> {formatDateTime(budget.last_updated)}</p>
        </div>
      </div>
      <div style={{ marginTop: '10px' }}>
        <div style={{ backgroundColor: '#e0e0e0', borderRadius: '4px', height: '20px', position: 'relative' }}>
          <div
            style={{
              backgroundColor: '#28a745',
              height: '100%',
              borderRadius: '4px',
              width: `${Math.min(spentPercentage, 100)}%`,
            }}
          />
        </div>
        <small>Spent vs Allocated</small>
      </div>
    </div>
  );
}