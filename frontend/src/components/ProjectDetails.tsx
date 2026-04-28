import React from 'react';
import { Project } from '../types/models';
import { formatDate } from '../utils/format';

interface ProjectDetailsProps {
  project: Project;
  onRequestForecast: (projectId: number) => void;
}

export function ProjectDetails({ project, onRequestForecast }: ProjectDetailsProps) {
  return (
    <div style={{ padding: '15px', backgroundColor: '#f9f9f9', borderRadius: '8px', marginBottom: '15px' }}>
      <h2>{project.name}</h2>
      {project.description && <p>{project.description}</p>}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
        <div>
          <strong>Start Date:</strong> {formatDate(project.start_date)}
        </div>
        <div>
          <strong>End Date:</strong> {formatDate(project.end_date)}
        </div>
        <div>
          <strong>Status:</strong> {project.status}
        </div>
        <div>
          <strong>Manager ID:</strong> {project.manager_id}
        </div>
      </div>
      <button
        onClick={() => onRequestForecast(project.id)}
        style={{
          marginTop: '15px',
          padding: '10px 20px',
          backgroundColor: '#007bff',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer',
        }}
      >
        Request Forecast
      </button>
    </div>
  );
}