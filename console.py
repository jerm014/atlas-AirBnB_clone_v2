#!/usr/bin/python3
""" Console Module """
import cmd
import sys
from models.base_model import BaseModel
from models import storage, classes
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    last_value = {
              "User": "None",
              "Place": "None",
              "State": "None",
              "City": "None",
              "Amenity": "None",
              "Review": "None"
              }

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = classes

    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float
            }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ''  # initialize line elements

        # scan for general formating - i.e '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # parse line left to right
            print("parsing line")
            pline = line[:]  # parsed line

            # isolate <class name>
            _cls = pline[:pline.find('.')]

            # isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # if parantheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # pline convert to tuple

                # isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')
                # possible bug here:
                # empty quotes register as empty _id when replaced

                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *args or **kwargs
                    if pline[0] == '{' and pline[-1] == '}' \
                            and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
                        # _args = _args.replace('\"', '')
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception as mess:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_last(self, command):
        """ Method to retrieve last object"""
        if command:
            if command in self.last_value:
                print(f"{command} {self.last_value[command]}")
            else:
                print(f"** Class {command} doesn't exist **")
        else:
            for key, value in self.last_value.items():
                print(f"{key} {value}")

    def help_last(self):
        """ Prints the help documentation for last """
        from uuid import uuid4
        temp_state = str(uuid4())
        temp_city = str(uuid4())
        print("Shows the value(s) of the stored variables\n")
        print("  last [class name]\n")
        print("You can use Tokens in your commands to represent an id for" +
              " a previously create[d] or show[n] object.\n")
        print("For example:\n")
        print("  (hbnb) create State name=\"Texas\"")
        print("  " + temp_state)
        print("  (hbnb) last")
        print("  User =")
        print("  Place =")
        print(f"  State = {temp_state}")
        print("  City =")
        print("  Amenity =")
        print("  Review =")
        print("  (hbnb) create City name=\"Dallas\" state_id=$State")
        print("  " + temp_city)
        print("  (hbnb) last")
        print("  User =")
        print("  Place =")
        print(f"  State = {temp_state}")
        print(f"  City = {temp_city}")
        print("  Amenity =")
        print("  Review =")
        print("  (hbnb) last State")
        print(f"  State = {temp_state}")
        print("  (hbnb) _\n")

    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        exit()

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_link(self, command):
        """ link an amenity to a place """
        args = command.split(" ")
        place_id = amenity_id = None

        for i, v in enumerate(args):
            if '$' in v:
                args[i] = self.last_value[v[1:]]

        for i, v in enumerate(args):
            if str(v).lower() == "place":
                place_id = args[i+1]
            if str(v).lower() == "amenity":
                amenity_id = args[i+1]

        if amenity_id and place_id:
            # print(f"adding {args[0]} ({args[1]}) to {args[2]} ({args[3]})")
            storage.link_amenity(amenity_id, place_id)
        elif amenity_id is None:
            print(" ** invalid Amenity **")
        else:
            print(" ** invalid Place **")

    def help_link(self):
        """ Prints the help documentation for link """
        print("Links an object to another object through a many-to-many " +
              "join.\n")
        print("  link Place <place_id> [to] Amenity <amenity_id>")
        print("  link Amenity <amenity_id> [to] Place <place_id>\n")

    def do_unlink(self, command):
        """ unlink an amenity from a place """
        args = command.split(" ")
        place_id = amenity_id = None

        for i, v in enumerate(args):
            if '$' in v:
                args[i] = self.last_value[v[1:]]

        for i, v in enumerate(args):
            if str(v).lower() == "place":
                place_id = args[i+1]
            if str(v).lower() == "amenity":
                amenity_id = args[i+1]

        if amenity_id and place_id:
            # print(f"removing {args[0]} ({args[1]}) from
            # {args[2]} ({args[3]})")
            storage.unlink_amenity(amenity_id, place_id)
        elif amenity_id is None:
            print(" ** invalid Amenity **")
        else:
            print(" ** invalid Place **")

    def help_unlink(self):
        """ Prints the help documentation for unlink """
        print("Unlinks an object from another object through a many-to-many " +
              "join.\n")
        print("  unlink Place <place_id> [from] Amenity <amenity_id>")
        print("  unlink Amenity <amenity_id> [from] Place <place_id>\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        exit()

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def do_create(self, args):
        """ Create an object of any class"""
        if not args:
            print("** class name missing **")
            return

        args_list = args.split()
        class_name = args_list[0]

        if class_name not in self.classes:
            print(f"** class '{class_name}' doesn't exist**")
            return

        kwargs = {}

        # Parse Parameters
        try:
            for param in args_list[1:]:
                key, value = param.split('=')
                key = key.strip()
                value = value.strip()

                # Handle value types
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1].replace('_', ' ')
                elif '.' in value:
                    value = float(value)
                elif '$' in value:
                    value = self.last_value[value[1:]]
                else:
                    value = int(value)

                kwargs[key] = value

        except ValueError:
            print("** Invalid parameter value **")
            return
        except Exception as e:
            print(f"** Error parsing parameters: {e} **")
            return

        # Create instance and set attributes
        try:
            new_instance = self.classes[class_name](**kwargs)
            new_instance.save()
            print(new_instance.id)
            self.last_value[class_name] = new_instance.id
        except Exception as e:
            print(f"** Error creating instance: {e} **")

    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type")
        print("  create <className> [attribute=value[, ...]]\n")

    def do_show(self, args):
        """ Method to show an individual object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]

        # guard against trailing args
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id

        try:
            print(storage.all(c_name)[key])
            self.last_value[c_name] = c_id
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("  show <className> <objectId>\n")

    def do_delete(self, args):
        self.do_destroy(args)

    def help_delete(self):
        """ Help information for the delete command """
        print("** Delete is a synonym for destory\n")
        self.help_destroy(["Deletes", "delete"])

    def do_destroy(self, args):
        """ Destroys a specified object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id

        try:
            storage.delete(key)
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self, delete=["Destorys","destroy"]):
        """ Help information for the destroy command """
        print(f"{delete[0]} an individual instance of a class\n")
        print(f"  {delete[1]} <className> <objectId>\n")

    def do_all(self, args):
        """ Shows all objects, or all objects of a class"""
        print_list = []

        if args:
            args = args.split(' ')[0]  # remove possible trailing args
            if args not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for k, v in storage.all().items():
                if k.split('.')[0] == args:
                    print(v)
        else:
            for k, v in storage.all().items():
                print(v)

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all objects of a class\n")
        print("  all [className]\n")

    def do_count(self, args):
        """Count current number of class instances"""
        count = 0
        for k, v in storage.all():
            if args == k.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """ """
        print("Counts the number of objects in a class\n")
        print("  count <class_name>\n")

    def do_update(self, args):
        """ Updates a certain object with new info """
        c_name = c_id = att_name = att_val = kwargs = ''

        # isolate cls from id/args, ex: (<cls>, delim, <id/args>)
        args = args.partition(" ")
        if args[0]:
            c_name = args[0]
        else:  # class name not present
            print("** class name missing **")
            return
        if c_name not in HBNBCommand.classes:  # class name invalid
            print("** class doesn't exist **")
            return

        # isolate id from args
        args = args[2].partition(" ")
        if args[0]:
            c_id = args[0]
        else:  # id not present
            print("** instance id missing **")
            return

        # generate key from class and id
        key = c_name + "." + c_id

        # determine if key is present
        if key not in storage.all():
            print("** no instance found **")
            return

        # first determine if kwargs or args
        if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
            kwargs = eval(args[2])
            args = []  # reformat kwargs into list, ex: [<name>, <value>, ...]
            for k, v in kwargs.items():
                args.append(k)
                args.append(v)
        else:  # isolate args
            args = args[2]
            if args and (args[0] == '\"'):  # check for quoted arg
                second_quote = args.find('\"', 1)
                att_name = args[1:second_quote]
                args = args[second_quote + 1:]

            args = args.partition(' ')

            # if att_name was not quoted arg
            if not att_name and (args[0] != ' ' and args[0] != ' '):
                att_name = args[0]
            # check for quoted val arg
            if args[2] and args[2][0] == '\"':
                att_val = args[2][1:args[2].find('\"', 1)]

            # if att_val was not quoted arg
            if not att_val and args[2]:
                att_val = args[2].partition(' ')[0]

            args = [att_name, att_val]

        # retrieve dictionary of current objects
        new_dict = storage.all()[key]

        # iterate through attr names and values
        for i, att_name in enumerate(args):
            # block only runs on even iterations
            if (i % 2 == 0):
                att_val = args[i + 1]  # following item is value
                if not att_name:  # check for att_name
                    print("** attribute name missing **")
                    return
                if not att_val:  # check for att_value
                    print(f"** {att_name} value missing **")
                    return
                # type cast as necessary
                if att_name in HBNBCommand.types:
                    att_val = HBNBCommand.types[att_name](att_val)

                # update dictionary with name, value pair
                setattr(new_dict, att_name, att_val)

        new_dict.save()  # save updates to file

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information\n")
        print("  update <className> <id> [name value[ name value ...]]\n")

    def do_Amenity(self, args):
        """ Stores an Amenity id to $Amenity """
        self.last_value["Amenity"] = args

    def do_Place(self, args):
        """ Stores a Place id to $Place """
        self.last_value["Place"] = args

    def do_State(self, args):
        """ Stores a State id to $State """
        self.last_value["State"] = args

    def do_City(self, args):
        """ Stores a City id to $City """
        self.last_value["City"] = args

    def do_Review(self, args):
        """ Stores a Review id to $Review """
        self.last_value["Review"] = args

    def do_User(self, args):
        """ Stores a User id to $User """
        self.last_value["User"] = args

    def help_Amenity(self):
        print("Stores an Amenity id to $Amenity\n")
        print("  Amenity <id>\n")

    def help_Place(self):
        print("Stores a Place id to $Place\n")
        print("  Place <id>\n")

    def help_State(self):
        print("Stores a State id to $State\n")
        print("  State <id>\n")

    def help_City(self):
        print("Stores a City id to $City\n")
        print("  City <id>\n")

    def help_Review(self):
        print("Stores a Review id to $Review\n")
        print("  Review <id>\n")

    def help_User(self):
        print("Stores a User id to $User\n")
        print("  User <id>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
