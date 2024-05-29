import json
import os
import re
import logging
from project_manager import ProjectManager
logging.basicConfig(filename='project.log', level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')
    
    
def is_valid_email(email):
    email_regex = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")
    return re.match(email_regex, email) is not None

def create_admin(file_path='admin_data.json'):
    username = input("Enter username for the admin user: ")
    password = input("Enter password for the admin user: ")
    email = input("Enter email for the admin user: ")

    if not is_valid_email(email):
        print("Invalid email address")
        return

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            if data.get('username') == username:
                print(f"Error: Admin with username '{username}' already exists.")
                return
    else:
        data = {}

    data['username'] = username
    data['password'] = password
    data['email'] = email
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Admin '{username}' created successfully.")
        logging.info("Admin '%s' created successfully.", username)
    except Exception as e:
        logging.error("Error saving admin data: %s", str(e))
        
def delete_all(self):
        pr= ProjectManager()
        confirmation = input("Are you sure you want to delete all data? (yes/no): ")
        if confirmation.lower() == "yes":
            pr.users = {}
            pr.projects = {}
            print("All data has been deleted.")
        else:
            print("Operation canceled.")
            
def main():
    create_admin()

if __name__ == '__main__':
    main()
