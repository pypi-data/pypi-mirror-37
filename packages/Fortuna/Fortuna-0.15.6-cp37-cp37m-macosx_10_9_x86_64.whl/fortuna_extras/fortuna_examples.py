from Fortuna import CumulativeWeightedChoice, MultiCat
from collections import OrderedDict


random_spell = MultiCat(OrderedDict({
    "cantrip": ("Acid Splash", "Blade Ward", "Chill Touch", "Dancing Lights", "Fire Bolt"),
    "level_1": ("Burning Hands", "Charm Person", "Chromatic Orb", "Detect Magic", "Find Familiar"),
    "level_2": ("Blindness", "Blur", "Cloud of Daggers", "Continual Flame", "Gust of Wind"),
}))


magic_item_table = CumulativeWeightedChoice((
    (50, lambda: f"Potion of healing"),
    (60, lambda: f"Spell scroll (cantrip) {random_spell('cantrip')}"),
    (70, lambda: f"Potion of climbing"),
    (90, lambda: f"Spell scroll (level 1) {random_spell('level_1')}"),
    (94, lambda: f"Spell scroll (level 2) {random_spell('level_2')}"),
    (98, lambda: f"Potion of greater healing"),
    (99, lambda: f"Bag of holding"),
    (100, lambda: f"Driftglobe"),
))


def get_random_magic_item() -> str:
    return magic_item_table()()


if __name__ == "__main__":
    from fortuna_extras.fortuna_tests import distribution_timer

    print("""
Typical Magic Item Table from an RPG, based on 1d100 roll.

     1-50   Potion of healing
    51-60   Spell scroll (cantrip) - one of several cantrips
    61-70   Potion of climbing
    71-90   Spell scroll (level 1) - one of several level 1 spells
    91-94   Spell scroll (level 2) - one of several level 2 spells
    95-98   Potion of greater healing
       99   Bag of holding
      100   Driftglobe
      
    """)
    print("Magic Item Table Distribution:")
    distribution_timer(get_random_magic_item, call_sig="get_random_magic_item()", max_distribution=100)
    print("Magic Item Table Samples:")
    for _ in range(25):
        print(get_random_magic_item())
