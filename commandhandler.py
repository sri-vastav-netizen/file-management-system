"""
This program handles the commands
passed by the client to server.
"""

import pathlib
import os
import time
from shutil import rmtree
import csv
import pandas


class CommandHandler():
    """
    Handles all the commands received from the client.
    Acts as helper program to the server.

    Returns
    -------
    Object
        CommandHandler Object    
    """

    ROOT_DIR = "Root/"
    REGISTERED_USERS_CSV_FILE = "AccessSession/registered_users.csv"
    LOGGED_IN_USERS_CSV_FILE = "AccessSession/logged_in_users.csv"
    CSV_HEADING = "username,password\n"

    def __init__(self):

        self.user_id = ""
        self.is_login = None
        self.registered_users = None
        self.logged_in_users = None
        self.current_dir = CommandHandler.ROOT_DIR
        self.read_index = {}
        self.char_count = 100

    def commands(self):
        commands = ["""register : To register as a new user ,
                    command:register <username> <password> \n""",
                    """login : To login , 
                    command:login <username> <password>""",
                    """quit : To logout, 
                    command:quit\n""",
                    """change_folder : To change the current path, 
                    command:change_folder <name>\n""",
                    """list : Lists all files in the current path, 
                    command:list\n""",
                    """read_file : To read content from the file, 
                    command:read_file <name>\n""",
                    """write_file : To write content into the file, 
                    command:write_file <name> <content>\n""",
                    """create_folder : To create new folder, 
                    command:create_folder <name>\n"""
                ]

        return "".join(commands)

    def access_user_info(self):
        if not os.path.exists("AccessSession"):
            os.mkdir("AccessSession")

        if not os.path.isfile(CommandHandler.REGISTERED_USERS_CSV_FILE):
            with open(CommandHandler.REGISTERED_USERS_CSV_FILE, "w") as writer:
                writer.write(CommandHandler.CSV_HEADING)
        if not os.path.isfile(CommandHandler.LOGGED_IN_USERS_CSV_FILE):
            with open(CommandHandler.LOGGED_IN_USERS_CSV_FILE, "w") as writer:
                writer.write(CommandHandler.CSV_HEADING)
        self.logged_in_users = pandas.read_csv(CommandHandler.LOGGED_IN_USERS_CSV_FILE)
        self.registered_users = pandas.read_csv(CommandHandler.REGISTERED_USERS_CSV_FILE)


    def register(self, user_id, password):

        self.access_user_info()
        if user_id in self.registered_users['username'].tolist():
            return "\nUsername not available"
        if len(password) < 8:
            return "\n Password length should be more than 8 characters."
        with open(CommandHandler.REGISTERED_USERS_CSV_FILE, "a") as writer:
            writer.write(user_id+","+password+"\n")
        if not os.path.exists(self.current_dir):
            os.mkdir(self.current_dir)
        os.mkdir(os.path.join(self.current_dir, user_id))

        self.current_dir = self.current_dir + user_id
        self.user_id = user_id
        return "\nSuccess! Registered " + self.user_id

    def login(self, user_id, password):

        self.access_user_info()
        if self.is_login:
            return "\nAlready Logged In"
        if user_id not in self.registered_users['username'].tolist():
           # print (self.registered_users)
            return "\nYou haven't registered! Please register--> command: register <username> <password>"
        if password not in self.registered_users['password'].tolist() and user_id in self.registered_users['username'].tolist():
            return "\nSorry, The password you entered is wrong. Please Try Again"
        if user_id in self.logged_in_users['username'].tolist():
            self.is_login = True
            self.user_id = user_id
            self.current_dir = self.current_dir + self.user_id
            return "\nYou logged through another system"
        
        self.is_login = True
        self.user_id = user_id
        self.current_dir = self.current_dir + self.user_id
        with open(CommandHandler.LOGGED_IN_USERS_CSV_FILE, "a") as writer:
            writer.write(user_id + "," + password + "\n")
        return "Success " + self.user_id + " Logged into the system"




    