import json
import re
import uuid
import logging
from enum import Enum
from typing import List, Dict, Any
import manager as ma

logging.basicConfig( filename='project.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email
        try:
            if not self.is_valid_email(email):
                raise ValueError("Invalid email address")
            logging.info(f'Created user: {username}')
        except Exception as e:
            logging.error(f'Error creating user {username}: {e}')

    
    def is_valid_email(email: str) -> bool:
        email_regex = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")
        return re.match(email_regex, email) is not None

class Project:
    def __init__(self, title: str, creator: str):
        try:
            self.id = str(uuid.uuid4())
            self.title = title
            self.creator = creator
            self.members = [creator]
            self.tasks = []
            logging.info(f'Created project: {title} by {creator}')
        except Exception as e:
            logging.error(f'Error creating project {title}: {e}')

    def add_member(self, user: str):
        try:
            self.members.append(user)
            logging.info(f'Added member: {user} to project: {self.title}')
        except Exception as e:
            logging.error(f'Error adding member {user} to project {self.title}: {e}')

    def remove_member(self, user: str):
        try:
            if user in self.members:
                self.members.remove(user)
                logging.info(f'Removed member: {user} from project: {self.title}')
        except Exception as e:
            logging.error(f'Error removing member {user} from project {self.title}: {e}')

    def delete_project(self):
        try:
            logging.info(f'Deleting project: {self.title}')
            del self
        except Exception as e:
            logging.error(f'Error deleting project {self.title}: {e}')

class Task:
    def __init__(self, title: str, description: str, assigned_to: List[str], priority: Priority = Priority.LOW,
                 status: Status = Status.BACKLOG):
        try:
            self.id = str(uuid.uuid4())
            self.title = title
            self.description = description
            self.assigned_to = assigned_to
            self.priority = priority
            self.status = status
            self.history = []
            self.comments = []
            logging.info(f'Created task: {title} with ID: {self.id} in status: {status.name} and priority: {priority.name}')
        except Exception as e:
            logging.error(f'Error creating task {title}: {e}')

    def assign_task(self, user: str):
        try:
            self.assigned_to.append(user)
            logging.info(f'Assigned task: {self.title} to user: {user}')
        except Exception as e:
            logging.error(f'Error assigning task {self.title} to user {user}: {e}')

    def unassign_task(self, user: str):
        try:
            if user in self.assigned_to:
                self.assigned_to.remove(user)
                logging.info(f'Unassigned task: {self.title} from user: {user}')
        except Exception as e:
            logging.error(f'Error unassigning task {self.title} from user {user}: {e}')

    def change_priority(self, new_priority: Priority):
        try:
            logging.info(f'Changing priority of task: {self.title} from {self.priority.name} to {new_priority.name}')
            self.priority = new_priority
        except Exception as e:
            logging.error(f'Error changing priority of task {self.title}: {e}')

    def change_status(self, new_status: Status):
        try:
            logging.info(f'Changing status of task: {self.title} from {self.status.name} to {new_status.name}')
            self.status = new_status
        except Exception as e:
            logging.error(f'Error changing status of task {self.title}: {e}')

    def add_comment(self, comment: str, user: str):
        try:
            self.comments.append({"user": user, "comment": comment})
            logging.info(f'User: {user} added comment to task: {self.title}')
        except Exception as e:
            logging.error(f'Error adding comment to task {self.title} by user {user}: {e}')

class ProjectManager:
    def __init__(self):
        try:
            self.users = {}
            self.projects = {}
            logging.info('Initialized ProjectManager')
        except Exception as e:
            logging.error(f'Error initializing ProjectManager: {e}')

    def create_user(self, username: str, password: str, email: str):
        try:
            if username not in self.users:
                self.users[username] = User(username, password, email)
                logging.info(f'Created user: {username}')
        except Exception as e:
            logging.error(f'Error creating user {username}: {e}')

    def create_project(self, title: str, creator: str):
        try:
            if creator in self.users:
                self.projects[title] = Project(title, creator)
                logging.info(f'Created project: {title} by creator: {creator}')
        except Exception as e:
            logging.error(f'Error creating project {title}: {e}')

    def add_member_to_project(self, project_title: str, member: str):
        try:
            if project_title in self.projects:
                self.projects[project_title].add_member(member)
                logging.info(f'Added member: {member} to project: {project_title}')
        except Exception as e:
            logging.error(f'Error adding member {member} to project {project_title}: {e}')

    def remove_member_from_project(self, project_title: str, member: str):
        try:
            if project_title in self.projects:
                self.projects[project_title].remove_member(member)
                logging.info(f'Removed member: {member} from project: {project_title}')
        except Exception as e:
            logging.error(f'Error removing member {member} from project {project_title}: {e}')

    def delete_project(self, project_title: str):
        try:
            if project_title in self.projects:
                del self.projects[project_title]
                logging.info(f'Deleted project: {project_title}')
        except Exception as e:
            logging.error(f'Error deleting project {project_title}: {e}')

    def create_task(self, project_title: str, title: str, description: str, assigned_to: List[str],
                    priority: Priority = Priority.LOW, status: Status = Status.BACKLOG):
        try:
            if project_title in self.projects:
                task = Task(title, description, assigned_to, priority, status)
                self.projects[project_title].tasks.append(task)
                logging.info(f'Created task: {title} in project: {project_title}')
        except Exception as e:
            logging.error(f'Error creating task {title} in project {project_title}: {e}')

    def assign_task_to_member(self, project_title: str, task_id: str, user: str):
        try:
            if project_title in self.projects:
                for task in self.projects[project_title].tasks:
                    if task.id == task_id:
                        task.assign_task(user)
                        logging.info(f'Assigned task: {task_id} to user: {user} in project: {project_title}')
        except Exception as e:
            logging.error(f'Error assigning task {task_id} to user {user} in project {project_title}: {e}')

    def unassign_task_from_member(self, project_title: str, task_id: str, user: str):
        try:
            if project_title in self.projects:
                for task in self.projects[project_title].tasks:
                    if task.id == task_id:
                        task.unassign_task(user)
                        logging.info(f'Unassigned task: {task_id} from user: {user} in project: {project_title}')
        except Exception as e:
            logging.error(f'Error unassigning task {task_id} from user {user} in project {project_title}: {e}')

    def change_task_priority(self, project_title: str, task_id: str, new_priority: Priority):
        try:
            if project_title in self.projects:
                for task in self.projects[project_title].tasks:
                    if task.id == task_id:
                        task.change_priority(new_priority)
                        logging.info(f'Changed priority of task: {task_id} to {new_priority.name} in project: {project_title}')
        except Exception as e:
            logging.error(f'Error changing priority of task {task_id} to {new_priority.name} in project {project_title}: {e}')

    def change_task_status(self, project_title: str, task_id: str, new_status: Status):
        try:
            if project_title in self.projects:
                for task in self.projects[project_title].tasks:
                    if task.id == task_id:
                        task.change_status(new_status)
                        logging.info(f'Changed status of task: {task_id} to {new_status.name} in project: {project_title}')
        except Exception as e:
            logging.error(f'Error changing status of task {task_id} to {new_status.name} in project {project_title}: {e}')

    def add_comment_to_task(self, project_title: str, task_id: str, comment: str, user: str):
        try:
            if project_title in self.projects:
                for task in self.projects[project_title].tasks:
                    if task.id == task_id:
                        task.add_comment(comment, user)
                        logging.info(f'Added comment to task: {task_id} by user: {user} in project: {project_title}')
        except Exception as e:
            logging.error(f'Error adding comment to task {task_id} by user {user} in project {project_title}: {e}')

    def view_tasks_in_project(self, project_title: str) -> List[Dict[str, Any]]:
        try:
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
                logging.info(f'Viewed tasks in project: {project_title}')
                return tasks_info
            else:
                logging.error(f'Project {project_title} does not exist')
                return []
        except Exception as e:
            logging.error(f'Error viewing tasks in project {project_title}: {e}')
            return []

    def view_task_details(self, project_title: str, task_id: str) -> Dict[str, Any]:
        try:
            if project_title in self.projects:
                for task in self.projects[project_title].tasks:
                    if task.id == task_id:
                        logging.info(f'Viewed details of task: {task_id} in project: {project_title}')
                        return {
                            "Task ID": task.id,
                            "Title": task.title,
                            "Description": task.description,
                            "Assigned To": task.assigned_to,
                            "Priority": task.priority.name,
                            "Status": task.status.name,
                            "Comments": task.comments
                        }
                logging.error(f'Task {task_id} does not exist in project {project_title}')
                return {}
            else:
                logging.error(f'Project {project_title} does not exist')
                return {}
        except Exception as e:
            logging.error(f'Error viewing details of task {task_id} in project {project_title}: {e}')
            return {}

    def save_data(self):
        try:
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
            logging.info('Saved data to users.json and projects.json')
        except Exception as e:
            logging.error(f'Error saving data: {e}')

def main():
    manager = ProjectManager()

    while True:
        
        print("0. Create admin")
        print("1. Create User")
        print("2. Create Project")
        print("3. Add Member to Project")
        print("4. Remove Member from Project")
        print("5. Create Task")
        print("6. Assign Task to Member")
        print("7. Unassign Task from Member")
        print("8. Change Task Priority")
        print("9. Change Task Status")
        print("10. Add Comment to Task")
        print("11. View Tasks in Project")
        print("12. View Task Details")
        print("13. Save Data")
        print("14. Exit")

        choice = input("Enter your choice: ")
        if choice == '0':
            manager= ma.create_admin()
            
        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            email = input("Enter email: ")
            manager.create_user(username, password, email)

        elif choice == '2':
            title = input("Enter project title: ")
            creator = input("Enter creator username: ")
            manager.create_project(title, creator)

        elif choice == '3':
            project_title = input("Enter project title: ")
            member = input("Enter member username: ")
            manager.add_member_to_project(project_title, member)

        elif choice == '4':
            project_title = input("Enter project title: ")
            member = input("Enter member username: ")
            manager.remove_member_from_project(project_title, member)

        elif choice == '5':
            project_title = input("Enter project title: ")
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            assigned_to = input("Enter usernames of assigned members (comma-separated): ").split(",")
            priority = Priority[input("Enter task priority (CRITICAL, HIGH, MEDIUM, LOW): ").upper()]
            status = Status[input("Enter task status (BACKLOG, TODO, DOING, DONE, ARCHIVED): ").upper()]
            manager.create_task(project_title, title, description, assigned_to, priority, status)

        elif choice == '6':
            project_title = input("Enter project title: ")
            task_id = input("Enter task ID: ")
            user = input("Enter username to assign: ")
            manager.assign_task_to_member(project_title, task_id, user)

        elif choice == '7':
            project_title = input("Enter project title: ")
            task_id = input("Enter task ID: ")
            user = input("Enter username to unassign: ")
            manager.unassign_task_from_member(project_title, task_id, user)

        elif choice == '8':
            project_title = input("Enter project title: ")
            task_id = input("Enter task ID: ")
            new_priority = Priority[input("Enter new priority (CRITICAL, HIGH, MEDIUM, LOW): ").upper()]
            manager.change_task_priority(project_title, task_id, new_priority)

        elif choice == '9':
            project_title = input("Enter project title: ")
            task_id = input("Enter task ID: ")
            new_status = Status[input("Enter new status (BACKLOG, TODO, DOING, DONE, ARCHIVED): ").upper()]
            manager.change_task_status(project_title, task_id, new_status)

        elif choice == '10':
            project_title = input("Enter project title: ")
            task_id = input("Enter task ID: ")
            comment = input("Enter comment: ")
            user = input("Enter username: ")
            manager.add_comment_to_task(project_title, task_id, comment, user)

        elif choice == '11':
            project_title = input("Enter project title: ")
            tasks = manager.view_tasks_in_project(project_title)
            for task in tasks:
                print(task)
                print
        elif choice == '12':
            project_title = input("Enter project title: ")
            task_id = input("Enter task ID: ")
            task_details = manager.view_task_details(project_title, task_id)
            print(task_details)

        elif choice == '13':
            manager.save_data()

        elif choice == '14':
            break

        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
