from evennia import default_cmds

class CmdExitError(default_cmds.MuxCommand):
    locks = "cmd:all()"
    arg_regex = r"\s|$"
    auto_help = False
    def func(self):
        "returns the error"
        self.caller.msg(f"|yYou cannot move %s." % self.key)


class CmdExitErrorNorth(CmdExitError):
    key = "north"
    aliases = ["n"]


class CmdExitErrorEast(CmdExitError):
    key = "east"
    aliases = ["e"]


class CmdExitErrorSouth(CmdExitError):
    key = "south"
    aliases = ["s"]


class CmdExitErrorWest(CmdExitError):
    key = "west"
    aliases = ["w"]


class CmdExitErrorNorthEast(CmdExitError):
    key = "northeast"
    aliases = ["ne"]


class CmdExitErrorSouthEast(CmdExitError):
    key = "southeast"
    aliases = ["se"]


class CmdExitErrorSouthWest(CmdExitError):
    key = "southwest"
    aliases = ["sw"]


class CmdExitErrorNorthWest(CmdExitError):
    key = "northwest"
    aliases = ["nw"]


class CmdExitErrorUp(CmdExitError):
    key = "up"
    aliases = ["u"]


class CmdExitErrorDown(CmdExitError):
    key = "down"
    aliases = ["d"]
