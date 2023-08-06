from Fortuna import weighted_choice, min_max, RandomCycle, zero_cool

from fortuna_extras import distribution_timer


class MultiCat:
    __qualname__ = "MultiCat"

    def __init__(self, obj):
        self.rand_cat = RandomCycle(obj.keys())
        self.obj = {key: RandomCycle(itm) for key, itm in obj.items()}

    def __call__(self, cat=None):
        if cat in self.obj.keys():
            return self.obj[cat]()
        else:
            return self.obj[self.rand_cat()]()


def magic_table_a():
    loot = (
        (50, "Potion of healing"),
        (60, f"Spell scroll (cantrip) {random_spell(spell_level=0)}"),
        (70, "Potion of climbing"),
        (90, f"Spell scroll (1st level) {random_spell(spell_level=1)}"),
        (94, f"Spell scroll (2nd level) {random_spell(spell_level=2)}"),
        (98, "Potion of greater healing"),
        (99, "Bag of holding"),
        (100, "Driftglobe")
    )
    return weighted_choice(loot)


spells = MultiCat({
    "cantrip": (
        "Acid Splash", "Blade Ward", "Chill Touch", "Dancing Lights", "Fire Bolt", "Friends", "Light",
        "Mage Hand", "Mending", "Message", "Minor Illusion", "Poison Spray", "Prestidigitation",
        "Ray of Frost", "Shocking Grasp", "True Strike"
    ),
    "level 1": (
        "Alarm", "Burning Hands", "Charm Person", "Chromatic Orb", "Color Spray", "Comprehend Languages",
        "Detect Magic", "Disguise Self", "Expeditious Retreat", "False Life", "Feather Fall", "Find Familiar",
        "Fog Cloud", "Grease", "Identify", "Illusory Script", "Jump", "Longstrider", "Mage Armor",
        "Magic Missile", "Protection from Evil and Good", "Ray of Sickness", "Shield", "Silent Image",
        "Sleep", "Tasha’s Hideous Laughter", "Tenser’s Floating Disk", "Thunderwave", "Unseen Servant",
        "Witch Bolt"
    ),
    "level 2": (
        "Alter Self", "Arcane Lock", "Blindness/Deafness", "Blur", "Cloud of Daggers", "Continual Flame",
        "Crown of Madness", "Darkness", "Darkvision", "Detect Thoughts", "Enlarge/Reduce", "Flaming Sphere",
        "Gentle Repose", "Gust of Wind", "Hold Person", "Invisibility", "Knock", "Levitate", "Locate Object",
        "Magic Mouth", "Magic Weapon", "Melf’s Acid Arrow", "Mirror Image", "Misty Step", "Nystul’s Magic Aura",
        "Phantasmal Force", "Ray of Enfeeblement", "Rope Trick", "Scorching Ray", "See Invisibility", "Shatter",
        "Spider Climb", "Suggestion", "Web"
    )
})


def random_spell(spell_level=None):
    level = spell_level if spell_level else zero_cool(2)
    return spells(level)


if __name__ == "__main__":
    distribution_timer(random_spell, "level 2")
