from Helpers import (
    print_colored, input_email, input_username, input_password, input_date,
    input_difficulty, input_hours, print_progress_bar, generate_motivational_message,
    clear_screen, pause
)
from user_data import UserData
from datetime import datetime, timedelta

class StudyBuddy:
    def __init__(self, data_file='user_login_details.json'):
        self.user_data = UserData(data_file)
        self.current_user_email = None
        self.hours_per_difficulty = 2

    def signup(self):
        clear_screen()
        print_colored("⚠️ Sign Up", "cyan")
        while True:
            email = input_email()
            if self.user_data.email_exists(email):
                print_colored("❌ Email already registered. Try logging in.", "red")
                pause()
                return False
            username = input_username()
            if self.user_data.username_exists(username):
                print_colored("❌ Username already taken. Try another.", "red")
                continue
            password = input_password()
            self.user_data.add_user(email, username, password)
            print_colored("✅ Signup successful! Please login now.", "green")
            pause()
            return True

    def login(self):
        clear_screen()
        print_colored("⚠️ Login", "cyan")
        email_or_username = input("📧 Enter email or username: ").strip()
        password = input("🔐 Enter password: ").strip()

        user = None
        if self.user_data.email_exists(email_or_username):
            user = self.user_data.get_user(email_or_username)
            email = email_or_username
        else:
            for e, u in self.user_data.data['users'].items():
                if u['username'] == email_or_username:
                    user = u
                    email = e
                    break

        if user and user['password'] == password:
            self.current_user_email = email
            print_colored(f"🚀 Welcome, {user['username']}!", "green")
            pause()
            return True
        else:
            print_colored("❌ Invalid credentials. Try again.", "red")
            pause()
            return False

    def view_tasks(self):
        clear_screen()
        tasks = self.user_data.get_tasks(self.current_user_email)
        if not tasks:
            print_colored("❌ No tasks found.", "yellow")
            pause()
            return
        print_colored("🎯 Your Tasks:", "cyan")
        for idx, task in enumerate(tasks):
            hours_studied = task.get('hours_studied', 0)
            deadline = task.get('deadline', 'N/A')
            difficulty = task.get('difficulty', 'N/A')
            total_hours = difficulty * self.hours_per_difficulty
            print(f"{idx+1}. {task['subject']} | Deadline: {deadline} | Difficulty: {difficulty} | Hours Studied: {hours_studied}")
            print_progress_bar(hours_studied, total_hours)
        pause()

    def add_task(self):
        clear_screen()
        print_colored("🎚️ Add New Task", "cyan")
        subject = input("📚 Enter subject/topic: ").strip()
    
        tasks = self.user_data.get_tasks(self.current_user_email)
        existing_task_index = None
        for idx, task in enumerate(tasks):
            if task['subject'].lower() == subject.lower():
                existing_task_index = idx
                break
            
        if existing_task_index is not None:
            print_colored(f"Task for subject '{subject}' already exists.", 'yellow')
            choice = input("Do you want to update the existing task instead? (y/n): ").strip().lower()
            if choice == 'y':
                deadline = input_date("📅 Enter new deadline (YYYY-MM-DD): ").strftime('%Y-%m-%d')
                difficulty = input_difficulty("🎚️ Enter new difficulty (1-10): ")
                tasks[existing_task_index]['deadline'] = deadline
                tasks[existing_task_index]['difficulty'] = difficulty
                self.user_data.save_data()
                print_colored("✅ Task updated successfully!", "green")
                pause()
                return
            else:
                print_colored("❌ Task not added.", "yellow")
                pause()
                return
    
        deadline = input_date("📅 Enter deadline (YYYY-MM-DD): ").strftime('%Y-%m-%d')
        difficulty = input_difficulty("🎚️ Enter difficulty (1-10): ")
        task = {
            "subject": subject,
            "deadline": deadline,
            "difficulty": difficulty,
            "hours_studied": 0
        }
        self.user_data.add_task(self.current_user_email, task)
        print_colored("✅ Task added successfully!", "green")
        pause()

    def update_task_progress(self):
        clear_screen()
        tasks = self.user_data.get_tasks(self.current_user_email)
        if not tasks:
            print_colored("❌ No tasks found to update.", "yellow")
            pause()
            return

        self.view_tasks()
        while True:
            choice = input(f"📝 Select task number to update hours (1-{len(tasks)}): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(tasks):
                task_index = int(choice) - 1
                break
            print_colored("❌ Invalid selection. Try again.", "red")

        current_hours = tasks[task_index].get('hours_studied', 0)
        hours = input_hours(f"🔥 Enter hours studied to add (current: {current_hours}): ")
        new_hours = current_hours + hours
        self.user_data.update_task_progress(self.current_user_email, task_index, new_hours)
        total_hours = tasks[task_index]['difficulty'] * self.hours_per_difficulty
        print_progress_bar(new_hours, total_hours)
        print_colored("✅ Hours updated successfully!", "green")
        pause()

    def create_study_plan(self):
        clear_screen()
        tasks = self.user_data.get_tasks(self.current_user_email)
        if not tasks:
            print_colored("❌ No tasks available to create a study plan.", "yellow")
            pause()
            return

        today = datetime.today()
        tasks_sorted = sorted(tasks, key=lambda t: (t['deadline'], -t['difficulty']))

        study_plan = {}
        for task in tasks_sorted:
            deadline_date = datetime.strptime(task['deadline'], '%Y-%m-%d')
            days_left = max((deadline_date - today).days, 1)
            total_hours = task['difficulty'] * self.hours_per_difficulty
            hours_studied = task.get('hours_studied', 0)
            remaining_hours = max(total_hours - hours_studied, 0)
            daily_study_hours = round(remaining_hours / days_left, 2)

            study_plan[task['subject']] = {
                "deadline": task['deadline'],
                "daily_study_hours": daily_study_hours
            }

        self.user_data.set_study_plan(self.current_user_email, study_plan)
        print_colored("🌟 Study plan created successfully! Choose 'View Study Plan' to see the day-wise schedule.", "green")
        pause()

    def view_study_plan(self):
        clear_screen()
        plan = self.user_data.get_study_plan(self.current_user_email)
        if not plan:
            print_colored("❌ No study plan found. Create one first.", "yellow")
            pause()
            return

        print_colored("📅 Your Day-wise Study Plan:", "cyan")
        today = datetime.today()

        for subject, details in plan.items():
            deadline_date = datetime.strptime(details['deadline'], '%Y-%m-%d')
            days_left = (deadline_date - today).days
            if days_left < 0:
                continue

            if days_left < 3:
                color = 'red'
            elif days_left < 7:
                color = 'yellow'
            else:
                color = 'green'

            print_colored(f"\n📚 {subject} (Deadline: {details['deadline']})", color)
            for day_offset in range(days_left + 1):
                date = (today + timedelta(days=day_offset)).strftime('%Y-%m-%d')
                hours = details['daily_study_hours']
                if hours < 1:
                    time_display = f"{int(hours * 60)} min"
                else:
                    time_display = f"{hours:.1f} hrs"
                print(f"  {date}: {time_display}")

        tasks = self.user_data.get_tasks(self.current_user_email)
        goal_met = all(task.get('hours_studied', 0) >= task['difficulty'] * self.hours_per_difficulty for task in tasks)
        if goal_met:
            print_colored("\n🎉 You've completed all your tasks! Excellent work!", "green")

        pause()

    def export_study_plan_pdf(self):
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
        except ImportError:
            print_colored("❌ ReportLab not installed. Install it to export PDFs.", "red")
            pause()
            return

        plan = self.user_data.get_study_plan(self.current_user_email)
        if not plan:
            print_colored("❌ No study plan to export.", "yellow")
            pause()
            return
        username = self.user_data.get_user(self.current_user_email)["username"]
        filename = f"{self.current_user_email}_study_plan.pdf"
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter
    
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, f" {username}'s Day-wise Study Plan ")

        y = height - 90
        today = datetime.today()

        c.setFont("Helvetica", 12)
        for subject, details in plan.items():
            deadline_str = details.get("deadline")
            daily_hours = details.get("daily_study_hours", 0)

            try:
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
            except:
                continue

            days_left = max((deadline - today).days + 1, 1)

            c.setFont("Helvetica-Bold", 13)
            c.drawString(50, y, f"Subject: {subject} (Deadline: {deadline_str})")
            y -= 20

            c.setFont("Helvetica", 11)
            for i in range(days_left):
                date = today + timedelta(days=i)
                study_time = daily_hours
                if study_time < 1:
                    time_str = f"{round(study_time * 60)} mins"
                else:
                    time_str = f"{round(study_time, 2)} hours"
                line = f"{date.strftime('%Y-%m-%d (%A)')}: {time_str}"
                c.drawString(70, y, line)
                y -= 15
                if y < 50:
                    c.showPage()
                    y = height - 50

            y -= 10

        c.save()
        print_colored(f"💪 Study plan exported as {filename}", "green")
        pause()

    def show_motivational_message(self):
        msg = generate_motivational_message()
        print_colored(msg, "green")

    def logout(self):
        self.current_user_email = None
        print_colored("💪🙂 Logged out successfully.", "green")
        pause()

    def user_menu(self):
        while True:
            clear_screen()
            print_colored("=== Study Buddy Menu ===", "cyan")
            print("1. View Tasks")
            print("2. Add Task")
            print("3. Update Task Hours")
            print("4. Create Study Plan")
            print("5. View Study Plan")
            print("6. Export Study Plan to PDF")
            print("7. Show Motivational Message")
            print("8. Logout")
            choice = input("Enter your choice (1-8): ").strip()

            if choice == '1':
                self.view_tasks()
            elif choice == '2':
                self.add_task()
            elif choice == '3':
                self.update_task_progress()
            elif choice == '4':
                self.create_study_plan()
            elif choice == '5':
                self.view_study_plan()
            elif choice == '6':
                self.export_study_plan_pdf()
            elif choice == '7':
                self.show_motivational_message()
                pause()
            elif choice == '8':
                self.logout()
                break
            else:
                print_colored("Invalid choice. Try again.", "red")
                pause()