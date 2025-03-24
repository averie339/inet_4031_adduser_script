#!/usr/bin/python3

import os
import re

def main():
    # Prompt the user to choose whether to run in "dry-run" mode (Y) or "normal" mode (N).
    dry_run = input("Would you like to run in dry-run mode? (Y/N): ").strip().upper() == 'Y'

    # Prompt the user for the input file name
    input_file = input("Enter the input file name (e.g., create-users.input): ").strip()

    # Open the input file
    with open(input_file, 'r') as file:
        for line in file:
            # Check if the line is a comment or invalid
            match = re.match("^#", line)
            fields = line.strip().split(':')

            if dry_run:  # Dry-run-specific behavior
                if match:
                    print("Skipping line (comment):", line.strip())
                    continue
                if len(fields) != 5:
                    print("Error: Line does not have enough fields:", line.strip())
                    continue
            else:  # Normal mode
                if match or len(fields) != 5:
                    continue

            # Extract user details
            username = fields[0]
            password = fields[1]
            gecos = "%s %s,,," % (fields[3], fields[2])
            groups = fields[4].split(',')

            # Account creation
            print("==> Creating account for %s..." % (username))
            cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos, username)
            if dry_run:
                print("[Dry-run] Command to create user:", cmd)
            else:
                os.system(cmd)

            # Set password
            print("==> Setting the password for %s..." % (username))
            cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password, password, username)
            if dry_run:
                print("[Dry-run] Command to set password:", cmd)
            else:
                os.system(cmd)

            # Assign groups
            for group in groups:
                if group != '-':
                    print("==> Assigning %s to the %s group..." % (username, group))
                    cmd = "/usr/sbin/adduser %s %s" % (username, group)
                    if dry_run:
                        print("[Dry-run] Command to assign group:", cmd)
                    else:
                        os.system(cmd)

if __name__ == '__main__':
    main()
