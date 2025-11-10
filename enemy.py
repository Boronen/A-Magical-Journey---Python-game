from characters import Character
from enemy_spells import ENEMY_SPELLS

class Enemy(Character):
    def __init__(self, name, race, pclass, hp, atk, defense, magic, speed, mana=0, spells=None):
        super().__init__(name, race, pclass)
        self.hp = self.max_hp = hp
        self.attack = atk
        self.defense = defense
        self.magic = magic
        self.speed = speed
        self.mana = self.max_mana = mana
        self.spells = spells or []
        self.status_effects = []
        self.stunned = False
        self.weakness = None
        self.resistance = None

enemy_templates = [
    {
        "name": "Farkas",
        "race": "beast",
        "pclass": "warrior",
        "hp": 30,
        "atk": 6,
        "def": 2,
        "magic": 10,
        "speed": 15,
        "mana": 0,
        "spells": []
    },
    {
        "name": "Goblin",
        "race": "goblin",
        "pclass": "thief",
        "hp": 40,
        "atk": 8,
        "def": 4,
        "magic": 12,
        "speed": 20,
        "mana": 0,
        "spells": []
    },
    {
        "name": "Óriás Patkány",
        "race": "beast",
        "pclass": "thief",
        "hp": 25,
        "atk": 5,
        "def": 1,
        "magic": 6,
        "speed": 10,
        "mana": 0,
        "spells": []
    },
    {
        "name": "Goblin Sámán",
        "race": "goblin",
        "pclass": "mage",
        "hp": 35,
        "atk": 4,
        "def": 2,
        "magic": 8,
        "speed": 12,
        "mana": 10,
        "spells": [ENEMY_SPELLS["fire_bolt"], ENEMY_SPELLS["curse"]]
    }
]


import random
from enemy import Enemy

def spawn_enemies():
    count = random.randint(1, 3)
    enemies = []
    for _ in range(count):
        base = random.choice(enemy_templates)
        enemy = Enemy(
            name=base["name"],
            race=base["race"],
            pclass=base["pclass"],
            hp=base["hp"],
            atk=base["atk"],
            defense=base["def"],
            magic=base["magic"],
            speed=base["speed"]
        )
        enemies.append(enemy)
    return enemies
