from player import Player
from enemy import Enemy, spawn_enemies
from battle import battle
from item import Item
from spell import Spell
from status import StatusEffect, poison_effect
from save import SaveManager
from story import add_side_character
from utils import safe_input_int

def show_party(party):
    print("\n=== 👥 Aktív Party ===")
    for p in party:
        p.show_stats()

from weapon import get_weapon_by_id

def parse_give_command(command, player):
    if command.startswith("/give "):
        weapon_id = command[6:].strip().lower()
        weapon = get_weapon_by_id(weapon_id)
        if weapon:
            player.equip_weapon(weapon)
        else:
            print("❌ Ismeretlen fegyver azonosító.")


def debug_menu():
    party = [Player("Tesztelő", "elf", "mage")]
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

        if choice == "1":
            xp = safe_input_int("Mennyi XP-t adjunk?: ", 1)
            party[0].gain_exp(xp)

        elif choice == "2":
            party[0].gain_exp(party[0].level * 20)

        elif choice == "3":
            party[0].skill_points += 1
            party[0].unlock_spell()

        elif choice == "4":
            potion = Item("Gyógyital", "Gyógyít 10 HP-t", 10)
            party[0].add_item(potion)
            party[0].show_inventory()

        elif choice == "5":
            poison = StatusEffect("Mérgezés", 3, poison_effect)
            party[0].status_effects.append(poison)
            for _ in range(4):
                party[0].apply_status_effects()

        elif choice == "6":
            enemies = spawn_enemies()
            battle(party, enemies)

        elif choice == "7":
            SaveManager.save_party(party, 1)
            loaded = SaveManager.load_party(1)
            if loaded:
                party = loaded
                print("✅ Party betöltve.")

        elif choice == "8":
            new_char = Player("Aria", "elf", "mage")
            add_side_character(new_char, party)

        elif choice == "9":
            show_party(party)

        elif choice == "10":
            cmd = input("Parancs: ").strip()
            parse_give_command(cmd, party[0])

        elif choice == "0":
            print("👋 Kilépés a debug menüből.")
            break

        else:
            print("❌ Érvénytelen választás.")

if __name__ == "__main__":
    debug_menu()
