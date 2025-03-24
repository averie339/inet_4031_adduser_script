#!/usr/bin/python3

import os
import re

def main():
    # Ask the user whether to run the script in "dry-run" mode (for simulation) or "normal" mode (for execution).
    dry_run = input("Would you like to run in dry-run mode? (Y/N): ").strip().upper() == 'Y'

    # Request the input file name from the user. This file should contain user data in a specific format.
    input_file = input("Enter the input file name (e.g., create-users.input): ").strip()

    # Open the specified input file for reading user data line by line.
    with open(input_file, 'r') as file:
        for line in file:
            # Skip lines that are comments (start with "#") or don't meet the expected field structure.
            match = re.match("^#", line)
            fields = line.strip().split(':')

            if dry_run:  # Dry-run-specific behavior for previewing actions without executing them.
                if match:  # Ignore lines that are comments.
                    print("Skipping line (comment):", line.strip())
                    continue
                if len(fields) != 5:  # Ensure the line has exactly 5 fields; otherwise, report an error.
                    print("Error: Line does not have enough fields:", line.strip())
                    continue
            else:  # Normal execution mode where actions are performed.
                if match or len(fields) != 5:  # Skip invalid lines or comments.
                    continue

            # Extract user details from the current line: username, password, full name, and group list.
            username = fields[0]
            password = fields[1]
            # `gecos` field includes user information (e.g., full name).
            gecos = "%s %s,,," % (fields[3], fields[2])
            # Groups are separated by commas; handle them as a list.
            groups = fields[4].split(',')

            # Account creation: Add the user account with the extracted information.
            print("==> Creating account for %s..." % (username))
            cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos, username)
            if dry_run:  # If in dry-run mode, only display the command.
                print("[Dry-run] Command to create user:", cmd)
            else:  # In normal mode, execute the command.
                os.system(cmd)

            # Set the user's password using the extracted credentials.
            print("==> Setting the password for %s..." % (username))
            cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password, password, username)
            if dry_run:  # In dry-run mode, simulate the action.
                print("[Dry-run] Command to set password:", cmd)
            else:  # In normal mode, execute the command.
                os.system(cmd)

            # Assign the user to the specified groups unless the group is marked with a '-'.
            for group in groups:
                if group != '-':  # Skip if the group entry is '-'.
                    print("==> Assigning %s to the %s group..." % (username, group))
                    cmd = "/usr/sbin/adduser %s %s" % (username, group)
                    if dry_run:  # In dry-run mode, preview the group assignment command.
                        print("[Dry-run] Command to assign group:", cmd)
                    else:  # In normal mode, execute the group assignment.
                        os.system(cmd)

if __name__ == '__main__':
    main()
