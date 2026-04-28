import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BudgetSummary } from '../src/components/BudgetSummary';
import { Budget } from '../src/types/models';

const mockBudget: Budget = {
  id: 1,
  project_id: 1,
  allocated_amount: 100000,
  spent_amount: 45000,
  forecasted_amount: 95000,
  last_updated: '2024-03-15T10:30:00',
};

describe('BudgetSummary', () => {
  it('renders no budget message when budget is null', () => {
    render(<BudgetSummary budget={null} />);
    expect(screen.getByText('No budget data available.')).toBeDefined();
  });

  it('renders budget values', () => {
    render(<BudgetSummary budget={mockBudget} />);

    expect(screen.getByText(/Allocated:/)).toBeDefined();
    expect(screen.getByText(/Spent:/)).toBeDefined();
    expect(screen.getByText(/Forecasted:/)).toBeDefined();
  });

  it('renders Budget Summary heading', () => {
    render(<BudgetSummary budget={mockBudget} />);
    expect(screen.getByText('Budget Summary')).toBeDefined();
  });

  it('renders spent and forecast percentages', () => {
    render(<BudgetSummary budget={mockBudget} />);

    expect(screen.getByText(/Spent %:/)).toBeDefined();
    expect(screen.getByText(/Forecast %:/)).toBeDefined();
  });

  it('renders last updated label', () => {
    render(<BudgetSummary budget={mockBudget} />);
    expect(screen.getByText(/Last Updated:/)).toBeDefined();
  });
});
