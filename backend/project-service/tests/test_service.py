import pytest
import sys
import os
from unittest.mock import MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

sys.modules['shared.db'] = MagicMock()
sys.modules['shared.db'].get_redis_client = MagicMock(return_value=MagicMock())

import service


class TestListProjects:
    def test_list_all_projects(self):
        projects = service.list_projects()
        assert isinstance(projects, list)
        assert len(projects) == 3

    def test_project_properties(self):
        projects = service.list_projects()
        for project in projects:
            assert project.id is not None
            assert project.name is not None
            assert project.status is not None
            assert project.start_date is not None
            assert project.end_date is not None


class TestGetProjectById:
    def test_get_existing_project(self):
        project = service.get_project_by_id(1)
        assert project is not None
        assert project.id == 1
        assert project.name == "Project Alpha"
        assert project.status == "active"

    def test_get_project_2(self):
        project = service.get_project_by_id(2)
        assert project is not None
        assert project.id == 2
        assert project.name == "Project Beta"
        assert project.status == "active"

    def test_get_project_3(self):
        project = service.get_project_by_id(3)
        assert project is not None
        assert project.id == 3
        assert project.name == "Project Gamma"
        assert project.status == "planning"

    def test_get_non_existing_project(self):
        project = service.get_project_by_id(999)
        assert project is None


class TestMockProjects:
    def test_mock_projects_count(self):
        assert len(service.MOCK_PROJECTS) == 3

    def test_mock_projects_have_required_fields(self):
        for project in service.MOCK_PROJECTS:
            assert hasattr(project, 'id')
            assert hasattr(project, 'name')
            assert hasattr(project, 'description')
            assert hasattr(project, 'start_date')
            assert hasattr(project, 'end_date')
            assert hasattr(project, 'manager_id')
            assert hasattr(project, 'status')
