pip install parameterized

import unittest
from parameterized import parameterized
from unittest.mock import patch, MagicMock
from projectManager import ProjectManager, Priority, Status


class TestProjectManager(unittest.TestCase):

    def setUp(self):
        self.manager = ProjectManager()

    def test_create_user(self):
        self.manager.create_user("user1", "password1")
        self.assertIn("user1", self.manager.users)

    def test_create_project(self):
        self.manager.create_project("Project 1", "user1")
        self.assertIn("Project 1", self.manager.projects)

    def test_add_member_to_project(self):
        self.manager.create_project("Project 1", "user1")
        self.manager.add_member_to_project("Project 1", "user2")
        self.assertIn("user2", self.manager.projects["Project 1"].members)

    @parameterized.expand([
        ("Project 1", "Task 1", "Description 1", ["user1"], Priority.LOW, Status.BACKLOG),
        ("Project 2", "Task 2", "Description 2", ["user2"], Priority.HIGH, Status.TODO),
    ])
    def test_create_task(self, project_title, title, description, assigned_to, priority, status):
        self.manager.create_project(project_title, "admin")
        self.manager.create_task(project_title, title, description, assigned_to, priority, status)
        self.assertTrue(any(task.title == title for task in self.manager.projects[project_title].tasks))

    @patch('your_module.uuid')
    def test_create_task_unique_id(self, mock_uuid):

        mock_uuid.uuid4.return_value = '1234'
        self.manager.create_project("Project 1", "admin")
        self.manager.create_task("Project 1", "Task 1", "Description 1", ["user1"])
        self.assertEqual(self.manager.projects["Project 1"].tasks[0].id, '1234')



if __name__ == '__main__':
    unittest.main()
