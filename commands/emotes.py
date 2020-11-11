from evennia import Command
from evennia.utils.utils import inherits_from
from evennia import InterruptCommand
from typeclasses.objects import Object
from typeclasses.exits import Exit
from typeclasses.characters import Character
from typeclasses.rooms import Room
from world import gendersub


class CmdApplaud(Command):
    """
    Applaud a specific target, or nothing in particular

    Usage: applaud <optional target> (optional text)

    Ex: applaud
        You: "You applaud."
        Room: "Roger applauds."
    Ex: applaud Thomas with a standing ovation
        You: "You applaud Thomas with a standing ovation."
        Thomas: "Roger applauds you with a standing ovation."
        Room: "Roger applauds Thomas with a standing ovation."

    """
    key = "applaud"
    lock = "cmd:all()"
    arg_regex = r"\s|$"
    help_category = "Emotes"

    def func(self):
        caller = self.caller
        args = self.args.lstrip()
        if not args:
            message = "%s applaud%s."
            caller.msg(message % ("You", ""))
            caller.location.msg_contents(message % (caller.key, "s"), exclude=caller)
            return
        try:
            target, text = args.split(" ", 1)
        except ValueError:
            target = args
            text = None
        try:
            targets = caller.search(target, quiet=True)
            target = targets[0]
        except IndexError:
            target = None
            text = args
        if target == caller:
            caller.msg(f"|yYou cannot target yourself!")
            return
        if text == None:
            if inherits_from(target, Character):
                message = "%s applaud%s %s."
                caller.msg(message % ("You", "", target))
                target.msg(message % (caller.key, "s", "you"))
                caller.location.msg_contents(message % (caller.key, "s", target), exclude=(caller, target))
                return
        if not text == None:
            if not text.endswith((".", "?", "!")):
                text = "%s." % text
            if inherits_from(target, Character):
                message = "%s applaud%s %s %s"
                caller.msg(message % ("You", "", target, text))
                target.msg(message % (caller.key, "s", "you", text))
                caller.location.msg_contents(message % (caller.key, "s", target, text), exclude=(caller, target))
                return
            if target == None:
                message = "%s applaud%s %s"
                caller.msg(message % ("You", "", text))
                caller.location.msg_contents(message % (caller.key, "s", text), exclude=caller)
                return
        else:
            caller.msg(f"|yWho are you trying to applaud?")


class CmdBat(Command):
    """
    Bat your eyelashes at someone, or nothing in particular

    Usage: bat <optional target> (optional text)

    Ex: bat John sweetly
        You: "You bat your eyelashes at John sweetly."
        John: "Joe bats his eyelashes at you sweetly."
        Room: "Joe bats his eyelashes at John sweetly."
    Ex: bat
        You: "You bat your eyelashes."
        Room: "Joe bats his eyelashes."

    """
    key = "bat"
    lock = "cmd:all()"
    arg_regex = r"\s|$"
    help_category = "Emotes"
    def func(self):
        caller = self.caller
        args = self.args.lstrip()
        if not args:
            message = "%s bat%s %s eyelashes."
            caller.msg(message % ("You", "", "your"))
            caller.location.msg_contents(message % (caller.key, "s", '|p'), exclude=caller)
            return
        try:
            target, text = args.split(" ", 1)
        except ValueError:
            target = args
            text = None
        try:
            targets = caller.search(target, quiet=True)
            target = targets[0]
        except IndexError:
            target = None
            text = args
        if target == caller:
            caller.msg(f"|yYou cannot target yourself!")
            return
        if text == None:
            if inherits_from(target, Character):
                message = "%s bat%s %s eyelashes at %s."
                caller.msg(message % ("You", "", "your", target))
                target.msg(message % (caller.key, "s", '|p', "you"))
                caller.location.msg_contents(message % (caller.key, "s", '|p', target), exclude=(caller, target))
                return
        if not text == None:
            if not text.endswith((".", "?", "!")):
                text = "%s." % text
            if inherits_from(target, Character):
                message = "%s bat%s %s eyelashes at %s %s"
                caller.msg(message % ("You", "", "your", target, text))
                target.msg(message % (caller.key, "s", '|p', "you", text))
                caller.location.msg_contents(message % (caller.key, "s", '|p', target, text), exclude=(caller, target))
                return
            if target == None:
                message = "%s bat%s %s eyelashes %s"
                caller.msg(message % ("You", "", "your", text))
                caller.location.msg_contents(message % (caller.key, "s", '|p', text), exclude=caller)
                return
        else:
            caller.msg(f"|yWho are you trying to bat your eyelashes at?")


class CmdBeam(Command):
    """
    Beam, a radiant or pleasureful smile, at a specific target or nothing in particular

    Usage: beam <optional target> (optional text)

    Ex: beam
        You: "You beam with pleasure."
        Room: "Sara beams with pleasure."
    Ex: beam joe
        You: "You beam at Joe."
        Joe: "Sara beams at you."
        Room: "Sara beams at Joe."

    """
    
    key = "beam"
    lock = "cmd:all()"
    arg_regex = r"\s|$"
    help_category = "Emotes"
    def func(self):
        caller = self.caller
        args = self.args.lstrip()
        if not args:
            message = "%s beam%s with pleasure."
            caller.msg(message % ("You", ""))
            caller.location.msg_contents(message % (caller.key, "s"), exclude=caller)
            return
        try:
            target, text = args.split(" ", 1)
        except ValueError:
            target = args
            text = None
        try:
            targets = caller.search(target, quiet=True)
            target = targets[0]
        except IndexError:
            target = None
            text = args
        if target == caller:
            caller.msg(f"|yYou cannot target yourself!")
            return
        if text == None:
            if inherits_from(target, Character):
                message = "%s beam%s at %s."
                caller.msg(message % ("You", "", target))
                target.msg(message % (caller.key, "s", "you"))
                caller.location.msg_contents(message % (caller.key, "s", target), exclude=(caller, target))
                return
        if not text == None:
            if not text.endswith((".", "?", "!")):
                text = "%s." % text
            if inherits_from(target, Character):
                message = "%s beam%s at %s %s"
                caller.msg(message % ("You", "", target, text))
                target.msg(message % (caller.key, "s", "you", text))
                caller.location.msg_contents(message % (caller.key, "s", target, text), exclude=(caller, target))
                return
            if target == None:
                message = "%s beam%s %s"
                caller.msg(message % ("You", "", text))
                caller.location.msg_contents(message % (caller.key, "s", text), exclude=caller)
                return
        else:
            caller.msg(f"|yWho are you trying to beam at?")


class CmdBelch(Command):
    """
    Belch at a specific target or nothing in particular

    Usage: belch <optional target> (optional text)

    Ex: belch loudly
        You: "You belch loudly."
        Room: "Bryan belches loudly."
    Ex: belch john and giggles
        You: "You belch at John and giggles."
        John: "Bryan belches at you and giggles."
        Room: "Bryan belches at John and giggles."

    """
    key = "belch"
    lock = "cmd:all()"
    arg_regex = r"\s|$"
    help_category = "Emotes"
    def func(self):
        caller = self.caller
        args = self.args.lstrip()
        if not args:
            message = "%s belch%s."
            caller.msg(message % ("You", ""))
            caller.location.msg_contents(message % (caller.key, "es"), exclude=caller)
            return
        try:
            target, text = args.split(" ", 1)
        except ValueError:
            target = args
            text = None
        try:
            targets = caller.search(target, quiet=True)
            target = targets[0]
        except IndexError:
            target = None
            text = args
        if target == caller:
            caller.msg(f"|yYou cannot target yourself!")
            return
        if text == None:
            if inherits_from(target, Character):
                message = "%s belch%s at %s"
                caller.msg(message % ("You", "", target))
                target.msg(message % (caller.key, "es", "you"))
                caller.location.msg_contents(message % (caller.key, "es", target), exclude=(caller, target))
                return
        if not text == None:
            if not text.endswith((".", "?", "!")):
                text = "%s." % text
            if inherits_from(target, Character):
                message = "%s belch%s at %s %s"
                caller.msg(message % ("You", "", target, text))
                target.msg(message % (caller.key, "es", "you", text))
                caller.location.msg_contents(message % (caller.key, "es", target, text), exclude=(caller, target))
                return
            if target == None:
                message = "%s belch%s %s"
                caller.msg(message % ("You", "", text))
                caller.location.msg_contents(message % (caller.key, "es", text), exclude=caller)
                return
        else:
            caller.msg(f"|yWho are you trying to belch at?")


class CmdBlanch(Command):
    """
    Blanch, turn pale from shock, fear, or surprise

    Usage: blanch (optional text)

    Ex: blanch and looks like she has seen a ghost
        You: "You blanch and looks like she has seen a ghost."
        Room: "Sara blanches and looks like she has seen a ghost."

    """
    key = "blanch"
    lock = "cmd:all()"
    arg_regex = r"\s|$"
    help_category = "Emotes"
    def func(self):
        caller = self.caller
        args = self.args.lstrip()
        if not args:
            message = "%s blanch%s."
            caller.msg(message % ("You", ""))
            caller.location.msg_contents(message % (caller.key, "es"), exclude=caller)
            return
        if args:
            text = args
            if not text.endswith((".", "?", "!")):
                text = "%s." % text
            message = "%s blanch%s %s"
            caller.msg(message % ("You", "", text))
            caller.location.msg_contents(message % (caller.key, "es", text), exclude=caller)


class CmdBlink(Command):
    """
    Blink your eyes at someone, or nothing in particular

    Usage: blink <optional target> (optional text)

    Ex: blink
        You: "You blink."
        Room: "Jeff blinks."
    Ex: blink peter and giggles
        You: "You blink at Peter and giggles."
        Peter: "Jeff blinks at you and giggles."
        Room: "Jeff blinks at Peter and giggles."

    """
    key = "blink"
    lock = "cmd:all()"
    arg_regex = r"\s|$"
    help_category = "Emotes"
    def func(self):
        caller = self.caller
        args = self.args.lstrip()
        if not args:
            message = "%s blink%s."
            caller.msg(message % ("You", ""))
            caller.location.msg_contents(message % (caller.key, "s"), exclude=caller)
            return
        try:
            target, text = args.split(" ", 1)
        except ValueError:
            target = args
            text = None
        try:
            targets = caller.search(target, quiet=True)
            target = targets[0]
        except IndexError:
            target = None
            text = args
        if target == caller:
            caller.msg(f"|yYou cannot target yourself!")
            return
        if text == None:
            if inherits_from(target, Character):
                message = "%s blink%s at %s"
                caller.msg(message % ("You", "", target))
                target.msg(message % (caller.key, "s", "you"))
                caller.location.msg_contents(message % (caller.key, "s", target), exclude=(caller, target))
                return
        if not text == None:
            if not text.endswith((".", "?", "!")):
                text = "%s." % text
            if inherits_from(target, Character):
                message = "%s blink%s at %s %s"
                caller.msg(message % ("You", "", target, text))
                target.msg(message % (caller.key, "s", "you", text))
                caller.location.msg_contents(message % (caller.key, "s", target, text), exclude=(caller, target))
                return
            if target == None:
                message = "%s blink%s %s"
                caller.msg(message % ("You", "", text))
                caller.location.msg_contents(message % (caller.key, "s", text), exclude=caller)
                return
        else:
            caller.msg(f"|yWho are you trying to blink at?")


class CmdBlow(Command):
    """
    Blow a kiss to someone

    Usage: blow <target> (optional text)

    Ex: blow ray
        You: "You blow a kiss to Ray."
        Ray: "April blows a kiss to you."
        Room: "April blows a kiss to Ray."

    """
    key = "blow"
    lock = "cmd:all()"
    arg_regex = r"\s|$"
    help_category = "Emotes"
    def func(self):
        caller = self.caller
        args = self.args.lstrip()
        if not args:
            caller.msg(f"|yWho are you trying to blow a kiss to?")
            return
        try:
            target, text = args.split(" ", 1)
        except ValueError:
            target = args
            text = None
        try:
            targets = caller.search(target, quiet=True)
            target = targets[0]
        except IndexError:
            caller.msg(f"|yWho are you trying to blow a kiss to?")
            return
        if target == caller:
            caller.msg(f"|yYou cannot target yourself!")
            return
        if text == None:
            if inherits_from(target, Character):
                message = "%s blow%s a kiss to %s"
                caller.msg(message % ("You", "", target))
                target.msg(message % (caller.key, "s", "you"))
                caller.location.msg_contents(message % (caller.key, "s", target), exclude=(caller, target))
                return
        if not text == None:
            if not text.endswith((".", "?", "!")):
                text = "%s." % text
            if inherits_from(target, Character):
                message = "%s blow%s a kiss to %s %s"
                caller.msg(message % ("You", "", target, text))
                target.msg(message % (caller.key, "s", "you", text))
                caller.location.msg_contents(message % (caller.key, "s", target, text), exclude=(caller, target))
                return
        else:
            caller.msg(f"|yWho are you trying to blow a kiss to?")


class CmdBow(Command):
    """
    Bow to someone, or nothing in particular

    Usage: bow <optional target> (optional text)

    Ex: bow deeply
        You: "You bow deeply."
        Room: "Josh bows deeply."
    Ex: bow richard
        You: "You bow to Richard."
        Richard: "Josh bows to you."
        Room: "Josh bows to Richard."
    
    """
    key = "bow"
    lock = "cmd:all()"
    arg_regex = r"\s|$"
    help_category = "Emotes"
    def func(self):
        caller = self.caller
        args = self.args.lstrip()
        if not args:
            message = "%s bow%s."
            caller.msg(message % ("You", ""))
            caller.location.msg_contents(message % (caller.key, "s"), exclude=caller)
            return
        try:
            target, text = args.split(" ", 1)
        except ValueError:
            target = args
            text = None
        try:
            targets = caller.search(target, quiet=True)
            target = targets[0]
        except IndexError:
            target = None
            text = args
        if target == caller:
            caller.msg(f"|yYou cannot target yourself!")
            return
        if text == None:
            if inherits_from(target, Character):
                message = "%s bow%s to %s"
                caller.msg(message % ("You", "", target))
                target.msg(message % (caller.key, "s", "you"))
                caller.location.msg_contents(message % (caller.key, "s", target), exclude=(caller, target))
                return
        if not text == None:
            if not text.endswith((".", "?", "!")):
                text = "%s." % text
            if inherits_from(target, Character):
                message = "%s bow%s to %s %s"
                caller.msg(message % ("You", "", target, text))
                target.msg(message % (caller.key, "s", "you", text))
                caller.location.msg_contents(message % (caller.key, "s", target, text), exclude=(caller, target))
                return
            if target == None:
                message = "%s bow%s %s"
                caller.msg(message % ("You", "", text))
                caller.location.msg_contents(message % (caller.key, "s", text), exclude=caller)
                return
        else:
            caller.msg(f"|yWho are you trying to bow to?")


class CmdBurp(Command):
    """
    Burp at someone, or nothing in particular

    Usage: burp <optional target> (optional text)

    Ex: burp
        You: "You burp."
        Room: "Bob burps."
    Ex: burp sam loudly
        You: "You burp at Sam loudly."
        Sam: "Bob burps at you loudly."
        Room: "Bob burps at Sam loudly."
    
    """
    key = "burp"
    lock = "cmd:all()"
    arg_regex = r"\s|$"
    help_category = "Emotes"
    def func(self):
        caller = self.caller
        args = self.args.lstrip()
        if not args:
            message = "%s burp%s."
            caller.msg(message % ("You", ""))
            caller.location.msg_contents(message % (caller.key, "s"), exclude=caller)
            return
        try:
            target, text = args.split(" ", 1)
        except ValueError:
            target = args
            text = None
        try:
            targets = caller.search(target, quiet=True)
            target = targets[0]
        except IndexError:
            target = None
            text = args
        if target == caller:
            caller.msg(f"|yYou cannot target yourself!")
            return
        if text == None:
            if inherits_from(target, Character):
                message = "%s burp%s at %s"
                caller.msg(message % ("You", "", target))
                target.msg(message % (caller.key, "s", "you"))
                caller.location.msg_contents(message % (caller.key, "s", target), exclude=(caller, target))
                return
        if not text == None:
            if not text.endswith((".", "?", "!")):
                text = "%s." % text
            if inherits_from(target, Character):
                message = "%s burp%s at %s %s"
                caller.msg(message % ("You", "", target, text))
                target.msg(message % (caller.key, "s", "you", text))
                caller.location.msg_contents(message % (caller.key, "s", target, text), exclude=(caller, target))
                return
            if target == None:
                message = "%s burp%s %s"
                caller.msg(message % ("You", "", text))
                caller.location.msg_contents(message % (caller.key, "s", text), exclude=caller)
                return
        else:
            caller.msg(f"|yWho are you trying to burp at?")


class CmdCackle(Command):
    """
    Cackle at someone, or nothing in particular

    Usage: cackle <optional target> (optional text)

    Ex: cackle with glee
        You: "You cackle with glee."
        Room: "Peter cackles with glee."
    Ex: cackle tom
        You: "You cackle at Tom."
        Tom: "Peter cackles at you."
        Room: "Peter cackles at Tom."
    
    """
    key = "cackle"
    lock = "cmd:all()"
    arg_regex = r"\s|$"
    help_category = "Emotes"
    def func(self):
        caller = self.caller
        args = self.args.lstrip()
        if not args:
            message = "%s cackle%s."
            caller.msg(message % ("You", ""))
            caller.location.msg_contents(message % (caller.key, "s"), exclude=caller)
            return
        try:
            target, text = args.split(" ", 1)
        except ValueError:
            target = args
            text = None
        try:
            targets = caller.search(target, quiet=True)
            target = targets[0]
        except IndexError:
            target = None
            text = args
        if target == caller:
            caller.msg(f"|yYou cannot target yourself!")
            return
        if text == None:
            if inherits_from(target, Character):
                message = "%s cackle%s at %s"
                caller.msg(message % ("You", "", target))
                target.msg(message % (caller.key, "s", "you"))
                caller.location.msg_contents(message % (caller.key, "s", target), exclude=(caller, target))
                return
        if not text == None:
            if not text.endswith((".", "?", "!")):
                text = "%s." % text
            if inherits_from(target, Character):
                message = "%s cackle%s at %s %s"
                caller.msg(message % ("You", "", target, text))
                target.msg(message % (caller.key, "s", "you", text))
                caller.location.msg_contents(message % (caller.key, "s", target, text), exclude=(caller, target))
                return
            if target == None:
                message = "%s cackle%s %s"
                caller.msg(message % ("You", "", text))
                caller.location.msg_contents(message % (caller.key, "s", text), exclude=caller)
                return
        else:
            caller.msg(f"|yWho are you trying to cackle at?")


class CmdCaress(Command):
    """
    Caress something or someone, to touch tenderly

    Usage: caress <target> (optional text)

    Ex: caress sword gently
        You: "You caress your one-handed iron sword gently."
        Room: "Brad caresses his one-handed iron sword gently."
    
    """
    key = "caress"
    lock = "cmd:all()"
    arg_regex = r"\s|$"
    help_category = "Emotes"
    def func(self):
        caller = self.caller
        args = self.args.lstrip()
        if not args:
            caller.msg(f"|yWhat are you trying to caress?")
            return
        try:
            target, text = args.split(" ", 1)
        except ValueError:
            target = args
            text = None
        try:
            targets = caller.search(target, quiet=True)
            target = targets[0]
        except IndexError:
            caller.msg(f"|yWhat are you trying to caress?")
            return
        if target == caller:
            caller.msg(f"|yYou cannot target yourself!")
            return
        if text == None:
            if inherits_from(target, Character):
                message = "%s caress%s %s"
                caller.msg(message % ("You", "", target))
                target.msg(message % (caller.key, "es", "you"))
                caller.location.msg_contents(message % (caller.key, "es", target), exclude=(caller, target))
                return
            if inherits_from(target, Object):
                if target.location == caller:
                    message = "%s caress%s %s %s"
                    caller.msg(message % ("You", "", "your", target))
                    caller.location.msg_contents(message % (caller.key, "es", '|p', target), exclude=caller)
                    return
                message = "%s caress%s %s"
                caller.msg(message % ("You", "", target))
                caller.location.msg_contents(message % (caller.key, "es", target), exclude=(caller, target))
                return
        if not text == None:
            if not text.endswith((".", "?", "!")):
                text = "%s." % text
            if inherits_from(target, Character):
                message = "%s caress%s %s %s"
                caller.msg(message % ("You", "", target, text))
                target.msg(message % (caller.key, "es", "you", text))
                caller.location.msg_contents(message % (caller.key, "es", target, text), exclude=(caller, target))
                return
            if inherits_from(target, Object):
                if target.location == caller:
                    message = "%s caress%s %s %s %s"
                    caller.msg(message % ("You", "", "your", target, text))
                    caller.location.msg_contents(message % (caller.key, "es", '|p', target, text), exclude=caller)
                    return
                message = "%s caress%s %s %s"
                caller.msg(message % ("You", "", target, text))
                caller.location.msg_contents(message % (caller.key, "es", target, text), exclude=(caller, target))
                return
        else:
            caller.msg(f"|yWhat are you trying to caress?")
