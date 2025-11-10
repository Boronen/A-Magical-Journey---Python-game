from player import Player
from characters import Character
from enemy import spawn_enemies
from battle import battle
from item import Item
from spell import Spell
from status import StatusEffect, poison_effect
from save import SaveManager
from story import add_side_character
from utils import safe_input_int
from weapon import get_weapon_by_id

def show_party(party):
    print("\n=== 👥 Aktív Party ===")
    for c in party:
        print(f"{c.name} (lvl {c.level}) — {c.race} {c.pclass}")
        print(f"HP: {c.hp}/{c.max_hp} | Mana: {c.mana}/{c.max_mana}")
        print(f"ATK: {c.attack} | DEF: {c.defense} | MAG: {c.magic} | MDEF: {c.magic_def} | SPD: {c.speed}")
        print("-" * 30)

def parse_give_command(command, character):
    if command.startswith("/give "):
        weapon_id = command[6:].strip().lower()
        weapon = get_weapon_by_id(weapon_id)
        if weapon:
            character.equip_weapon(weapon)
        else:
            print("❌ Ismeretlen fegyver azonosító.")

def debug_menu():
    player = Player()
    hero = Character("Tesztelő", "elf", "mage")

    # Biztonságos spell inicializálás
    if hero.all_spells:
        first = list(hero.all_spells.keys())[0]
        hero.unlocked_spells[first] = hero.all_spells[first]

    player.add_character(hero)
    print("🧪 Debug party létrehozva: Tesztelő (elf mage)")

    while True:
        print("\n=== 🧪 DEBUG MENÜ ===")
        print("1. XP adás")
        print("2. Szintlépés teszt")
        print("3. Spell feloldás")
        print("4. Inventory teszt")
        print("5. Status effekt (mérgezés)")
        print("6. Harc teszt")
        print("7. Mentés / Betöltés")
        print("8. Side karakter csatlakozás")
        print("9. Party statok")
        print("10. Cmd")
        print("0. Kilépés")

        choice = input("> ").strip()
        main = player.party[0] if player.party else None

        if not main:
            print("❌ Nincs karakter a partyban.")
            continue

        if choice == "1":
            xp = safe_input_int("Mennyi XP-t adjunk?: ", 1)
            player.exp += xp
            print(f"✅ {xp} XP hozzáadva a globális játékoshoz.")

        elif choice == "2":
            player.exp += main.level * 20
            print(f"🎉 Szintlépés triggerelve {main.name}-nek.")

        elif choice == "3":
            player.skill_points += 1
            main.skill_points += 1
            main.unlock_spell()

        elif choice == "4":
            potion = Item("Gyógyital", "Gyógyít 10 HP-t", 10)
            player.add_item(potion)
            player.show_inventory()

        elif choice == "5":
            poison = StatusEffect("Mérgezés", 3, poison_effect)
            main.status_effects.append(poison)
            for _ in range(4):
                main.apply_status_effects()

        elif choice == "6":
            enemies = spawn_enemies()
            battle(player.party, enemies)
            for c in player.party:
                c.hp = c.max_hp
            print("🧪 Debug után HP visszaállítva maxra.")

        elif choice == "7":
            SaveManager.save_party(player.party, 1)
            loaded = SaveManager.load_party(1)
            if loaded:
                player.party = loaded
                print("✅ Party betöltve.")
            else:
                print("❌ Betöltés sikertelen.")

        elif choice == "8":
            new_char = Character("Aria", "elf", "mage")
            add_side_character(new_char, player.party)

        elif choice == "9":
            show_party(player.party)

        elif choice == "10":
            cmd = input("Parancs: ").strip()
            parse_give_command(cmd, main)

        elif choice == "0":
            print("👋 Kilépés a debug menüből.")
            break

        else:
            print("❌ Érvénytelen választás.")

if __name__ == "__main__":
    debug_menu()
