"""CLI interface for Todo App.

This module provides the menu-driven command-line interface for the
todo application as specified in contracts/cli-interface.md.
"""

import sys
from src.task_manager import TaskManager, TaskNotFoundError


# Menu constants
MENU_HEADER = """
========================================
       TODO APP - Main Menu
========================================

1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Complete/Incomplete
6. Exit

"""


def display_menu() -> None:
    """Display the main menu."""
    print(MENU_HEADER)


def get_menu_choice() -> str:
    """Get and validate menu choice from user.

    Returns:
        Valid menu choice (1-6)
    """
    while True:
        choice = input("Enter your choice (1-6): ").strip()
        if choice in ["1", "2", "3", "4", "5", "6"]:
            return choice
        print("✗ Error: Invalid choice. Please enter 1-6.")


def add_task_flow(manager: TaskManager) -> None:
    """Handle the add task flow.

    Prompts user for title and description, creates the task,
    and displays confirmation.
    """
    # Get title (required, reprompt if empty)
    while True:
        title = input("Enter task title: ").strip()
        if title:
            break
        print("✗ Error: Title cannot be empty. Please try again.")

    # Get description (optional)
    description = input("Enter task description (optional, press Enter to skip): ")

    # Create task
    task = manager.add_task(title, description)

    print(f'✓ Task #{task.id} created: "{task.title}"')


def view_tasks_flow(manager: TaskManager) -> None:
    """Handle the view all tasks flow.

    Displays all tasks in a formatted table or a message if no tasks exist.
    """
    tasks = manager.get_all_tasks()

    print("========================================")
    print("            YOUR TASKS")
    print("========================================")

    if not tasks:
        print("No tasks found. Add your first task!")
        print("========================================")
        return

    # Print table header
    print(f"{'ID':<4}| {'Status':<7}| {'Title':<26}| {'Description':<27}")
    print("-" * 4 + "|" + "-" * 8 + "|" + "-" * 27 + "|" + "-" * 27)

    # Print each task
    for task in tasks:
        status = "[x]" if task.is_complete else "[ ]"
        # Truncate description for display
        desc = task.description
        if len(desc) > 25:
            desc = desc[:22] + "..."
        # Truncate title for display
        title = task.title
        if len(title) > 25:
            title = title[:22] + "..."

        print(f"{task.id:<4}| {status:<7}| {title:<26}| {desc:<27}")

    print("========================================")

    # Count summary
    complete = sum(1 for t in tasks if t.is_complete)
    pending = len(tasks) - complete
    print(f"Total: {len(tasks)} tasks ({complete} complete, {pending} pending)")


def toggle_status_flow(manager: TaskManager) -> None:
    """Handle the mark complete/incomplete flow.

    Prompts for task ID and toggles its completion status.
    """
    task_id_input = input("Enter task ID to toggle status: ").strip()

    # Validate ID format
    try:
        task_id = int(task_id_input)
    except ValueError:
        print("✗ Error: Invalid ID format. Please enter a number.")
        return

    if task_id <= 0:
        print("✗ Error: Invalid ID. Task IDs start from 1.")
        return

    # Toggle status
    try:
        task = manager.toggle_complete(task_id)
        status = "complete" if task.is_complete else "pending"
        print(f'✓ Task #{task.id} "{task.title}" marked as {status}.')
    except TaskNotFoundError:
        print(f"✗ Error: Task #{task_id} not found.")


def update_task_flow(manager: TaskManager) -> None:
    """Handle the update task flow.

    Prompts for task ID and new values for title/description.
    """
    task_id_input = input("Enter task ID to update: ").strip()

    # Validate ID format
    try:
        task_id = int(task_id_input)
    except ValueError:
        print("✗ Error: Invalid ID format. Please enter a number.")
        return

    if task_id <= 0:
        print("✗ Error: Invalid ID. Task IDs start from 1.")
        return

    # Get existing task
    task = manager.get_task(task_id)
    if task is None:
        print(f"✗ Error: Task #{task_id} not found.")
        return

    # Prompt for new title
    print(f'Current title: "{task.title}"')
    new_title = input("Enter new title (press Enter to keep current): ").strip()

    # Prompt for new description
    print(f'Current description: "{task.description}"')
    new_description = input("Enter new description (press Enter to keep current): ")

    # Update task (only pass values that changed)
    update_title = new_title if new_title else None
    update_desc = new_description if new_description else None

    manager.update_task(task_id, title=update_title, description=update_desc)

    print(f"✓ Task #{task_id} updated successfully.")


def delete_task_flow(manager: TaskManager) -> None:
    """Handle the delete task flow.

    Prompts for task ID and confirms before deletion.
    """
    task_id_input = input("Enter task ID to delete: ").strip()

    # Validate ID format
    try:
        task_id = int(task_id_input)
    except ValueError:
        print("✗ Error: Invalid ID format. Please enter a number.")
        return

    if task_id <= 0:
        print("✗ Error: Invalid ID. Task IDs start from 1.")
        return

    # Get existing task
    task = manager.get_task(task_id)
    if task is None:
        print(f"✗ Error: Task #{task_id} not found.")
        return

    # Confirm deletion
    confirm = input(
        f'Are you sure you want to delete task #{task_id} "{task.title}"? (y/n): '
    ).strip().lower()

    if confirm == "y":
        manager.delete_task(task_id)
        print(f"✓ Task #{task_id} deleted.")
    else:
        print("Deletion cancelled.")


def exit_flow() -> None:
    """Handle the exit flow."""
    print("Goodbye! Your tasks were not saved (in-memory only).")
    sys.exit(0)


def main() -> None:
    """Main entry point for the CLI Todo App."""
    manager = TaskManager()

    while True:
        try:
            display_menu()
            choice = get_menu_choice()

            if choice == "1":
                add_task_flow(manager)
            elif choice == "2":
                view_tasks_flow(manager)
            elif choice == "3":
                update_task_flow(manager)
            elif choice == "4":
                delete_task_flow(manager)
            elif choice == "5":
                toggle_status_flow(manager)
            elif choice == "6":
                exit_flow()

        except KeyboardInterrupt:
            print("\n")
            exit_flow()
        except Exception as e:
            print(f"✗ An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
