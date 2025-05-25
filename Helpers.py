# In Helpers.py
import re
import os
import random
from datetime import datetime

# Console color printing
def print_colored(text, color):
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'cyan': '\033[96m',
        'magenta': '\033[95m',
        'endc': '\033[0m',
    }
    color_code = colors.get(color.lower(), '')
    end_code = colors['endc'] if color_code else ''
    print(f"{color_code}{text}{end_code}")

# Email input validation
def input_email():
    while True:
        email = input("📧 Enter email: ").strip().lower()
        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            return email
        print_colored("❌ Invalid email format. Try again.", 'red')

# Username input validation
def input_username():
    while True:
        username = input("👤 Enter username: ").strip()
        if 3 <= len(username) <= 15 and username.isalnum():
            return username
        print_colored("❌ Username must be 3-15 characters, alphanumeric only.", 'red')

# Password input validation
def input_password():
    while True:
        password = input("🔐 Enter password: ").strip()
        if len(password) >= 6:
            return password
        print_colored("❌ Password must be at least 6 characters.", 'red')

# Date input
def input_date(prompt):
    while True:
        date_str = input(prompt).strip()
        try:
            return datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            print_colored("📅 Invalid date format. Use YYYY-MM-DD.", 'red')

# Difficulty input
def input_difficulty(prompt, allow_zero=False, max_val=10):
    while True:
        val = input(prompt).strip()
        if val.isdigit():
            num = int(val)
            if allow_zero and num == 0:
                return num
            if 1 <= num <= max_val:
                return num
        print_colored(f"❌ Enter a number between {'0' if allow_zero else '1'} and {max_val}.", 'red')

# Hours input validation
def input_hours(prompt):
    while True:
        val = input(prompt).strip()
        try:
            hours = float(val)
            if hours >= 0:
                return hours
            print_colored("❌ Hours must be non-negative.", 'red')
        except ValueError:
            print_colored("❌ Enter a valid number (e.g., 2.5 for 2.5 hours).", 'red')

# Progress bar with emoji (converts hours to percentage for display)
def print_progress_bar(hours, total_hours, length=20, return_str=False):
    percentage = min(round((hours / total_hours) * 100), 100) if total_hours > 0 else 0
    filled_length = int(length * percentage // 100)
    bar = '█' * filled_length + '-' * (length - filled_length)
    msg = f"[{bar}] {percentage}% ✅" if percentage == 100 else f"[{bar}] {percentage}%"
    if return_str:
        return msg
    print(msg)

# Random motivational message
def generate_motivational_message():
    messages = [
        "💪 Keep pushing forward!",
        "🚀 You're doing great!",
        "📘 Every step counts!",
        "🧠 Stay focused and keep going!",
        "🏁 Success is near!",
        "👏 Keep up the awesome work!",
        "🌟 Believe in yourself!",
        "☕ Stay positive and study hard!",
        "📈 Small progress is still progress!",
    ]
    return random.choice(messages)

# Screen clear
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Pause screen
def pause():
    input("⏸ Press Enter to continue...")

# Friendly main menu printer
def print_menu(title, options):
    print_colored(f"\n=== {title} ===", 'cyan')
    for idx, option in enumerate(options, 1):
        print(f"{idx}. {option}")