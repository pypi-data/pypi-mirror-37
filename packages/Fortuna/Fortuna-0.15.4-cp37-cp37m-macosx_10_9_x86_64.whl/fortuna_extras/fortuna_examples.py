""" Random inside random with random sprinkles, or Dynamic non-determinism """
from Fortuna import CumulativeWeightedChoice, MultiCat
from fortuna_extras import distribution_timer
from collections import OrderedDict


""" MultiCat is an abstraction layer to enable random selection
from a sequence inside an OrderedDict by passing an optional category key.
MultiCat uses RandomCycle() to produce a uniform non-repeating distribution of values within each cat sequence.
If no key is provided MultiCat will use Mostly() to choose a random key for you,
where values at beginning of the key list are more common than values at the back.
This makes the top of the data structure geometrically more common than the bottom.
Cats love to be on top. """


random_spell = MultiCat(OrderedDict({
    # Top key is progressively more common without a cat_key.
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
    # Bottom key is progressively more rare without a cat_key.
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
    print("""Treasure Table Example: 
 1-50   Potion of healing
51-60   Spell scroll (6th level) - dynamic (could be one of several level 6 spells)
61-70   Potion of climbing
71-90   Spell scroll (7th level) - dynamic (could be one of several level 7 spells)
91-94   Spell scroll (8th level) - dynamic (could be one of several level 8 spells)
95-98   Potion of greater healing
   99   Bag of holding
  100   Driftglobe
""")
    distribution_timer(random_magic_table, call_sig="random_magic_table()", max_distribution=100)
