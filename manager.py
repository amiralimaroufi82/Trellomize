class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Task:
    def __init__(self, description):
        self.description = description

class Project:
    def __init__(self, name):
        self.name = name
        self.tasks = []

class ProjectManager:
    def __init__(self):
        self.projects = []

    def create_project(self, name):
        project = Project(name)
        self.projects.append(project)

    def add_task_to_project(self, project, task_description):
        task = Task(task_description)
        project.tasks.append(task)




