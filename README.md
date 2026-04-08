# "Gap Filler" (Smart task Memo):

#### Video Demo:  <URL: https://youtu.be/w70onzzy51Y>
#### Description:

# Program definition:

The program includes several features for organizing tasks during off-peak free time, a time when it's difficult to find a suitable task that fits within the available free time. The application is flexible, so the user is not bound by a fixed schedule for tasks.

# The language and libraries used in the program:  
## The program was built using Python and 3 additional libraries:

1. sys 
2. SQL from the library cs50

3.datetime from the library datetime  
4. tabulate from the library tabulate 

The database program used is SQLite3  

# Tables used in the program:

1. The tasks contains the task ID, task name, task description, task priority, estimated time to complete the task, task recording time, task completion time, task status, and the ID number (FOREIGN KEY (category_id) REFERENCES categories(id)) for classifying the task (from the categories table).

2. The categories contains the names of the categories and the ID for each category.

# Functions in the program:

1. main
2. add_tasks
3. get_tasks
4. history_tasks
5. show_tasks
6. update_tasks
7. delete_tasks
8. help

# ** How the program works (Features):**

* The user enters the tasks and information for each task: task name, task description, task category (there are six categories), estimated time to complete the task, task priority (there are three levels of importance: High, Medium, Low) by typing the command add. (Some information is mandatory, some can be filled in automatically (by default if left blank), and some is optional.) *

* If the user wants to modify the information for a specific task, they can edit the task name, description, estimated time, importance, or status (finished or unfinished). To edit tasks, the user types the command `update` in the command prompt. *

* If the user wants to get a task, the user enters the command get in the command prompt. Then, the program asks them to enter the available time. The program selects the task based on importance, then time , and the date of task registration. The program displays the task and asks the user if they want to do it. If they want that, the task status is changed to finished and it prints the sentence: 'Great! You have selected the task: [task name]'. But if the user rejects that task, the program selects another task based on the priorities we mentioned. *

* The user can view the history of completed tasks by typing the command history in the command prompt. The program displays a Formatted table of completed tasks and the information for each task. *

* The user can also view Active Tasks by typing the command show in the command prompt. The program displays a formatted table of unfinished tasks and the information for each task as well. *

* There is a feature to delete a task if the user wants that, by typing the command delete in the command prompt, then choosing the unique ID number of the task they want to delete, and after confirming the deletion, the task is deleted from the table. *

* The user can see all the commands used in the program and their functionalities by typing the command 'help' in the command prompt. *


# Academic Honesty:

In this project, artificial intelligence was used. The places where I derived some codes and ideas can be seen next to the line of code that I copied or modified from Gemini. 

The table format (tasks & categories) was also improved by Gemini. 

I also want to note that the project name and some of its operating methods were suggestions from Gemini; other than that, the planning, code style, etc., is My own original work.