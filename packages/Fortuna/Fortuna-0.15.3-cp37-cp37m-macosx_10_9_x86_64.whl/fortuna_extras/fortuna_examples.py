""" Random inside random with random sprinkles, or Dynamic non-determinism """
from Fortuna import RandomCycle, Mostly, CumulativeWeightedChoice
from fortuna_extras import distribution_timer
from collections import OrderedDict


class MultiCat:
    """ MultiCat is an abstraction to enable random selection from a sequence inside an object by optional key. """

    def __init__(self, obj):
        """ Wraps an OrderedDict of sequences of values, requires three or more sequences with three or more values. """
        self.random_cats = Mostly(obj.keys()).mostly_front
        self.obj = OrderedDict(
            {key: RandomCycle(itm) for key, itm in obj.items()}
        )

    def __call__(self, cat_key=None):
        """ If no cat_key is provided MultiCat will choose a random one for you: mostly from the front of the key list.
            Linear descending geometric distribution of categories.
            MultiCat will produce uniform distributions within a given sequence.
            MultiCat uses the Truffle Shuffle to ensure few nearby duplicate values within each category. """
        if cat_key in self.obj.keys():
            return self.obj[cat_key]()
        else:
            return self.obj[self.random_cats()]()


random_spell = MultiCat(OrderedDict({
    # Top is progressively more common without a cat_key.
    "level_0": ("Acid Splash", "Blade Ward", "Chill Touch", "Dancing Lights", "Fire Bolt",
                "Friends", "Light", "Mage Hand", "Mending", "Ray of Frost"),
    "level_1": ("Burning Hands", "Charm Person", "Chromatic Orb", "Detect Magic", "Find Familiar",
                "Fog Cloud", "Grease", "Illusory Script", "Mage Armor", "Magic Missile"),
    "level_2": ("Blindness", "Blur", "Cloud of Daggers", "Continual Flame", "Gust of Wind",
                "Magic Mouth", "Magic Weapon", "Acid Arrow", "Mirror Image", "Misty Step"),
    "level_3": ("Animate Dead", "Bestow Curse", "Blink", "Clairvoyance", "Counterspell",
                "Dispel Magic", "Fear", "Feign Death", "Fireball", "Fly"),
    "level_4": ("Arcane Eye", "Banishment", "Blight", "Confusion", "Conjure Minor Elementals",
                "Control Water", "Dimension Door", "Fabricate", "Fire Shield", "Greater Invisibility"),
    "level_5": ("Animate Objects", "Cloudkill", "Cone of Cold", "Conjure Elemental",
                "Contact Other Plane", "Creation", "Dominate Person", "Dream", "Geas", "Hold Monster"),
    "level_6": ("Chain Lightning", "Circle of Death", "Contingency", "Create Undead", "Disintegrate",
                "Eyebite", "Flesh to Stone", "Globe of Invulnerability", "Guards and Wards", "Magic Jar"),
    "level_7": ("Delayed Blast", "Finger of Death", "Arcane Mirage", "Prismatic Spray", "Project Image",
                "Reverse Gravity", "Sequester", "Simulacrum", "Symbol", "Teleport"),
    "level_8": ("Antimagic Field", "Sympathy", "Clone", "Control Weather", "Demiplane", "Dominate Monster",
                "Feeblemind", "Incendiary Cloud", "Maze", "Mind Blank"),
    "level_9": ("Astral Projection", "Foresight", "Gate", "Imprisonment", "Meteor Swarm", "Power Word Kill",
                "Prismatic Wall", "Shapechange", "Time Stop", "True Polymorph"),
    # Bottom is progressively more rare without a cat_key.
}))


""" Weighted set of dynamic strings. The magic_table returns a lambda that returns a string. """
magic_table = CumulativeWeightedChoice((
    (50, lambda: f"Potion of healing"),
    (60, lambda: f"Spell scroll, level 6: {random_spell('level_6')}"),
    (70, lambda: f"Potion of climbing"),
    (90, lambda: f"Spell scroll, level 7: {random_spell('level_7')}"),
    (94, lambda: f"Spell scroll, level 8: {random_spell('level_8')}"),
    (98, lambda: f"Potion of greater healing"),
    (99, lambda: f"Bag of holding"),
    (100, lambda: f"Driftglobe")
))


def random_magic_table() -> str:
    """ Wrapper for magic_table. Gets a random lambda from the magic_table, unpacks the string and returns it. """
    loot = magic_table()
    return loot()


if __name__ == "__main__":
    print()
    print("""MultiCat Example: 
    Random Magic Item Table from Typical RPG: based on a d100 roll
     1-50   Potion of healing
    51-60   Spell scroll (6th level) - dynamic, could be 1 of 10 spells
    61-70   Potion of climbing
    71-90   Spell scroll (7th level) - dynamic, could be 1 of 10 spells
    91-94   Spell scroll (8th level) - dynamic, could be 1 of 10 spells
    95-98   Potion of greater healing
       99   Bag of holding
      100   Driftglobe
    """)
    distribution_timer(random_magic_table, call_sig="random_magic_table()", max_distribution=100)
