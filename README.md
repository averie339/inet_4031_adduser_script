# INET4031 Add Users Script and User List
# Program Description
This script is designed to automate the process of adding users, setting their passwords, and assigning them to groups on a Linux system. Normally, this task involves manually running commands like adduser, passwd, and adduser <username> <group> for each user. This can be time-consuming and error-prone when dealing with multiple users.

The script simplifies this process by reading user information from an input file and automating these commands. It ensures users are created, passwords are set, and group assignments are completed seamlessly. By using this script, administrators can reduce errors and save time compared to manually performing these steps.

# Program User Operation
This section outlines the steps required to operate the script effectively. By following these instructions, users can set up accounts and groups with minimal effort.

# Input File Format
The input file should contain one line per user, with fields separated by colons (:) in the following format:

username:password:last_name:first_name:groups

* username: The user's login name.
* password: The password for the user account.
* last_name: The user's last name.
* first_name: The user's first name.
* groups: A comma-separated list of groups the user should be added to. Use - if no groups are required.

Example:

user01:securepwd:Doe:John:group01,group02

user02:anotherpwd:Smith:Jane:-

#This is a comment line and will be ignored

To skip a line, start it with a # (e.g., a comment). To omit group assignments for a user, use - in the groups field.

# Command Execution
Make the Script Executable Before running the script, ensure it is executable by running:

chmod +x create-users.py

Run the Script Execute the script with the input file as follows:

./create-users.py < create-users.input

This runs the script and processes user data from the input file.

# "Dry Run"
Before running the script for real, perform a "dry run" to ensure there are no errors. A dry run simulates the process without actually modifying the system.

1. Comment out all os.system(cmd) lines in the script to prevent execution.
2. Run the script:

./create-users.py < create-users.input

This will print the commands that would be executed, allowing you to verify their correctness.

By performing a dry run, you can catch errors early and ensure the script is configured properly. After confirming the output, uncomment the os.system(cmd) lines to execute the commands for real.
