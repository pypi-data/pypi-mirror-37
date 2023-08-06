from Fortuna import CumulativeWeightedChoice, MultiCat, distribution_timer
from collections import OrderedDict


note = """
Typical treasure tables from a massively popular roll playing game.

    Treasure Table A
     1-50   Potion of healing
    51-60   Spell scroll (cantrip) - one of several cantrips
    61-70   Potion of climbing
    71-90   Spell scroll (level 1) - one of several level 1 spells
    91-94   Spell scroll (level 2) - one of several level 2 spells
    95-98   Potion of greater healing
       99   Bag of holding
      100   Driftglobe
      
    Treasure Table E
     1-30   Spell scroll (8th level) - one of several level 8 spells
    31-55   Potion of storm giant strength
    56-70   Potion of supreme healing
    71-85   Spell scroll (9th level) - one of several level 9 spells
    86-93   Universal solvent
    94-98   Arrow of slaying
    99-100  Sovereign glue
    
"""


class RandomSpell:

    def __call__(self, spell_level=None) -> str:
        return self.random_spell(spell_level)

    def __init__(self):
        self.random_spell = MultiCat(OrderedDict({
            "cantrip": (
                "Acid Splash", "Blade Ward", "Chill Touch", "Dancing Lights", "Fire Bolt", "Friends", "Guidance",
                "Light", "Mage Hand", "Mending", "Message", "Minor Illusion", "Poison Spray", "Prestidigitation",
                "Ray of Frost", "Resistance", "Sacred Flame", "Shocking Grasp", "Spare the Dying", "Thaumaturgy",
                "True Strike", "Vicious Mockery",
            ),
            "level_1": (
                "Alarm", "Animal Friendship", "Bane", "Bless", "Burning Hands", "Charm Person", "Chromatic Orb",
                "Color Spray", "Command", "Comprehend Languages", "Create or Destroy Water", "Cure Wounds",
                "Detect Evil and Good", "Detect Magic", "Detect Poison and Disease", "Disguise Self",
                "Dissonant Whispers", "Expeditious Retreat", "Faerie Fire", "False Life", "Feather Fall",
                "Find Familiar", "Fog Cloud", "Grease", "Guiding Bolt", "Healing Word", "Heroism", "Identify",
                "Illusory Script", "Inflict Wounds", "Jump", "Longstrider", "Mage Armor", "Magic Missile",
                "Protection from Evil and Good", "Purify Food and Drink", "Ray of Sickness", "Sanctuary",
                "Shield", "Shield of Faith", "Silent Image", "Sleep", "Speak with Animals", "Tasha's Hideous Laughter",
                "Tenser's Floating Disk", "Thunderwave", "Unseen Servant", "Witch Bolt",
            ),
            "level_2": (
                "Aid", "Alter Self", "Animal Messenger", "Arcane Lock", "Augury", "Blindness/Deafness", "Blur",
                "Calm Emotions", "Cloud of Daggers", "Continual Flame", "Crown of Madness", "Darkness", "Darkvision",
                "Detect Thoughts", "Enhance Ability", "Enlarge/Reduce", "Enthrall", "Find Traps", "Flaming Sphere",
                "Gentle Repose", "Gust of Wind", "Heat Metal", "Hold Person", "Invisibility", "Knock",
                "Lesser Restoration", "Levitate", "Locate Animals or Plants", "Locate Object", "Magic Mouth",
                "Magic Weapon", "Melf's Acid Arrow", "Mirror Image", "Misty Step", "Nystul's Magic Aura",
                "Phantasmal Force", "Prayer of Healing", "Protection from Poison", "Ray of Enfeeblement",
                "Rope Trick", "Scorching Ray", "See Invisibility", "Shatter", "Silence", "Spider Climb",
                "Spiritual Weapon", "Suggestion", "Warding Bond", "Web", "Zone of Truth",
            ),
            # ... (level_3 - level_7) ...
            "level_8": (
                "Antimagic Field", "Antipathy/Sympathy", "Clone", "Control Weather", "Demiplane", "Dominate Monster",
                "Earthquake", "Feeblemind", "Glibness", "Holy Aura", "Incendiary Cloud", "Maze", "Mind Blank",
                "Power Word Stun", "Sunburst", "Telepathy", "Trap the Soul",
            ),
            "level_9": (
                "Astral Projection", "Foresight", "Gate", "Imprisonment", "Mass Heal", "Meteor Swarm",
                "Power Word Heal", "Power Word Kill", "Prismatic Wall", "Shapechange", "Time Stop", "True Polymorph",
                "True Resurrection", "Weird", "Wish",
            )
        }))


class TreasureTable_A:

    def __init__(self):
        self.random_spell = RandomSpell()
        self.treasure = CumulativeWeightedChoice((
            (50, lambda: f"Potion of healing"),
            (60, lambda: f"Spell scroll (cantrip) {self.random_spell('cantrip')}"),
            (70, lambda: f"Potion of climbing"),
            (90, lambda: f"Spell scroll (level 1) {self.random_spell('level_1')}"),
            (94, lambda: f"Spell scroll (level 2) {self.random_spell('level_2')}"),
            (98, lambda: f"Potion of greater healing"),
            (99, lambda: f"Bag of holding"),
            (100, lambda: f"Driftglobe"),
        ))

    def __call__(self) -> str:
        return self.treasure()()


class TreasureTable_E:

    def __init__(self):
        self.random_spell = RandomSpell()
        self.treasure = CumulativeWeightedChoice((
            (30, lambda: f"Spell scroll (8th level) {self.random_spell('level_8')}"),
            (55, lambda: f"Potion of storm giant strength"),
            (70, lambda: f"Potion of supreme healing"),
            (85, lambda: f"Spell scroll (9th level) {self.random_spell('level_9')}"),
            (93, lambda: f"Universal solvent"),
            (98, lambda: f"Arrow of slaying"),
            (100, lambda: f"Sovereign glue")
        ))

    def __call__(self) -> str:
        return self.treasure()()


if __name__ == "__main__":
    print(note)

    print("Treasure Table A Distribution:")
    treasure_table_a = TreasureTable_A()
    distribution_timer(treasure_table_a, call_sig="treasure_table_a()", max_distribution=125)

    print("Treasure Table E Distribution:")
    treasure_table_e = TreasureTable_E()
    distribution_timer(treasure_table_e, call_sig="treasure_table_e()", max_distribution=125)
