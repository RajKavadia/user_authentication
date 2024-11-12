import hashlib

# Function to hash a password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user():
    username = input("Enter username: ")
    password = input("Enter password: ")

    # Ensure the users file exists before reading it
    if not os.path.exists('users.txt'):
        with open('users.txt', 'w'):  # Create the file if it doesn't exist
            pass

    # Check if username already exists
    with open('users.txt', 'r') as f:
        users = f.readlines()
        for user in users:
            if user.split(',')[0] == username:
                print("Username already exists.")
                return

    # Store username and hashed password
    with open('users.txt', 'a') as f:
        f.write(f"{username},{hash_password(password)}\n")
    print("Registration successful.")


# Login Function
def login_user():
    username = input("Enter username: ")
    password = input("Enter password: ")
    hashed_password = hash_password(password)

    with open('users.txt', 'r') as f:
        users = f.readlines()
        for user in users:
            stored_username, stored_password = user.strip().split(',')
            if stored_username == username and stored_password == hashed_password:
                print("Login successful.")
                return username  # Return the logged-in user's username
    print("Invalid credentials.")
    return None


import os

# Helper function to load tasks for a specific user
def load_tasks(username):
    if not os.path.exists(f'{username}_tasks.txt'):
        return []
    with open(f'{username}_tasks.txt', 'r') as f:
        tasks = f.readlines()
    return [task.strip().split(',') for task in tasks]

# Helper function to save tasks for a specific user
def save_tasks(username, tasks):
    with open(f'{username}_tasks.txt', 'w') as f:
        for task in tasks:
            f.write(','.join(task) + '\n')

# Add Task Function
def add_task(username):
    task_description = input("Enter task description: ")
    tasks = load_tasks(username)
    task_id = len(tasks) + 1  # Generate a new task ID
    task_status = "Pending"
    tasks.append([str(task_id), task_description, task_status])
    save_tasks(username, tasks)
    print(f"Task added with ID {task_id}.")

# View Tasks Function
def view_tasks(username):
    tasks = load_tasks(username)
    if not tasks:
        print("No tasks available.")
        return
    for task in tasks:
        task_id, description, status = task
        print(f"ID: {task_id} | Description: {description} | Status: {status}")

# Mark Task as Completed Function
def mark_task_completed(username):
    task_id = input("Enter task ID to mark as completed: ")
    tasks = load_tasks(username)
    for task in tasks:
        if task[0] == task_id:
            task[2] = "Completed"
            save_tasks(username, tasks)
            print(f"Task ID {task_id} marked as completed.")
            return
    print("Task not found.")

# Delete Task Function
def delete_task(username):
    task_id = input("Enter task ID to delete: ")
    tasks = load_tasks(username)
    for i, task in enumerate(tasks):
        if task[0] == task_id:
            del tasks[i]
            save_tasks(username, tasks)
            print(f"Task ID {task_id} deleted.")
            return
    print("Task not found.")


def task_manager(username):
    while True:
        print("\nTask Manager Menu:")
        print("1. Add a Task")
        print("2. View Tasks")
        print("3. Mark a Task as Completed")
        print("4. Delete a Task")
        print("5. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_task(username)
        elif choice == "2":
            view_tasks(username)
        elif choice == "3":
            mark_task_completed(username)
        elif choice == "4":
            delete_task(username)
        elif choice == "5":
            print("Logging out...")
            break
        else:
            print("Invalid choice, please try again.")


def main():
    while True:
        print("\nWelcome to the Task Manager!")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            register_user()
        elif choice == "2":
            username = login_user()
            if username:
                task_manager(username)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
