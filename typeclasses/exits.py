"""
Exits

Exits are connectors between Rooms. An exit always has a destination property
set and has a single command defined on itself with the same name as its key,
for allowing Characters to traverse the exit to its destination.

"""
from evennia.contrib.ingame_python.typeclasses import EventExit


class Exit(EventExit):
    """
    Exits are connectors between rooms. Exits are normal Objects except
    they defines the `destination` property. It also does work in the
    following methods:

     basetype_setup() - sets default exit locks (to change, use `at_object_creation` instead).
     at_cmdset_get(**kwargs) - this is called when the cmdset is accessed and should
                              rebuild the Exit cmdset along with a command matching the name
                              of the Exit object. Conventionally, a kwarg `force_init`
                              should force a rebuild of the cmdset, this is triggered
                              by the `@alias` command when aliases are changed.
     at_failed_traverse() - gives a default error message ("You cannot
                            go there") if exit traversal fails and an
                            attribute `err_traverse` is not defined.

    Relevant hooks to overload (compared to other types of Objects):
        at_traverse(traveller, target_loc) - called to do the actual traversal and calling of the other hooks.
                                            If overloading this, consider using super() to use the default
                                            movement implementation (and hook-calling).
        at_after_traverse(traveller, source_loc) - called by at_traverse just after traversing.
        at_failed_traverse(traveller) - called by at_traverse if traversal failed for some reason. Will
                                        not be called if the attribute `err_traverse` is
                                        defined, in which case that will simply be echoed.
    """

    pass


class Door(Exit):

    def at_object_creation(self):
        self.db.return_exit = None
        self.db.closed = False
        self.db.open = True
        self.aliases.add({self.name})

    def get_display_name(self, looker, **kwargs):
        if self.db.closed == True:
            string = "closed %s" % (self.name)
            return string
        if self.db.open == True:
            string = "open %s" % (self.name)
            return string

    def setlock(self, lockstring):
        self.locks.add(lockstring)
        self.db.return_exit.locks.add(lockstring)

    def setdesc(self, description):
        self.db.desc = description
        self.db.return_exit.db.desc = description

    def delete(self):
        if self.db.return_exit:
            super().delete()
        super().delete()
        return True

    def at_failed_traverse(self, traversing_object):
        traversing_object.msg("|yThe %s is closed!" % self.key)
        
