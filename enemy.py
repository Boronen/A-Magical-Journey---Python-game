import random

class Enemy:
    def __init__(self, name, hp, dmg, defense, gold, exp):
        self.name = name
        self.hp = self.max_hp = hp
        self.dmg = dmg
        self.defense = defense
        self.gold = gold
        self.exp = exp

        self.weakness = "fire"
        self.resistance = "ice"
        self.stunned = False
        self.status_effects = []


enemy_templates = [
    Enemy("Farkas", 30, 6, 2, 10, 15),
    Enemy("Goblin", 40, 8, 4, 12, 20),
    Enemy("Óriás Patkány", 25, 5, 1, 6, 10),
]

def spawn_enemies():
    count = random.randint(1, 3)
    enemies = []
    for _ in range(count):
        base = random.choice(enemy_templates)
        enemies.append(Enemy(
            base.name,
            base.max_hp,
            base.dmg,
            base.defense,
            base.gold,
            base.exp
        ))
    return enemies