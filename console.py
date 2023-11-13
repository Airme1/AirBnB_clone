#!/usr/bin/python3
import cmd
from models.base_model import BaseModel
from models import storage
import json
import re


class HBNBCommand(cmd.Cmd):
    """The class for the cmd module"""
    prompt = "(hbnb)"

    def do_help(self, arg: str) -> bool | None:
        return super().do_help(arg)

    def do_quit(self, line):
        """To quit program"""
        return True

    def do_emptyline():
        """do nothing when enter is
        pressed on an emmpty line
        """
        pass

if __name__ == '__main__':
    HBNBCommand().cmdloop()