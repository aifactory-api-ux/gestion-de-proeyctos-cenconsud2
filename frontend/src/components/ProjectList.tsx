import React from 'react';
import { Project } from '../types/models';
import { formatDate } from '../utils/format';

interface ProjectListProps {
  projects: Project[];
  onSelect: (id: number) => void;
  selectedId: number | null;
}

export function ProjectList({ projects, onSelect, selectedId }: ProjectListProps) {
  if (projects.length === 0) {
    return <p>No projects available.</p>;
  }

  return (
    <ul style={{ listStyle: 'none', padding: 0 }}>
      {projects.map(project => (
        <li
          key={project.id}
          onClick={() => onSelect(project.id)}
          style={{
            padding: '10px',
            marginBottom: '5px',
            cursor: 'pointer',
            backgroundColor: selectedId === project.id ? '#e0e0e0' : '#f5f5f5',
            borderRadius: '4px',
            border: selectedId === project.id ? '2px solid #007bff' : '1px solid #ddd',
          }}
        >
          <strong>{project.name}</strong>
          <br />
          <small>Status: {project.status}</small>
          <br />
          <small>Duration: {formatDate(project.start_date)} - {formatDate(project.end_date)}</small>
        </li>
      ))}
    </ul>
  );
}