"""
PY-DOS
Made by DeBeast591
(C) 2020 DeBeast591
Enjoy!
* SYS REQUIREMENTS *
- Python 3.7<=
- TERMINAL!!!
- Nano
* MODULES *
- OS
"""

# Imports
import os

# Paths
PATH = str(os.getcwd())
REL_DATA_PATH = PATH + "/data/"
MAIN_FILES = PATH + "/DRIVES/"

# Version
with open(REL_DATA_PATH + "version.txt") as VERSION:
    version = VERSION.readlines()
    version = " ".join(version)
    version = version.split()
    version = ".".join(version)

# Config
def config():
    global show_stats, ask_for_drives, allow_config_edits, CONFIG, input_marker, primary_drive
    with open(REL_DATA_PATH + "config.txt") as FILE:
        CONFIG = FILE.readlines()
        """
        Config Syntax:
        CONFIG
        {STRING: input marker}
        {STRING: primary drive}
        {BOOL: show stats?}
        {BOOL: ask what drive to use?}
        {BOOL: allow config file edits?}
        """

    # Config variables (String)
    input_marker = CONFIG[1]
    input_marker = input_marker.replace("\n", "")
    primary_drive = CONFIG[2]

    # Config Variables (Bool)
    if CONFIG[3] in ["true", "true\n"]: show_stats = True
    else: show_stats = False
    if CONFIG[4] in ["true", "true\n"]: ask_for_drives = True
    else: ask_for_drives = False
    if CONFIG[4] in ["true", "true\n"]: allow_config_edits = True
    else: allow_config_edits = False

# Start Code
config()
print("PyDOS VERSION " + version)
OUTSIDE_DRIVE = False

# Password
def password():
    with open(PATH + "/DRIVES/" + ACTIVE_DRIVE + "/drive_config.txt") as FILE:
        temp_file = FILE.readlines()
    # if there is a password
    if temp_file[2] in ["true", "true\n"]:
        password = input("Drive Password: ")
        if password == temp_file[3]:
            print("Permission to drive granted.")
            return True
        else:
            # does a newline (\n) exist after the line in config?
            password = password + "\n"
            if password == temp_file[3]:
                print("Permission to drive granted.")
                return True
            else:
                print("Password wrong.")
                return False
    else: return True

# Ask For Drive
if ask_for_drives:
    # looooping
    while True:
        ACTIVE_DRIVE = str(input("Select a drive:\n"))
        CURRENT_DRIVE = ACTIVE_DRIVE
        if os.path.exists(PATH + "/DRIVES/" + ACTIVE_DRIVE):
            MAIN_FILES = PATH + "/DRIVES/" + ACTIVE_DRIVE
            while not password(): continue
            break
        else: print("E: Drive does not exist.")
else:
    ACTIVE_DRIVE = primary_drive
    if "\n" in ACTIVE_DRIVE:
        ACTIVE_DRIVE = ACTIVE_DRIVE.strip("\n")
        primary_drive = primary_drive.strip("\n")
    MAIN_FILES = PATH + "/DRIVES/" + ACTIVE_DRIVE

# Drive Config
MODE = "NULL"
def drive_config():
    global DRIVE_CONFIG, MODE, allow_drive_config_edits
    with open(PATH + "/DRIVES/" + ACTIVE_DRIVE + "/drive_config.txt") as FILE:
        DRIVE_CONFIG = FILE.readlines()
        """
        Drive Config Syntax:
        DRIVE CONFIG
        {STRING: mode}
        {BOOL: password?}
        {STRING: password}
        {BOOL: allow drive config edits?}
        """
    if DRIVE_CONFIG[1] in ["read-only", "read-only\n"]: MODE = "READ_ONLY"
    elif DRIVE_CONFIG[1] in ["read-write", "read-write\n"]: MODE = "READ_WRITE"
    else: MODE = "READ_ONLY"
    if DRIVE_CONFIG[4] in ["true", "true\n"]: allow_drive_config_edits = True
    elif DRIVE_CONFIG[4] in ["false", "false\n"]: allow_drive_config_edits = False
    else: allow_drive_config_edits = False

# Command Check
def command_check(command_length, true_command_length):
    if len(command_length) != true_command_length:
        print("E: Command too short or long, type 'help' to see the command syntax.")
        return True
    else: return False

# Main Code
drive_config()
RunningPyDOSFile = False
PDFILE_LOCATION = 0
PDFILE = []
PDFILE_FILE_LOCATION = None
while True:

    # if user is outside drive
    if OUTSIDE_DRIVE:
        ACTIVE_DRIVE = CURRENT_DRIVE
        CURRENT_DRIVE = ACTIVE_DRIVE
        MAIN_FILES = MAIN_FILES + ACTIVE_DRIVE
        # Drive Reconfigure
        drive_config()

    # awaiting user input
    if RunningPyDOSFile:
        if int(PDFILE_LOCATION) != len(PDFILE):
            action = PDFILE[PDFILE_LOCATION].split()
            PDFILE_LOCATION += 1
        else:
            RunningPyDOSFile = False
            show_stats = True
            pass
    else:
        action = input(ACTIVE_DRIVE + input_marker).split()

    # help
    if action[0] == "help":
        if not command_check(action, 1):
            print("PyDOS Help:")
            print("NOTE: Printed in order from where they are in the source code")
            print("NOTE: Some commands are blocked by read/only drives\n")
            print("help - prints help")
            print("lf - prints all folders and files in the active folder")
            print("ld - prints all drives")
            print("ls - lists files, folders, and drives (only lists files and folders in the active drive)")
            print("end {OPTIONAL_FLAG} - terminates PyDOS")
            print("\t-y - auto-ends the session without asking")
            print("open {FLAG} {FILE} - opens a file and runs it or prints it's contents")
            print("\t-print - prints contents")
            print("\t-run - runs the file (in Python)")
            print("\t-pd - runs the file (in PyDOS)")
            print("cd {ACTION}")
            print("\t.. - goes up one folder")
            print("\t-d - changes the active drive")
            print("\t{FOLDER} - goes into the folder")
            print("mk {FLAG} {NAME} - makes folders, files, etc. Can also edit files")
            print("\t-dir - makes a dir")
            print("\t-folder - makes a dir")
            print("\t-file - makes a file and edits using Nano")
            print("\t-drive - makes a drive")
            print("del {FILE} - deletes a file (moves it to DRIVES/.trash/)")
            print("config {FLAG} - edits config")
            print("\t-main - main config")
            print("\t-drive - drive config")
            print("sleep - waits untill a key is pressed")
            print("reload - reloads the config and drive config")
            print("echo {ANY_STRING} - prints the '{ANY_STRING}'")
            print("cls - clears the screen")
            print("contition {TYPE} {SAY} {WANTED_INPUT} {TRUE_OUTPUT} {FALSE_OUTPUT} - true / false")
            print("\tTYPES:")
            print("\t\tinput - gets user input")
            print("\t\toutput - get the last output (TRUE/FALSE OUTPUT)")
            print("\tNOTES:")
            print("\t\t{WANTED_INPUT} - not required for the output type")
            print("etrash - emptys the trash (DRIVES/.trash/)")

    # lists all files/folders
    elif action[0] == "lf":
        if not command_check(action, 1):
            files = os.listdir(PATH + "/DRIVES/" + ACTIVE_DRIVE)
            for x in files:
                print(x)

    # lists all drives
    elif action[0] == "ld":
        if not command_check(action, 1):
            drives = os.listdir(PATH + "/DRIVES/")
            for x in drives:
                print(x)
    
    # lists all folders, files, and drives
    elif action[0] == "ls":
        if not command_check(action, 1):
            drives = os.listdir(PATH + "/DRIVES/")
            print("Drives: ")
            for x in drives:
                print(x)
            print("\nFolders and Files:")
            files = os.listdir(PATH + "/DRIVES/" + ACTIVE_DRIVE)
            for x in files:
                print(x)

    # terminates PY-DOS
    elif action[0] == "end":
        if not command_check(action, len(action)):
            if len(action) == 2:
                if action[1] == "-y":
                    quit()
            else:
                if input("Are you sure you want to end this session? (y/n)\n\t") == "y": quit()
                else: print("Abort")

    # opens files
    elif action[0] == "open":
        if not command_check(action, 3):
            # prints files
            if os.path.exists(PATH + "/DRIVES/" + ACTIVE_DRIVE + "/" + action[2]):
                if action[1] == "-print":
                    with open(PATH + "/DRIVES/" + ACTIVE_DRIVE + "/" + action[2]) as temp_file:
                        for x in temp_file.readlines():
                            print(x, end="")
                elif action[1] == "-run":
                    if MODE == "READ_ONLY": print("E: This is a read only drive.")
                    else: os.system("python3 " + PATH +"/DRIVES/" + ACTIVE_DRIVE + "/" + action[2])
                elif action[1] == "-pd":
                    if MODE == "READ_ONLY": print("E: This is a read only drive.")
                    else:
                        RunningPyDOSFile = True
                        PDFILE_LOCATION = 0
                        PDFILE = []
                        PDFILE_FILE_LOCATION = open(PATH + "/DRIVES/" + ACTIVE_DRIVE + "/" + action[2])
                        PDFILE_FILE_LOCATION = PDFILE_FILE_LOCATION.readlines()
                        for x in PDFILE_FILE_LOCATION:
                            PDFILE.append(str(x))
            else: print("E: File does not exist.")

    # chages active dir
    elif action[0] == "cd":
        # cd to drives
        if action[1] == "-d":
            if not command_check(action, 3):
                if os.path.exists(PATH + "/DRIVES/" + action[2]):
                    if "/" in ACTIVE_DRIVE:
                        print("E: You must be in the root of the drive to use this command.")
                    else:
                        # Password
                        with open(PATH + "/DRIVES/" + action[2] + "/drive_config.txt") as FILE:
                            temp_file = FILE.readlines()
                        # if there is a password
                        if temp_file[2] in ["true", "true\n"]:
                            password = input("Drive Password: ")
                            if password == temp_file[3]:
                                print("Permission to drive granted.")
                                MAIN_FILES = MAIN_FILES + action[2]
                                ACTIVE_DRIVE = action[2]
                                CURRENT_DRIVE = ACTIVE_DRIVE
                                # Drive Reconfigure
                                drive_config()
                            else:
                                # does a newline (\n) exist after the line in config?
                                password = password + "\n"
                                if password == temp_file[3]:
                                    print("Permission to drive granted.")
                                    MAIN_FILES = MAIN_FILES + action[2]
                                    ACTIVE_DRIVE = action[2]
                                    CURRENT_DRIVE = ACTIVE_DRIVE
                                    # Drive Reconfigure
                                    drive_config()
                                else: print("Password wrong.")
                        else:
                            MAIN_FILES = MAIN_FILES + action[2]
                            ACTIVE_DRIVE = action[2]
                            CURRENT_DRIVE = ACTIVE_DRIVE
                            # Drive Reconfigure
                            drive_config()
            else: print("Drive does not exist.")
        # go up in folder tree
        elif action[1] == "..":
            if not command_check(action, 2):
                LOCATION = str(os.getcwd())
                OUTSIDE_DRIVE = False
                if ACTIVE_DRIVE == "" or " " or "/":
                    OUTSIDE_DRIVE = True
                ACTIVE_DRIVE = ACTIVE_DRIVE.split("/")
                del ACTIVE_DRIVE[-1]
                ACTIVE_DRIVE = "/".join(ACTIVE_DRIVE)
        # move down in folder tree
        elif os.path.exists(PATH + "/DRIVES/" + ACTIVE_DRIVE + "/" + action[1]):
            if command_check(action, 2) == False:
                ACTIVE_DRIVE = ACTIVE_DRIVE + "/" + action[1]
                if "/DRIVES/" in ACTIVE_DRIVE: OUTSIDE_DRIVE = True
                else: OUTSIDE_DRIVE = False
        else: print("Folder does not exist.")

    # makes a dir or file (can also edit files)
    elif action[0] == "mk":
        if not command_check(action, 3):
            if MODE == "READ_ONLY": print("E: This is a read only drive.")
            else:
                if action[1] in ["-dir", "-folder"]:
                    os.system("mkdir " + PATH + "/DRIVES/" + ACTIVE_DRIVE + "/" + action[2])
                elif action[1] == "-file":
                    if action[2] == "drive_config.txt": print("E: Use 'config -drive' to edit the config file.")
                    else: os.system("nano " + PATH + "/DRIVES/" + ACTIVE_DRIVE + "/" + action[2])

    # deletes a dir and puts it in the trash
    elif action[0] == "del":
        if not command_check(action, 2):
            if MODE == "READ_ONLY": print("E: This is a read only drive.")
            else: os.system("mv " + PATH + "/DRIVES/" + ACTIVE_DRIVE + "/" + action[1] + " " + PATH + "/DRIVES/.trash/")

    # config
    elif action[0] == "config":
        if not command_check(action, 2):
            if action[1] == "-main":
                if allow_config_edits: os.system("nano " + PATH + "/data/config.txt")
                else: print("E: Config edits are blocked.")
            elif action[1] == "-drive":
                if allow_drive_config_edits: os.system("nano " + PATH + "/DRIVES/" + ACTIVE_DRIVE + "/drive_config.txt")
                else: print("E: Drive config edits are blocked.")

    # config and drive config reload
    elif action[0] == "reload":
        if not command_check(action, 1):
            config()
            drive_config()

    # sleep
    elif action[0] == "sleep":
        if not command_check(action, 1):
            action = input(input_marker)
            hide_stat = True

    # echo
    elif action[0] == "echo":
        if not command_check(action, len(action)):
            action.remove("echo")
            action = " ".join(action)
            print(action)

    # cls
    elif action[0] == "cls":
        if not command_check(action, 1):
            os.system("clear")
    
    # conditions
    elif action[0] == "condition":
        if not command_check(action, 1):
            # gets user input and tests
            if action[1] == "input":
                if input(action[2] + input_marker) == action[3]:
                    CONDITION_OUTPUT = action[4]
                else:
                    CONDITION_OUTPUT = action[5]
            # gets the previous condition's output and tests
            elif action[1] == "output":
                if CONDITION_OUTPUT == action[2]:
                    CONDITION_OUTPUT = action[3]
                    print(action[3])
                else:
                    CONDITION_OUTPUT = action[4]
                    print(action[4])
    
    # empty trash
    elif action[0] == "etrash":
        if not command_check(action, 1):
            if MODE == "READ_WRITE":
                if input("Are you sure, this CAN NOT be undone? (y/n) ") == "y":
                    os.system("rm -rf " + PATH + "/DRIVES/.trash/*")
                else:
                    print("Abort")
            else: print("E: This is a read only drive.")
    
    # error
    else:
        print("E: Command does not exist.")

    # show stats
    if show_stats:
        if not RunningPyDOSFile: print("\n[STATS] Executed")
