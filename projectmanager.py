import json
import uuid
from enum import Enum
from typing import List, Dict, Any


class Priority(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


class Status(Enum):
    BACKLOG = 1
    TODO = 2
    DOING = 3
    DONE = 4
    ARCHIVED = 5


class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password


class Project:
    def __init__(self, title: str, creator: str):
        self.id = str(uuid.uuid4())
        self.title = title
        self.creator = creator
        self.members = [creator]
        self.tasks = []

    def add_member(self, user: str):
        self.members.append(user)

    def remove_member(self, user: str):
        if user in self.members:
            self.members.remove(user)

    def delete_project(self):
        del self


class Task:
    def __init__(self, title: str, description: str, assigned_to: List[str], priority: Priority = Priority.LOW,
                 status: Status = Status.BACKLOG):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.assigned_to = assigned_to
        self.priority = priority
        self.status = status
        self.history = []
        self.comments = []

    def assign_task(self, user: str):
        self.assigned_to.append(user)

    def unassign_task(self, user: str):
        if user in self.assigned_to:
            self.assigned_to.remove(user)

    def change_priority(self, new_priority: Priority):
        self.priority = new_priority

    def change_status(self, new_status: Status):
        self.status = new_status

    def add_comment(self, comment: str, user: str):
        self.comments.append({"user": user, "comment": comment})


class ProjectManager:
    def __init__(self):
        self.users = {}
        self.projects = {}

    def create_user(self, username: str, password: str):
        if username not in self.users:
            self.users[username] = User(username, password)

    def create_project(self, title: str, creator: str):
        if creator not in self.projects:
            self.projects[title] = Project(title, creator)

    def add_member_to_project(self, project_title: str, member: str):
        if project_title in self.projects:
            self.projects[project_title].add_member(member)

    def remove_member_from_project(self, project_title: str, member: str):
        if project_title in self.projects:
            self.projects[project_title].remove_member(member)

    def delete_project(self, project_title: str):
        if project_title in self.projects:
            del self.projects[project_title]

    def create_task(self, project_title: str, title: str, description: str, assigned_to: List[str],
                    priority: Priority = Priority.LOW, status: Status = Status.BACKLOG):
        if project_title in self.projects:
            task = Task(title, description, assigned_to, priority, status)
            self.projects[project_title].tasks.append(task)

    def assign_task_to_member(self, project_title: str, task_id: str, user: str):
        if project_title in self.projects:
            for task in self.projects[project_title].tasks:
                if task.id == task_id:
                    task.assign_task(user)

    def unassign_task_from_member(self, project_title: str, task_id: str, user: str):
        if project_title in self.projects:
            for task in self.projects[project_title].tasks:
                if task.id == task_id:
                    task.unassign_task(user)

    def change_task_priority(self, project_title: str, task_id: str, new_priority: Priority):
        if project_title in self.projects:
            for task in self.projects[project_title].tasks:
                if task.id == task_id:
                    task.change_priority(new_priority)

    def change_task_status(self, project_title: str, task_id: str, new_status: Status):
        if project_title in self.projects:
            for task in self.projects[project_title].tasks:
                if task.id == task_id:
                    task.change_status(new_status)

    def add_comment_to_task(self, project_title: str, task_id: str, comment: str, user: str):
        if project_title in self.projects:
            for task in self.projects[project_title].tasks:
                if task.id == task_id:
                    task.add_comment(comment, user)

    def view_tasks_in_project(self, project_title: str) -> List[Dict[str, Any]]:
        if project_title in self.projects:
            tasks_info = []
            for task in self.projects[project_title].tasks:
                tasks_info.append({
                    "Task ID": task.id,
                    "Title": task.title,
                    "Description": task.description,
                    "Priority": task.priority.name,
                    "Status": task.status.name
                })
            return tasks_info

    def view_task_details(self, project_title: str, task_id: str) -> Dict[str, Any]:
        if project_title in self.projects:
            for task in self.projects[project_title].tasks:
                if task.id == task_id:
                    return {
                        "Task ID": task.id,
                        "Title": task.title,
                        "Description": task.description,
                        "Assigned To": task.assigned_to,
                        "Priority": task.priority.name,
                        "Status": task.status.name,
                        "Comments": task.comments
                    }

    def save_data(self):
        with open("users.json", "w") as users_file:
            json.dump({user.username: user.password for user in self.users.values()}, users_file, indent=4)

        with open("projects.json", "w") as projects_file:
            projects_data = {}
            for title, project in self.projects.items():
                projects_data[title] = {
                    "creator": project.creator,
                    "members": project.members,
                    "tasks": [{task.id: {
                        "title": task.title,
                        "description": task.description,
                        "assigned_to": task.assigned_to,
                        "priority": task.priority.name,
                        "status": task.status.name,
                        "comments": task.comments
                    }} for task in project.tasks]
                }
            json.dump(projects_data, projects_file, indent=4)

    """def delete_all(self):
        confirmation = input("Are you sure you want to delete all data? (yes/no): ")
        if confirmation.lower() == "yes":
            self.users = {}
            self.projects = {}
            print("All data has been deleted.")
        else:
            print("Operation canceled.")"""
    """manager.delete_all"""


manager = ProjectManager()
manager.create_user("amirali", "amirali1382")
manager.create_user("hossein", "hossein1900")
manager.create_project("Pr1", "amirali")
manager.create_task("Pr1", "Task 1", "Description 1", ["hossein"])
manager.save_data()
#print("Project Title:", project.title)
#print("Project Members:", [member.username for member in project.members])
#print("Tasks in Project:")
#for task in project.tasks:
       # print("Task Title:", task.title)
       # print("Task Assignees:", [assignee.username for assignee in task.assignees])
        #print("Task Status:", task.status.name)
        #print("Task Comments:", [f"{comment[1]}: {comment[0]}" for comment in task.comments])
        #print()
