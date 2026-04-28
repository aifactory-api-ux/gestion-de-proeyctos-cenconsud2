import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { ForecastChart } from '../src/components/ForecastChart';
import { ForecastResponse } from '../src/types/models';

const mockForecast: ForecastResponse = {
  project_id: 1,
  forecasted_cost: 98000,
  confidence: 0.85,
  generated_at: '2024-03-15T12:00:00',
};

describe('ForecastChart', () => {
  it('renders nothing when forecast is null', () => {
    const { container } = render(<ForecastChart forecast={null} />);
    expect(container.firstChild).toBeNull();
  });

  it('renders forecast values when provided', () => {
    render(<ForecastChart forecast={mockForecast} />);

    expect(screen.getByText(/Project ID:/)).toBeDefined();
    expect(screen.getByText(/Forecasted Cost:/)).toBeDefined();
    expect(screen.getByText(/Confidence:/)).toBeDefined();
    expect(screen.getByText(/Generated:/)).toBeDefined();
  });

  it('renders Forecast Analysis heading', () => {
    render(<ForecastChart forecast={mockForecast} />);
    expect(screen.getByText('Forecast Analysis')).toBeDefined();
  });

  it('renders Predicted Cost label', () => {
    render(<ForecastChart forecast={mockForecast} />);
    expect(screen.getByText('Predicted Cost')).toBeDefined();
  });
});
