import re
from evennia.utils import logger
from evennia import Command
from evennia.utils.utils import inherits_from
from evennia.contrib.ingame_python.typeclasses import EventCharacter


# gender maps

_GENDER_PRONOUN_MAP = {
    "male": {"s": "he", "o": "him", "p": "his", "a": "his"},
    "female": {"s": "she", "o": "her", "p": "her", "a": "hers"},
    "neutral": {"s": "it", "o": "it", "p": "its", "a": "its"},
    "ambiguous": {"s": "they", "o": "them", "p": "their", "a": "theirs"},
}
_RE_GENDER_PRONOUN = re.compile(r"(?<!\|)\|(?!\|)[sSoOpPaA]")


class SetGender(Command):
    """
    Sets gender on yourself or another character

    Usage: @gender male||female||neutral||ambiguous
           @gender <target> male|female|neutral|ambiguous

    """
    key = "@gender"
    locks = "cmd:perm(Admin)"
    help_category = "Admin"

    def func(self):
        caller = self.caller
        args = self.args.lstrip().lower()
        try:
            target, gender = args.split(" ", 1)
        except ValueError:
            target = None
            gender = args
        if gender not in ("male", "female", "neutral", "ambiguous"):
            caller.msg(f"|yUsage: @gender male||female||neutral||ambiguous")
            return
        if target == None:
            caller.db.gender = gender
            caller.msg(f"Your gender was set to %s." % gender)
            return
        else:
            try:
                targets = caller.search(target, quiet=True)
                target = targets[0]
            except IndexError:
                caller.msg(f"|yWho are you trying to change the gender of?")
                return
            if not inherits_from(target, EventCharacter):
                caller.msg(f"|yYou cannot assign a gender to that!")
                return
            target.db.gender = gender
            caller.msg(f"You have set %s's gender to %s." % (target, gender))
            target.msg(f"%s has set your gender to %s." % (caller.key, gender))


class GenderCharacter(EventCharacter):
    """
    - `|s`, `|S`: Subjective form: he, she, it, He, She, It, They
    - `|o`, `|O`: Objective form: him, her, it, Him, Her, It, Them
    - `|p`, `|P`: Possessive form: his, her, its, His, Her, Its, Their
    - `|a`, `|A`: Absolute Possessive form: his, hers, its, His, Hers, Its, Theirs
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.gender = "ambiguous"

    def _get_pronoun(self, regex_match):
        typ = regex_match.group()[1]  # "s", "O" etc
        gender = self.attributes.get("gender", default="ambiguous")
        gender = gender if gender in ("male", "female", "neutral") else "ambiguous"
        pronoun = _GENDER_PRONOUN_MAP[gender][typ.lower()]
        return pronoun.capitalize() if typ.isupper() else pronoun

    def msg(self, text=None, from_obj=None, session=None, **kwargs):
        if text is None:
            super().msg(from_obj=from_obj, session=session, **kwargs)
            return

        try:
            if text and isinstance(text, tuple):
                text = (_RE_GENDER_PRONOUN.sub(self._get_pronoun, text[0]), *text[1:])
            else:
                text = _RE_GENDER_PRONOUN.sub(self._get_pronoun, text)
        except TypeError:
            pass
        except Exception as e:
            logger.log_trace(e)
        super().msg(text, from_obj=from_obj, session=session, **kwargs)
