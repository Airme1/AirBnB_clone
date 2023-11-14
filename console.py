#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    brace = re.search(r"/{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if brace is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:brace.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(brace.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter.
    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Do nothing on empty line."""
        pass

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        m_dict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        similar = re.search(r"\.", arg)
        if similar is not None:
            argl = [arg[:similar.span()[0]], arg[similar.span()[1]:]]
            similar = re.search(r"\((.*?)\)", argl[1])
            if similar is not None:
                command = [argl[1][:similar.span()[0]], similar.group()[1:-1]]
                if command[0] in m_dict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return m_dict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """cmd to leave the program."""
        return True

    def do_EOF(self, arg):
        """EOF to leave the program."""
        print("")
        return True

    def do_create(self, arg):
        """
        Create new class instance and print its id.
        """
        argl = parse(arg)
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(argl[0])().id)
            storage.save()

    def do_show(self, arg):
        """
        Display the string representation of a class instance of a given id.
        """
        argl = parse(arg)
        object_dict = storage.all()
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argl[0], argl[1]) not in object_dict:
            print("** no instance found **")
        else:
            print(object_dict["{}.{}".format(argl[0], argl[1])])

    def do_destroy(self, arg):
        """
        Delete a class instance of a given id."""
        argl = parse(arg)
        object_dict = storage.all()
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argl[0], argl[1]) not in object_dict.keys():
            print("** no instance found **")
        else:
            del object_dict["{}.{}".format(argl[0], argl[1])]
            storage.save()

    def do_all(self, arg):
        """
        Display string representations of all instances of a given class.
        """
        argl = parse(arg)
        if len(argl) > 0 and argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(argl) > 0 and argl[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(argl) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def do_count(self, arg):
        """
        Retrieve number of instances for a class."""
        argl = parse(arg)
        count = 0
        for obj in storage.all().values():
            if argl[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """Usage:
        Update a class instance of a given id by adding or updating
        """
        argl = parse(arg)
        object_dict = storage.all()

        if len(argl) == 0:
            print("** class name missing **")
            return False
        if argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(argl) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(argl[0], argl[1]) not in object_dict.keys():
            print("** no instance found **")
            return False
        if len(argl) == 2:
            print("** attribute name missing **")
            return False
        if len(argl) == 3:
            try:
                type(eval(argl[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(argl) == 4:
            obj = object_dict["{}.{}".format(argl[0], argl[1])]
            if argl[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[argl[2]])
                obj.__dict__[argl[2]] = valtype(argl[3])
            else:
                obj.__dict__[argl[2]] = argl[3]
        elif type(eval(argl[2])) == dict:
            obj = object_dict["{}.{}".format(argl[0], argl[1])]
            for key, val in eval(argl[2]).items():
                if (key in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[key]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[key])
                    obj.__dict__[key] = valtype(val)
                else:
                    obj.__dict__[key] = val
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()