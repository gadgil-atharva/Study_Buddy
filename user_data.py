import json
import os

class UserData:
    def __init__(self, filename='user_login_details.json'):
        self.filename = filename
        self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.data = json.load(f)
                for user in self.data['users'].values():
                    for task in user.get('tasks', []):
                        if 'progress' in task:
                            task['hours_studied'] = task.pop('progress', 0) / 10.0
        else:
            self.data = {"users": {}}
            self.save_data()

    def save_data(self):
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=4)

    def email_exists(self, email):
        return email in self.data['users']

    def username_exists(self, username):
        for user in self.data['users'].values():
            if user['username'] == username:
                return True
        return False

    def add_user(self, email, username, password):
        self.data['users'][email] = {
            "username": username,
            "password": password,
            "tasks": [],
            "study_plan": {}
        }
        self.save_data()

    def get_user(self, email):
        return self.data['users'].get(email)

    def get_tasks(self, email):
        user = self.get_user(email)
        if user:
            return user.get('tasks', [])
        return []

    def add_task(self, email, task):
        user = self.get_user(email)
        if user:
            user['tasks'].append(task)
            self.save_data()

    def update_task_progress(self, email, task_index, hours):
        user = self.get_user(email)
        if user and 0 <= task_index < len(user.get('tasks', [])):
            user['tasks'][task_index]['hours_studied'] = hours
            self.save_data()

    def get_study_plan(self, email):
        user = self.get_user(email)
        if user:
            return user.get('study_plan', {})
        return {}

    def set_study_plan(self, email, plan):
        user = self.get_user(email)
        if user:
            user['study_plan'] = plan
            self.save_data()