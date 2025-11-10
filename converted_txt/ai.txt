# ai.py

import random

def choose_enemy_action(enemy, targets):
    # Ha nincs spell vagy nincs mana, fizikai támadás
    usable_spells = [
        s for s in enemy.spells
        if enemy.mana >= s.get_effects(1).get("mana_cost", 0)
    ]

    if not usable_spells or random.random() < 0.3:
        return {"type": "attack", "target": random.choice(targets)}

    spell = random.choice(usable_spells)
    target = random.choice(targets)
    return {"type": "spell", "spell": spell, "target": target}

levels={
    1: {"damage": 6, "mana_cost": 4},
    2: {"bonus_damage": 4, "mana_cost": 5},
    3: {"status": ["burn"], "duration": 2, "mana_cost": 6}
}
