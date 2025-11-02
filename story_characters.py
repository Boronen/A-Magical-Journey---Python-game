# story_characters.py

from player import Player
from weapon import get_weapon_by_id

def create_side_character(char_id):
    if char_id == "kael":
        p = Player("Kael", "elf", "mage")
        p.weapon = get_weapon_by_id("sétapálca")
        p.unlocked_spells = {
            "Ice Shard": p.all_spells["Ice Shard"],
            "Ice Pillar": p.all_spells["Ice Pillar"]
        }
        return p

    elif char_id == "brakka":
        p = Player("Brakka", "orc", "warrior")
        p.weapon = get_weapon_by_id("lich-kard")
        p.unlocked_spells = {
            "Power Slash": p.all_spells["Power Slash"],
            "Whirlwind": p.all_spells["Whirlwind"]
        }
        return p

    elif char_id == "nix":
        p = Player("Nix", "human", "thief")
        p.weapon = get_weapon_by_id("lopó-kés")
        p.unlocked_spells = {
            "Poison Dagger": p.all_spells["Poison Dagger"],
            "Shadow Strike": p.all_spells["Shadow Strike"]
        }
        return p

    else:
        return None
