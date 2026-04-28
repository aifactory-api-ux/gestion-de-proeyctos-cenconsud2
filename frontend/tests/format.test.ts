import { describe, it, expect } from 'vitest';
import { formatCurrency, formatDate, formatDateTime, formatPercentage } from '../src/utils/format';

describe('formatCurrency', () => {
  it('formats positive numbers correctly', () => {
    const result = formatCurrency(1000);
    expect(result).toBe('$1,000.00');
  });

  it('formats zero correctly', () => {
    const result = formatCurrency(0);
    expect(result).toBe('$0.00');
  });

  it('formats decimal numbers correctly', () => {
    const result = formatCurrency(1234.56);
    expect(result).toBe('$1,234.56');
  });
});

describe('formatDate', () => {
  it('formats date string correctly', () => {
    const result = formatDate('2024-01-15');
    expect(result).toContain('Jan');
    expect(result).toContain('15');
    expect(result).toContain('2024');
  });

  it('handles different date formats', () => {
    const result = formatDate('2024-12-25');
    expect(result).toContain('Dec');
    expect(result).toContain('25');
  });
});

describe('formatDateTime', () => {
  it('formats datetime string correctly', () => {
    const result = formatDateTime('2024-03-15T12:30:00');
    expect(result).toContain('Mar');
    expect(result).toContain('15');
    expect(result).toContain('2024');
  });
});

describe('formatPercentage', () => {
  it('formats decimal to percentage', () => {
    const result = formatPercentage(0.85);
    expect(result).toBe('85.0%');
  });

  it('formats zero correctly', () => {
    const result = formatPercentage(0);
    expect(result).toBe('0.0%');
  });

  it('formats one correctly', () => {
    const result = formatPercentage(1);
    expect(result).toBe('100.0%');
  });
});
