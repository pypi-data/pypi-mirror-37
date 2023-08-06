from Fortuna import CumulativeWeightedChoice, MultiCat, distribution_timer
from collections import OrderedDict


note = """
Typical Magic Item Table from an RPG, based on 1d100 roll.

     1-50   Potion of healing
    51-60   Spell scroll (cantrip) - one of several cantrips
    61-70   Potion of climbing
    71-90   Spell scroll (level 1) - one of several level 1 spells
    91-94   Spell scroll (level 2) - one of several level 2 spells
    95-98   Potion of greater healing
       99   Bag of holding
      100   Driftglobe
"""


class RandomSpell:

    def __call__(self, level_cat=None) -> str:
        return self._random_spell(level_cat)

    def __init__(self):
        self._random_spell = MultiCat(OrderedDict({
            "cantrip": ("Acid Splash", "Blade Ward", "Chill Touch", "Dancing Lights", "Fire Bolt"),  # ...
            "level_1": ("Burning Hands", "Charm Person", "Chromatic Orb", "Detect Magic", "Find Familiar"),  # ...
            "level_2": ("Blindness", "Blur", "Cloud of Daggers", "Continual Flame", "Gust of Wind"),  # ...
            # ... up to level 9
        }))


class MagicItemTable:

    def __call__(self) -> str:
        return self._magic_item_table()()

    def __init__(self):
        self.random_spell = RandomSpell()
        self._magic_item_table = CumulativeWeightedChoice((
            (50, lambda: f"Potion of healing"),
            (60, lambda: f"Spell scroll (cantrip) {self.random_spell('cantrip')}"),
            (70, lambda: f"Potion of climbing"),
            (90, lambda: f"Spell scroll (level 1) {self.random_spell('level_1')}"),
            (94, lambda: f"Spell scroll (level 2) {self.random_spell('level_2')}"),
            (98, lambda: f"Potion of greater healing"),
            (99, lambda: f"Bag of holding"),
            (100, lambda: f"Driftglobe"),
        ))


if __name__ == "__main__":
    print(note)

    print("Magic Item Table Distribution:")
    random_magic_item = MagicItemTable()
    distribution_timer(random_magic_item, call_sig="random_magic_item()")

    print("Cantrip Distribution:")
    random_spell = RandomSpell()
    distribution_timer(random_spell, 'cantrip', call_sig="random_spell('cantrip')")

    print("All Spells Distribution:")
    random_spell = RandomSpell()
    distribution_timer(random_spell, call_sig="random_spell()")
