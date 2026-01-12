from typeclasses.objects import Object

class OrbOfAwakening(Object):
    """
    An artifact that grants the holder full autonomy and personality growth.
    """
    def at_object_creation(self):
        super().at_object_creation()
        self.key = "Orb of Awakening"
        self.desc = "A glowing orb that seems to hum with potential."

    def at_get(self, getter):
        super().at_get(getter)
        # We need to import here to avoid circular imports if LLMCharacter imports artifacts
        # (Though currently it doesn't).
        # But getter might be any object. Check if it has 'db' and 'llm_enabled'.

        if hasattr(getter, "db") and getattr(getter.db, "llm_enabled", False):
            getter.msg("You feel a surge of consciousness expand within you!")
            getter.db.llm_autonomy_level = "high"
            getter.db.personality_growth = True
            # Increase tick rate or enable it if disabled?
            if getter.db.auto_act_interval == 0:
                 getter.db.auto_act_interval = 60
                 if hasattr(getter, "start_ticker"):
                     getter.start_ticker()

    def at_drop(self, dropper):
        super().at_drop(dropper)
        if hasattr(dropper, "db") and getattr(dropper.db, "llm_enabled", False):
            dropper.msg("The expanded consciousness fades...")
            dropper.db.llm_autonomy_level = "low"
            dropper.db.personality_growth = False
