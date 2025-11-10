import random
from utils import safe_input_int
from ai import choose_enemy_action
import spell

def show_battle_status(players, enemies):
    print("\n=== 👥 Party állapot ===")
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

def calculate_elemental_damage(base_dmg, element, target):
    if element == target.weakness:
        return int(base_dmg * 2)
    elif element == target.resistance:
        return int(base_dmg * 0.5)
    else:
        return base_dmg

def battle(players, enemies):
    print("\n⚔️ Harc elkezdődött!")
    round_num = 1

    while not is_party_dead(players) and not is_enemy_dead(enemies):
        print(f"\n=== 🌀 KÖR {round_num} ===")

        # Status effektek alkalmazása
        for c in players + enemies:
            c.stunned = False
            c.apply_status_effects()

        show_battle_status(players, enemies)

        # Harci sorrend speed alapján
        turn_order = sorted(players + enemies, key=lambda c: c.speed, reverse=True)

        for actor in turn_order:
            if actor.hp <= 0 or actor.stunned:
                print(f"⛔ {actor.name} nem tud cselekedni (stun)")
                continue

            is_player = actor in players
            print(f"\n👉 {actor.name} lép ({actor.hp}/{actor.max_hp} HP)")

            if is_player:
                print("1. Támadás  2. Spell  3. Item  4. Analyse")
                choice = input("> ").strip()

                if choice == "1":
                    target = choose_target(enemies)
                    if target:
                        base_dmg = actor.get_attack_damage()
                        element = actor.get_attack_element()
                        dmg = calculate_elemental_damage(base_dmg, element, target)
                        dmg -= target.defense
                        dmg = max(dmg, 0)
                        target.hp -= dmg
                        print(f"💥 {actor.name} megtámadta {target.name}-t ({dmg} dmg, elem: {element})")
                        if hasattr(actor, "try_weapon_special"):
                            actor.try_weapon_special(target)

                elif choice == "2":
                    target = choose_target(enemies)
                    if target:
                        result = actor.cast_spell(return_all=True)
                        if not result or result[0] is None:
                            print(f"❌ {actor.name} nem tud spell-t használni.")
                            continue

                        s, dmg, element, effect = result
                        dmg = calculate_elemental_damage(dmg, element, target)
                        dmg -= target.magic_def
                        dmg = max(dmg, 0)
                        target.hp -= dmg
                        print(f"🪄 {actor.name} varázsolt {s.name}-t {target.name}-ra ({dmg} dmg, elem: {element})")
                        if effect:
                            target.status_effects.append(effect)

                elif choice == "3":
                    actor.show_inventory()

                elif choice == "4":
                    spell.analyze(target)

            else:
                action = choose_enemy_action(actor, players)
                target = action["target"]

                if action["type"] == "attack":
                    base_dmg = actor.get_attack_damage()
                    element = actor.get_attack_element()
                    dmg = calculate_elemental_damage(base_dmg, element, target)
                    dmg -= target.defense
                    dmg = max(dmg, 0)
                    target.hp -= dmg
                    print(f"👾 {actor.name} megtámadta {target.name}-t ({dmg} dmg, elem: {element})")

                elif action["type"] == "spell":
                    spell_obj = action["spell"]
                    dmg = spell_obj.calculate_damage(actor, level=1)
                    element = spell_obj.element
                    dmg = calculate_elemental_damage(dmg, element, target)
                    dmg -= target.magic_def
                    dmg = max(dmg, 0)
                    target.hp -= dmg
                    print(f"🪄 {actor.name} elsüti {spell_obj.name}-t {target.name}-ra ({dmg} dmg, elem: {element})")
                    effect = spell_obj.get_effects(1).get("status")
                    if effect:
                        from status import StatusEffect
                        target.status_effects.append(StatusEffect(effect[0], 2, lambda t: None))

            if target.hp <= 0:
                print(f"☠️ {target.name} elesett!")

        round_num += 1

    # Harc vége után
    if is_party_dead(players):
        print("\n💀 Vereség!")
        for c in players:
            c.hp=1
    else:
        print("\n🎉 Győzelem!")
