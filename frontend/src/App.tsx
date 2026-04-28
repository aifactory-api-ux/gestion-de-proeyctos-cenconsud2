import { useState } from 'react';
import { User } from './types/models';
import { ProjectList } from './components/ProjectList';
import { ProjectDetails } from './components/ProjectDetails';
import { BudgetSummary } from './components/BudgetSummary';
import { ForecastChart } from './components/ForecastChart';
import { UserMenu } from './components/UserMenu';
import { useProjects } from './hooks/useProjects';
import { useBudget } from './hooks/useBudget';
import { useForecast } from './hooks/useForecast';

const MOCK_USER: User = {
  id: 1,
  email: 'admin@cenconsud2.com',
  full_name: 'Admin User',
  role: 'admin',
};

function App() {
  const [selectedProjectId, setSelectedProjectId] = useState<number | null>(null);
  const { projects, loading: projectsLoading, error: projectsError } = useProjects();
  const { budget, fetchBudget } = useBudget(selectedProjectId);
  const { forecast, loading: forecastLoading, error: forecastError, fetchForecast } = useForecast(selectedProjectId);

  const selectedProject = projects.find(p => p.id === selectedProjectId);

  const handleSelectProject = (id: number) => {
    setSelectedProjectId(id);
    fetchBudget(id);
  };

  const handleRequestForecast = (projectId: number) => {
    fetchForecast(projectId);
  };

  const handleLogout = () => {
    console.log('Logout clicked');
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h1>Cenconsud2 Project Management</h1>
        <UserMenu user={MOCK_USER} onLogout={handleLogout} />
      </header>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '20px' }}>
        <div>
          <h2>Projects</h2>
          {projectsLoading && <p>Loading projects...</p>}
          {projectsError && <p style={{ color: 'red' }}>{projectsError}</p>}
          <ProjectList
            projects={projects}
            onSelect={handleSelectProject}
            selectedId={selectedProjectId}
          />
        </div>

        <div>
          {selectedProject && (
            <>
              <ProjectDetails
                project={selectedProject}
                onRequestForecast={handleRequestForecast}
              />
              <BudgetSummary budget={budget} />
              {forecastLoading && <p>Loading forecast...</p>}
              {forecastError && <p style={{ color: 'red' }}>{forecastError}</p>}
              <ForecastChart forecast={forecast} />
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;