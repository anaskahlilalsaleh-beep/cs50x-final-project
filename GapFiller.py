import sys 
from cs50 import SQL
from datetime import datetime
from tabulate import tabulate # I obtained this library from AI!

# Connect to the SQLite database
db = SQL("sqlite:///tasks.db")


def main():
    # Ensure correct number of command-line arguments and correct input
    if len(sys.argv) != 2:
        print("Usage: python main.py <database_path>")
        sys.exit(1)

    sys.argv[1] = sys.argv[1].upper()
    database_path = sys.argv[1]

    if database_path not in ['ADD', 'GET', 'HISTORY', 'SHOW', 'HELP', 'UPDATE', 'DELETE', 'HELP', 'EXIT']:
        print("Usage: python main.py <database_path>")
        sys.exit(1)

    if database_path == "ADD":
        # Create and save a new task to the database
        add_task()
           
    elif database_path == "GET":
        # Retrieve the most suitable task based on time and priority
        get_tasks()

    elif database_path == "HISTORY":
        # View all completed tasks 
        history_tasks()

    elif database_path == "SHOW":
        # Display a table of all (unfinished) tasks
        show_tasks()

    elif database_path == 'UPDATE':
        # Update or Change information in the task
        update_tasks()

    elif database_path == 'DELETE':
        # Delete a task by its ID
        delete_tasks()

    # Show help message (This function was Suggested by AI!)
    elif database_path == "HELP": 
        help()

    # Exit the program if the user inputs EXIT command (This function was added by AI!)
    elif database_path == "EXIT":
        print("Exiting the program.")
        sys.exit(0)


def add_task():
    title = input("Enter task title: ").lower()
    description = input("Enter task description: ") #A proposal derived from Ai!
    
    while True:  
        category = input("select the number: 1. Quick Wins / 2. Errands / 3. Academic / 4. Personal / 5. Work / 6. Others: ")
        if category in ['1', '2', '3', '4', '5', '6']: # (the idea taken from Ai)
            category = int(category) # Convert to integer for database storage (the idea taken from Ai) 
            break
        print("Invalid category. Please enter a number between 1 and 6.")

    while True:  #The idea of ​​the episode is based on Ai.
        priority = input("Enter the priority (High / Medium / Low): ").lower()
        if priority in ['high', 'medium', 'low']:
            break
        print("Invalid priority. Please enter High, Medium, or Low.")

    while True:
        Estimated_time = input("Enter estimated time to complete the task (in minutes): ")
        if Estimated_time.isdigit():
            Estimated_time = int(Estimated_time)
            break
        print("Invalid input. Please enter a number.")
    input_date = datetime.now().strftime("%Y-%m-%d %H:%M") # (YYYY-MM-DD HH:MM) format (added by Ai)

    task = db.execute("INSERT INTO tasks (task, description, category_id, priority, estimated_time, input_date) VALUES (?, ?, ?, ?, ?, ?)", title, description, category, priority, Estimated_time, input_date)
    category_id = db.execute("SELECT name FROM categories WHERE id = ?", category) # The formula was written with the help of AI!
    print(f"Category: {category_id[0]['name']}, Title: {title}, Description: {description}, Priority: {priority}, Estimated Time: {Estimated_time} minutes, Input Date: {input_date}") # The method and concept are inspired by AI!
    print("Task added successfully.")


def get_tasks():
    tasks = db.execute("SELECT tasks.*, categories.name AS category_name FROM tasks JOIN categories ON tasks.category_id = categories.id WHERE status = 'unfinished' ORDER BY CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 WHEN 'low' THEN 3 END, input_date ASC") # the query is taken from Ai!
    while True:
        available_time = input("Enter available time in minutes: ")
        if available_time.isdigit():
            available_time = int(available_time)
            break
        print("Invalid input. Please enter a number.")
    
    for task in tasks:
        if task["estimated_time"] <= available_time: 
            print(f"Category: {task['category_name']}, Priority: {task['priority']}, ")
            print(f"Title: {task['task']},  Description: {task['description']}, Estimated Time: {task['estimated_time']} min.")
            while True:
                user_input = input("Do you want to do the job? (yes/no): ") 
                if user_input.lower() in ["yes", "no", "y", "n"]:
                    break
                print("Invalid input. Please enter 'yes' or 'no'.")
            if user_input.lower() in ["yes",  'y']:
                db.execute("update tasks set status = 'finished' where id = ?", task["id"])
                time = datetime.now().strftime("%Y-%m-%d %H:%M")
                db.execute("update tasks set terminated = ? where id = ?", time, task["id"])
                print(f"Great! You have selected the task: {task['task']}")
                break
            elif user_input.lower() in ["no", 'n']:
                print("Looking for next best task...")
                continue
        elif not any(task["estimated_time"] <= available_time and task["status"] == "unfinished" for task in tasks): # The writing method was improved using AI!
            print("No tasks fit within the available time.")
            break
    

def history_tasks():
    amount = db.execute("SELECT count(*) FROM tasks WHERE status = 'finished'")
    completed_tasks = db.execute("SELECT categories.name AS category_name, tasks.task, tasks.description, tasks.estimated_time, tasks.priority, tasks.status, tasks.input_date, tasks.terminated FROM tasks JOIN categories ON tasks.category_id = categories.id WHERE status = 'finished' ORDER BY CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 WHEN 'low' THEN 3 END, input_date ASC") # the query is taken from Ai!
    print(tabulate(completed_tasks, headers='keys', tablefmt="grid")) # how to join categories table?
    print(f"{amount[0]['count(*)']} Mission accomplished")


def show_tasks():
    unfinished_tasks = db.execute("SELECT categories.name AS category_name, tasks.task, tasks.description, tasks.estimated_time, tasks.priority, tasks.status, tasks.input_date FROM tasks JOIN categories ON tasks.category_id = categories.id WHERE status = 'unfinished' ORDER BY CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 WHEN 'low' THEN 3 END, input_date ASC") # the query is taken from Ai!
    print(tabulate(unfinished_tasks, headers='keys', tablefmt="grid"))


def update_tasks():
    tasks_table = db.execute("SELECT tasks.id, tasks.task, tasks.description, tasks.estimated_time, tasks.priority, tasks.status FROM tasks ORDER BY CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 WHEN 'low' THEN 3 END, input_date ASC") 
    # Get the task id
    id = []
    for tasks_id in tasks_table:
        temp = int(tasks_id['id'])
        id.append(temp)
    while True:
        print((tabulate(tasks_table, headers='keys', tablefmt="grid")))
        task_id =  input("select the task id: ")
        if task_id.isdigit():
            task_id = int(task_id)
            if task_id in id:   
                break
        print("Invalid input. Please enter the id number!")

    task = db.execute("SELECT tasks.task, tasks.description, tasks.estimated_time, tasks.priority, tasks.status FROM tasks WHERE id = ?", task_id)
    print(tabulate(task, headers='keys', tablefmt="grid"))
    
    # the name of the column that the user wishes to change.
    while True:  
        column =  input("Enter the name of the column you want to change: ").lower()
        if column in ['task', 'description', 'estimated_time', 'priority', 'status']:
            break
        print("Invalid category. Please choose one of the following titles: ('task', 'description', 'estimated_time', 'priority', 'status')")
    
    # obtain the value that the user wants to change.
    if column == 'estimated_time':
        while True:
            changes = input("Enter estimated time to complete the task (in minutes): ")
            if changes.isdigit():
                changes = int(changes)
                break
            print("Invalid input. Please enter a number.")
    elif column == 'priority':
         while True: 
            changes = input("Enter the priority (High / Medium / Low): ").lower()
            if changes in ['high', 'medium', 'low']:
                break
            print("Invalid priority. Please enter High, Medium, or Low.")
    elif column == 'status':
        while True: 
            changes = input("Enter the status (finished / unfinished): ").lower()
            if changes in ['finished', 'unfinished']:
                break
            print("Invalid priority. Please enter status finished or unfinished")
    elif column == 'task':
        changes = input("inter the now Task Title: ")
    elif column == 'description':
        changes = input("inter the now Task description: ")
                
    
    db.execute("update tasks set ? = ? where id = ?", column, changes, task_id)
    task_title = db.execute("select * from tasks where id = ?", task_id)
    print(tabulate(task_title, headers='keys', tablefmt="grid"))
    print(f"The {column} has been changed to '{changes}' successfully!")


def delete_tasks():
    tasks_table = db.execute("SELECT tasks.id, tasks.task, tasks.description, tasks.estimated_time, tasks.priority, tasks.status FROM tasks WHERE status = 'unfinished' ORDER BY CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 WHEN 'low' THEN 3 END, input_date ASC") 
    # Get the task id
    id = []
    for tasks_id in tasks_table:
        temp = int(tasks_id['id'])
        id.append(temp)
    while True:
        print((tabulate(tasks_table, headers='keys', tablefmt="grid")))
        task_id =  input("(DELETE) select the task id: ")
        task_id = int(task_id)
        if task_id in id:   
            break
        print("Invalid input. Please enter the id number!")
    
    task_info = db.execute("SELECT tasks.task, tasks.description, tasks.estimated_time, tasks.priority, tasks.status FROM tasks WHERE id = ?", task_id)
    task = task_info[0]['task']

    while True:
        user_input = input("Are you sure you want to delete the task? (yes/no): ") 
        if user_input.lower() in ["yes", "no", "y", "n"]:
            break
        print("Invalid input. Please enter 'yes' or 'no'.")
    if user_input.lower() in ["yes", 'y']:
            db.execute("delete from tasks where id = ?", task_id)
            print(f"The Task '{task}' has been deleted successfully!")  
    else:
        print("Canceled!")
    

def help():
    print("Available commands:")
    print("ADD - Add a new task")
    print("GET - Get a task")
    print("history - View all completed tasks")
    print("Show - Show unfinished tasks")
    print("UPDATE - Update or Change information in the task") 
    print("DELETE - Delete a task") 
    print("HELP - Show this help message")
    print("EXIT - Exit the program")


# Call the main function
main()
