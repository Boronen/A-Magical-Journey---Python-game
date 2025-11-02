import random
from utils import safe_input_int
import spell

def show_battle_status(players, enemies):
    print("\n=== 🧍‍♂️ Party állapot ===")
    for p in players:
        print(f"{p.name:<12} HP: {p.hp:>3}/{p.max_hp:<3} | Mana: {p.mana:>2}/{p.max_mana:<2}")

    print("\n=== 👾 Ellenségek ===")
    for e in enemies:
        print(f"{e.name:<12} HP: {e.hp:>3}/{e.max_hp:<3}")

def choose_target(target_list, prompt="Válassz célpontot"):
    living = [t for t in target_list if t.hp > 0]
    if not living:
        return None
    print(f"\n{prompt}:")
    for i, t in enumerate(living, 1):
        print(f"{i}. {t.name} (HP: {t.hp}/{t.max_hp})")
    idx = safe_input_int("> ", 1, len(living))
    return living[idx - 1]

def is_party_dead(party):
    return all(p.hp <= 0 for p in party)

def is_enemy_dead(enemies):
    return all(e.hp <= 0 for e in enemies)

# battle.py

def calculate_elemental_damage(base_dmg, element, target):
    if element == target.weakness:
        return int(base_dmg * 2)
    elif element == target.resistance:
        return int(base_dmg * 0.5)
    else:
        return base_dmg

def show_battle_status(players, enemies):
    print("\n=== 👥 Party állapot ===")
    for p in players:
        print(f"{p.name:<12} HP: {p.hp:>3}/{p.max_hp:<3} | Mana: {p.mana:>2}/{p.max_mana:<2}")
    print("\n=== 👾 Ellenségek ===")
    for e in enemies:
        print(f"{e.name:<12} HP: {e.hp:>3}/{e.max_hp:<3}")

# battle.py

def calculate_elemental_damage(base_dmg, element, target):
    if element == target.weakness:
        return int(base_dmg * 2)
    elif element == target.resistance:
        return int(base_dmg * 0.5)
    else:
        return base_dmg

# battle.py

def battle(players, enemies):
    print("\n⚔️ Harc elkezdődött!")
    round_num = 1

    while not is_party_dead(players) and not is_enemy_dead(enemies):
        print(f"\n=== 🌀 KÖR {round_num} ===")

        # Status effektek alkalmazása
        for p in players:
            p.stunned = False
            p.apply_status_effects()
        for e in enemies:
            e.stunned = False
            for effect in e.status_effects[:]:
                effect.apply(e)
                if effect.duration <= 0:
                    e.status_effects.remove(effect)

        show_battle_status(players, enemies)

        # Játékos kör
        for player in players:
            if player.hp <= 0 or player.stunned:
                print(f"⛔ {player.name} nem tud cselekedni (stun)")
                continue

            print(f"\n👉 {player.name} lép ({player.hp}/{player.max_hp} HP)")
            print("1. Támadás  2. Spell  3. Item  4. Analyse")
            choice = input("> ").strip()

            if choice == "1":
                target = choose_target(enemies)
                if target:
                    base_dmg = player.get_attack_damage()
                    element = player.get_attack_element()
                    dmg = calculate_elemental_damage(base_dmg, element, target)
                    target.hp -= dmg
                    print(f"💥 {player.name} megtámadta {target.name}-t ({dmg} dmg, elem: {element})")
                    player.try_weapon_special(target)

            elif choice == "2":
                target = choose_target(enemies)
                if target:
                    spell, dmg, element, effect = player.cast_spell(return_all=True)
                    dmg = calculate_elemental_damage(dmg, element, target)
                    target.hp -= dmg
                    print(f"🪄 {player.name} varázsolt {spell.name}-t {target.name}-ra ({dmg} dmg, elem: {element})")
                    if effect:
                        target.status_effects.append(effect)

            elif choice == "3":
                player.show_inventory()

            elif choice == "4":
                spell.analyze(target)

        # Ellenség kör
        for enemy in enemies:
            if enemy.hp <= 0 or enemy.stunned:
                print(f"⛔ {enemy.name} nem tud támadni (stun)")
                continue
            target = random.choice([p for p in players if p.hp > 0])
            base_dmg = enemy.dmg
            element = "physical"
            dmg = calculate_elemental_damage(base_dmg, element, target)
            target.hp -= dmg
            print(f"👾 {enemy.name} megtámadta {target.name}-t ({dmg} dmg)")

        round
