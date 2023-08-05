import pytest

from mambas.server import models
from mambas.server import views


class TestBaseView():

    def test_set_navigation_projects(self):
        projects = [models.Project(1, "Project1", 0, "token")]
        base_view = views.BaseView()
        base_view.set_navigation_projects(projects)
        assert base_view.view_model["navigation_projects"][0]["id"] == 1
        assert base_view.view_model["navigation_projects"][0]["name"] == "Project1"


if __name__ == "__main__":
    pytest.main([__file__])
