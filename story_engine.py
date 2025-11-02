from text_loader import load_chapter
from battle import battle
from enemy import spawn_enemies
from utils import safe_input_int

# Karakterstílusok: prefixek, ahogy a szövegben megjelennek
CHARACTER_STYLES = {
    "NARRATOR": "Narrátor",
    "PLAYER": "Te",
    "PLAYER_THOUGHT": "Gondolat",
    "LUA": "Lua",
    "VALERION": "Valerion",
    "ARIA": "Aria",
    "BRANK": "Brank",
    "NIX": "Nix",
    "KAEL": "Kael"
    # Bővíthető további karakterekkel
}

def run_story(chapter_path, player, party):
    scenes = load_chapter(chapter_path, player)

    i = 0
    last_choice = None

    while i < len(scenes):
        scene = scenes[i]
        stype = scene["type"]
        content = scene["content"]

        if stype in CHARACTER_STYLES:
            prefix = CHARACTER_STYLES[stype]
            if "{name}" in prefix:
                prefix = prefix.replace("{name}", player.name)
            for line in content:
                print(f"\n{prefix}: {line}")
                input()

        elif stype == "ACTION":
            print("\nVálassz:")
            for idx, line in enumerate(content, 1):
                print(f"{idx}. {line}")
            last_choice = safe_input_int("> ", 1, len(content))

        elif stype.startswith("RESPONSE"):
            try:
                response_num = int(stype.split("_")[1])
                if response_num == last_choice:
                    for line in content:
                        print(f"\n{line}")
                        input()
            except (IndexError, ValueError):
                pass  # ha nincs szám, vagy nem értelmezhető, átugorjuk

        elif stype == "BATTLE_TRIGGER":
            print("\nHarc következik...")
            enemies = spawn_enemies()
            battle(party, enemies)

        elif stype == "CHAPTER_END":
            for line in content:
                print(f"\n{line}")
                input()
            break

        else:
            for line in content:
                print(f"\n{line}")
                input()

        i += 1
