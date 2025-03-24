#!/usr/bin/python3

# INET4031
# Averie Schouten
# 03/18/2025
# 03/23/2025

# The os module is used to execute system commands like creating users or setting passwords.
# The re module is used for regular expression operations, such as pattern matching to process input lines.
# The sys module allows the program to interact with the system and read input from stdin.
import os
import re
import sys

def main():
    for line in sys.stdin:

        # The regular expression checks if a line starts with the character '#'.
	# Lines starting with '#' are treated as comments and should be ignored, as they don't contain user data.
        match = re.match("^#",line)

        # The line is stripped of leading/trailing whitespace, then split by ':' to divide it into separate fields.
	# Each field corresponds to data like username, password, first name, last name, and groups.
        fields = line.strip().split(':')

        # The IF condition checks if the line is a comment (starts with '#') or doesn't have exactly 5 fields.
	# This ensures that only valid data lines are processed. If the condition is met, the line is skipped.
        if match or len(fields) != 5:
            continue

        # These variables extract specific user details from the split fields:
	# - 'username' stores the username.
	# - 'password' stores the password.
	# - 'gecos' combines the first and last name into a single formatted string for the user information in /etc/passwd.
        username = fields[0]
        password = fields[1]
        gecos = "%s %s,,," % (fields[3],fields[2])

        # The groups field is split by commas to create a list of groups the user should be added to.
	# This allows assigning the user to multiple groups in subsequent steps.
        groups = fields[4].split(',')

        # This print statement provides feedback to the user, indicating the account creation process for a specific username.
        print("==> Creating account for %s..." % (username))
        # The 'cmd' variable builds the system command to create a user account with the specified details.
	# It uses '/usr/sbin/adduser' with the GECOS field and the disabled password option.
        cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos,username)

        print(cmd)
        os.system(cmd)

        # This line sets the user's password using the echo and passwd commands.
	# It passes the password twice (for confirmation) to the passwd command for the specified username.
        print("==> Setting the password for %s..." % (username))
        # The `cmd` variable builds a shell command that sets the password for the created user using 'passwd'.
	# The command combines 'echo' to pass the password twice (confirmation) and 'passwd' to apply the password to the user account.
        cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password,password,username)

        print(cmd)
        os.system(cmd)

        for group in groups:
            # The IF condition checks if the group field is not a single hyphen ('-'), which indicates no group.
	    # If the group is valid, the user is assigned to the specified group using the adduser command.
            if group != '-':
                print("==> Assigning %s to the %s group..." % (username,group))
                cmd = "/usr/sbin/adduser %s %s" % (username,group)
                print(cmd)
                os.system(cmd)

if __name__ == '__main__':
    main()
