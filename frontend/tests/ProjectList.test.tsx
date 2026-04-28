import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { ProjectList } from '../src/components/ProjectList';
import { Project } from '../src/types/models';

const mockProjects: Project[] = [
  {
    id: 1,
    name: 'Project Alpha',
    description: 'First project',
    start_date: '2024-01-01',
    end_date: '2024-12-31',
    manager_id: 1,
    status: 'active',
  },
  {
    id: 2,
    name: 'Project Beta',
    description: 'Second project',
    start_date: '2024-03-01',
    end_date: '2024-09-30',
    manager_id: 2,
    status: 'active',
  },
];

describe('ProjectList', () => {
  it('renders empty message when no projects', () => {
    const onSelect = vi.fn();
    render(<ProjectList projects={[]} onSelect={onSelect} selectedId={null} />);

    expect(screen.getByText('No projects available.')).toBeDefined();
  });

  it('renders list of projects', () => {
    const onSelect = vi.fn();
    render(<ProjectList projects={mockProjects} onSelect={onSelect} selectedId={null} />);

    expect(screen.getByText('Project Alpha')).toBeDefined();
    expect(screen.getByText('Project Beta')).toBeDefined();
  });

  it('calls onSelect when project is clicked', () => {
    const onSelect = vi.fn();
    render(<ProjectList projects={mockProjects} onSelect={onSelect} selectedId={null} />);

    const firstProject = screen.getByText('Project Alpha');
    fireEvent.click(firstProject);
    expect(onSelect).toHaveBeenCalledWith(1);
  });

  it('renders project status', () => {
    const onSelect = vi.fn();
    render(<ProjectList projects={mockProjects} onSelect={onSelect} selectedId={null} />);

    const statusElements = screen.getAllByText(/Status: active/);
    expect(statusElements.length).toBe(2);
  });
});
