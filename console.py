#!/usr/bin/python3
"""Module for command line interpreter for models
"""

from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.engine.file_storage import FileStorage
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import cmd


class HBNBCommand(cmd.Cmd):
    """start point of the cmd interpreter
    """
    prompt = "(hbnb)"
    __classes = {
            "BaseModel": BaseModel,
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review,
            }
    objects = storage.all()

    def do_EOF(self, line):
        """EOF command to exit the program
        """
        return True

    def do_quit(self, line):
        """Quit command to exit the program
        """
        return True

    def do_emptyline(self):
        """do nothing when an empty line is inputed
        """
        pass
    
    def postloop(self):
        """do nothing after each console loop
        """
        pass

    def do_create(self, lines):
        """create a new instance of a class
        """
        line = lines.split()
        if not HBNBCommand.check_class(line):
            return
        cls = line[0]
        new_instance = eval(cls + "()")
        new_instance.save()
        print(new_instance.id)

    def do_show(self, args):
        """print string representation of instance
        """
        arg = args.split()
        if not HBNBCommand.check_class(arg):
            return
        if not HBNBCommand.check_id(arg):
            return
        key = "{}.{}".format(arg[0], arg[1])
        print(HBNBCommand.objects[key])

    def do_destroy(self, args):
        """delete an instance based on class name and id
        """
        arg = args.split()
        if not HBNBCommand.check_class(arg):
            return
        if not HBNBCommand.check_id(arg):
            return
        key = "{}.{}".format(arg[0], arg[1])
        del HBNBCommand.objects[key]
        storage.save()

    def do_all(self, arg):
        """print the string representation of all instances
        based or not on class name
        """
        str_lst = []
        if len(arg) > 0:
            args = arg.split()
            if not HBNBCommand.check_class(args):
                return
            cls = args[0]
            for key, instance in HBNBCommand.objects.items():
                if cls in key:
                    str_lst.append(str(instance))
        else:
            for idx, instance in HBNBCommand.objects.items():
                str_lst.append(str(instance))
        print(str_lst)

    def do_update(self, arg):
        """update instances
        """
        args = arg.split()
        if "\"" in args[1] or "\"" in args[2]:
            args[1], args[2], args[3] = args[1].strip("\""),\
            args[2].strip("\""), args[3].strip("\"")
        if not HBNBCommand.check_class(args):
            return
        if not HBNBCommand.check_id(args):
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        attr_name = args[2]
        attr_value = str(args[3])
        if attr_value.isdigit():
            attr_value = int(args[3])
        elif attr_value.replace(".", "", 1).isdigit() and\
                attr_value.count(".") < 2:
            attr_value = float(args[3])
        key = "{}.{}".format(args[0], args[1])
        instance = HBNBCommand.objects[key]
        setattr(instance, attr_name, attr_value)
        instance.save()

    def default(self, args):
        """called when the inputted command starts
        with a class name.
        """
        line = args.split("(")
        cmd = line[0].split(".")[1]
        if cmd == 'all':
            HBNBCommand.do_all(self, line[0].split(".")[0])
        elif cmd == 'count':
            count = 0
            for k in HBNBCommand.objects.keys():
                key = k.split('.')
                if line[0].split(".")[0] == key[0]:
                    count += 1
            print(count)
            return
        elif cmd == "show":
            cls = line[0].split(".")[0]
            id = line[1].strip(')')
            HBNBCommand.do_show(self, cls + " " + id)
            return
        elif cmd == "destroy":
            cls = line[0].split(".")[0]
            id = line[1].strip(')')
            HBNBCommand.do_destroy(self, cls + " " + id)
            return
        elif cmd ==  "update":
            temp = line[1].strip(')').split(",")
            HBNBCommand.do_update(self, line[0].split(".")[0] + " " +\
                                   temp[0] + " " + temp[1] + " " + temp[2])

    def check_class(args):
        """if a class was passed and exists
        """
        if len(args) < 1:
            print("** class name missing **")
            return False
        cls = args[0]
        if cls not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return False
        return True

    def check_id(arg):
        """checks that id was passed and id exists
        """
        if len(arg) < 2:
            print("** instance id missing **")
            return False
        id = arg[1]
        cls = arg[0]
        key = "{}.{}".format(cls, id)
        if key not in HBNBCommand.objects:
            print("** no instance found **")
            return False
        return True


if __name__ == "__main__":
    HBNBCommand().cmdloop()
