from core import StudyBuddy
from Helpers import clear_screen, pause, print_colored

def main_menu():
    sb = StudyBuddy()
    while True:
        clear_screen()
        print_colored("=== 😄 Welcome to Study Buddy 😄 ===","cyan")
        print("1. 🔐 Login")
        print("2. ✍️  Signup")
        print("3. 🚪 Exit")
        choice = input("💾 Enter your choice: ").strip()

        if choice == '1':
            if sb.login():
                sb.user_menu()
        elif choice == '2':
            sb.signup()
        elif choice == '3':
            print("👋 Goodbye! Keep crushing!!")
            break
        else:
            print("😢 Invalid choice, try again.")
            pause()

if __name__ == '__main__':
    main_menu()
