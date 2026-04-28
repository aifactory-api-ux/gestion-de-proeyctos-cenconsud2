import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { ProjectDetails } from '../src/components/ProjectDetails';
import { Project } from '../src/types/models';

const mockProject: Project = {
  id: 1,
  name: 'Project Alpha',
  description: 'First project description',
  start_date: '2024-01-01',
  end_date: '2024-12-31',
  manager_id: 1,
  status: 'active',
};

describe('ProjectDetails', () => {
  it('renders project name', () => {
    const onRequestForecast = vi.fn();
    render(<ProjectDetails project={mockProject} onRequestForecast={onRequestForecast} />);

    expect(screen.getByText('Project Alpha')).toBeDefined();
  });

  it('renders project description', () => {
    const onRequestForecast = vi.fn();
    render(<ProjectDetails project={mockProject} onRequestForecast={onRequestForecast} />);

    expect(screen.getByText('First project description')).toBeDefined();
  });

  it('renders project details', () => {
    const onRequestForecast = vi.fn();
    render(<ProjectDetails project={mockProject} onRequestForecast={onRequestForecast} />);

    expect(screen.getByText(/Start Date:/)).toBeDefined();
    expect(screen.getByText(/End Date:/)).toBeDefined();
    expect(screen.getByText(/Status:/)).toBeDefined();
    expect(screen.getByText(/Manager ID:/)).toBeDefined();
  });

  it('renders Request Forecast button', () => {
    const onRequestForecast = vi.fn();
    render(<ProjectDetails project={mockProject} onRequestForecast={onRequestForecast} />);

    const button = screen.getByRole('button', { name: /Request Forecast/i });
    expect(button).toBeDefined();
  });

  it('calls onRequestForecast when button is clicked', () => {
    const onRequestForecast = vi.fn();
    render(<ProjectDetails project={mockProject} onRequestForecast={onRequestForecast} />);

    const button = screen.getByRole('button', { name: /Request Forecast/i });
    fireEvent.click(button);
    expect(onRequestForecast).toHaveBeenCalledWith(1);
  });

  it('renders without description', () => {
    const projectNoDesc: Project = { ...mockProject, description: undefined };
    const onRequestForecast = vi.fn();
    render(<ProjectDetails project={projectNoDesc} onRequestForecast={onRequestForecast} />);

    expect(screen.getByText('Project Alpha')).toBeDefined();
  });
});
