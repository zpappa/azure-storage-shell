from shlex import split
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azss.abs_command import ShellCommand
from azss.connect import connect
from azss.ls import ls
from azss.cd import cd
from azss.pwd import pwd


def print_usage():
    print("ls - list the current directory")
    print("help - display this message")
    print("exit - exit this application")


available_commands = {
    "exit": ShellCommand(command=exit, help="Exit the shell", args=[]),
    "connect": ShellCommand(command=connect, help="Connect with a connection string", args=["connection_string"]),
    "ls": ShellCommand(command=ls, help="List a directory", args=["-l", "-a", "-t", "-h"]),
    "cd": ShellCommand(command=cd, help="Enter a dircetory", args=["directory"]),
    "pwd": ShellCommand(command=pwd, help="Print working directory", args=[])
}

try:
    while True:
        inp = input("abs> ")
        tokens = split(inp, True)
        if len(tokens) > 0:
            if tokens[0] in available_commands:
                # todo assert args?
                available_commands[tokens[0]].command(*tokens[1:])
            else:
                print("Command not found {0}".format(tokens[0]))
except KeyboardInterrupt as e:
    print("\r\nReceived sigint, exiting")
    exit(1)
