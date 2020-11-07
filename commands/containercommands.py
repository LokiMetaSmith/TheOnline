from evennia import Command
from evennia.utils.utils import inherits_from
from evennia import InterruptCommand
from typeclasses.exits import Door
from typeclasses.objects import Container
from evennia import default_cmds


class CmdPutObject(Command):
    """
    Put an object into a container

    Usage: put <object> in <container>
    
    """
    key = "put"
    aliases = "place"
    arg_regex = r"\s|$"
    lock = "cmd:all()"
    help_category = "General"

    def func(self):
        caller = self.caller
        if not self.args:
            caller.msg(f"|yWhat are you trying to put?")
            return
        args = self.args.lstrip()
        try:
            obj, cont = args.split(" in ", 1)
        except ValueError:
            caller.msg(f"|yInvalid usage.  Use 'put <object> in <container>', including the 'in' and spaces separating the two objects.")
            return
        try:
            conts = caller.search(cont, quiet=True)
            cont = conts[0]
        except IndexError:
            caller.msg(f"|yWhat container are you referring to?")
            return
        try:
            objs = caller.search(obj, quiet=True)
            obj = objs[0]
        except IndexError:
            caller.msg(f"|yWhat are you trying to put in the %s?" % cont)
            return
        if not cont.db.container == True:
            caller.msg(f"|yYou cannot put anything inside that!")
            return
        if not cont.db.open == True:
            caller.msg(f"|yYou must open the %s first!" % cont)
            return
        if not obj.location == caller:
            caller.msg(f"|yYou must pick up the %s first!" % obj)
            return
        if obj.db.equipped == True:
            caller.msg(f"|yYou must unequip the %s first!" % obj)
            return
        obj.move_to(cont, location=cont, quiet=True)
        message = "%s put%s the %s into the %s."
        caller.msg(message % ("You", "", obj, cont))
        caller.location.msg_contents(message % (caller.key, "s", obj, cont), exclude=caller)


class CmdGetObject(default_cmds.CmdGet):
    __doc__ = default_cmds.CmdGet.__doc__
    """
    Get an object from a container

    Usage: get <object> from <container>

    """
    key = "get"
    aliases = "remove"
    lock = "cmd:all()"
    arg_regex = r"\s|$"
    help_category = "General"

    def func(self):
        caller = self.caller
        if not self.args:
            caller.msg(f"|yWhat are you trying to get?")
            return
        args = self.args.lstrip()
        try:
            obj, cont = args.split(" from ", 1)
        except ValueError:
            obj = args
            cont = None
        if cont == None:
            try:
                objs = caller.search(obj, quiet=True)
                obj = objs[0]
            except IndexError:
                caller.msg(f"|yWhat item are you referring to?")
                return
            if caller == obj:
                caller.msg(f"|yYou can't get yourself!")
                return
            if not obj.access(caller, "get"):
                if obj.db.get_err_msg:
                    caller.msg(obj.db.get_err_msg)
                else:
                    caller.msg(f"|yYou can't pick that up.")
                return
            if not obj.at_before_get(caller):
                return
            if obj.location == caller:
                caller.msg(f"|yThe %s is already in your inventory!" % obj)
                return
            obj.move_to(caller, quiet=True)
            obj.at_get(caller)
            message = "%s pick%s up the %s."
            caller.msg(message % ("You", "", obj))
            caller.location.msg_contents(message % (caller.key, "s", obj), exclude=caller)
        else:
            try:
                conts = caller.search(cont, quiet=True)
                cont = conts[0]
            except IndexError:
                caller.msg(f"|yWhat container are you referring to?")
                return
            try:
                objs = cont.search(obj, quiet=True)
                obj = objs[0]
            except IndexError:
                try:
                    objs = caller.search(obj, quiet=True)
                    obj = objs[0]
                except IndexError:
                    caller.msg(f"|yWhat item are you referring to?")
                    return
            if not cont.db.open == True:
                caller.msg(f"|yYou must open the %s first!" % cont)
                return
            if not obj.location == cont:
                caller.msg(f"|yThe %s is not in the %s!" % (obj, cont))
                return
            obj.move_to(caller, location=caller, quiet=True)
            obj.at_get(caller)
            message = "%s get%s the %s from the %s."
            caller.msg(message % ("You", "", obj, cont))
            caller.location.msg_contents(message % (caller.key, "s", obj, cont), exclude=caller)            


class CmdOpenObject(Command):
    """
    Open a closed object, such as a container or a door

    Usage: open <object>

    """
    key = "open"
    lock = "cmd:all()"
    arg_regex = r"\s|$"
    help_category = "General"

    def parse(self):
        if not self.args:
            self.msg(f"|yWhat are you trying to open?")
            return
        target = self.args.lstrip()
        try:
            targets = self.caller.search(target, quiet=True)
            self.target = targets[0]
        except IndexError:
            self.msg(f"|yWhat are you trying to open?")
            raise InterruptCommand
        if self.target.db.open == True:
            self.msg(f"|yThe %s is already open!" % self.target)
            raise InterruptCommand

    def func(self):
        caller = self.caller
        target = self.target
        if not inherits_from(target, Container) and not inherits_from(target, Door):
            self.msg(f"|yYou cannot open that!")
            return
        target.db.closed = False
        target.db.open = True
        if inherits_from(target, Container):
            message = "%s open%s the %s."
            caller.msg(message % ("You", "", target))
            caller.location.msg_contents(message % (caller.key, "s", target), exclude=caller)
        if inherits_from(target, Door):
            target.setlock("traverse:true()")
            target.db.return_exit.db.closed = False
            target.db.return_exit.db.open = True
            message1 = "%s open%s the %s."
            message2 = "The %s opens."
            caller.msg(message1 % ("You", "", target))
            caller.location.msg_contents(message1 % (caller.key, "s", target), exclude=caller)
            target.db.return_exit.location.msg_contents(message2 % (target))


class CmdCloseObject(Command):
    """
    Close an open object, such as a container or a door

    Usage: close <object>

    """
    key = "close"
    lock = "cmd:all()"
    arg_regex = r"\s|$"
    help_category = "General"

    def parse(self):
        if not self.args:
            self.msg(f"|yWhat are you trying to close?")
            return
        target = self.args.lstrip()
        try:
            targets = self.caller.search(target, quiet=True)
            self.target = targets[0]
        except IndexError:
            self.msg(f"|yWhat are you trying to close?")
            raise InterruptCommand
        if self.target.db.closed == True:
            self.msg(f"|yThe %s is already closed!" % self.target)
            raise InterruptCommand

    def func(self):
        caller = self.caller
        target = self.target
        if not inherits_from(target, Container) and not inherits_from(target, Door):
            self.msg(f"|yYou cannot close that!")
            return
        target.db.closed = True
        target.db.open = False
        if inherits_from(target, Container):
            message = "%s close%s the %s."
            caller.msg(message % ("You", "", target))
            caller.location.msg_contents(message % (caller.key, "s", target), exclude=caller)
        if inherits_from(target, Door):
            target.setlock("traverse:false()")
            target.db.return_exit.db.closed = True
            target.db.return_exit.db.open = False
            message1 = "%s close%s the %s."
            message2 = "The %s closes."
            caller.msg(message1 % ("You", "", target))
            caller.location.msg_contents(message1 % (caller.key, "s", target), exclude=caller)
            target.db.return_exit.location.msg_contents(message2 % (target))
