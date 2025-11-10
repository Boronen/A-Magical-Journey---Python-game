from text_loader import load_chapter
from battle import battle
from enemy import spawn_enemies
from utils import safe_input_int

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
}

def run_story(chapter_path, player, party):
    scenes = load_chapter(chapter_path, player)
    i = 0

    while i < len(scenes):
        scene = scenes[i]
        stype = scene["type"]
        content = scene["content"]

        # RESPONSE blokkokat átugorjuk, mert az ACTION után már feldolgoztuk
        if stype.startswith("RESPONSE"):
            i += 1
            continue

        # ACTION blokk: választás és válasz feldolgozása
        elif stype == "ACTION":
            print("\nVálassz:")
            for idx, line in enumerate(content, 1):
                print(f"{idx}. {line}")

            choice = safe_input_int("> ", 1, len(content))
            chosen_line = content[choice - 1]
            print(f"\nTe választottad: {chosen_line}")
            input()

            # Megkeressük a megfelelő RESPONSE blokkot
            response_key = f"RESPONSE_{choice}"
            j = i + 1
            while j < len(scenes):
                if scenes[j]["type"] == response_key:
                    for line in scenes[j]["content"]:
                        # Prefix alapján kiírás
                        if ":" in line:
                            prefix, text = line.split(":", 1)
                            prefix = prefix.strip()
                            text = text.strip()
                            print(f"\n{prefix}: {text}")
                        else:
                            print(f"\n{line}")
                        input()
                    break
                j += 1
            i = j  # Ugrás a válasz utánra

        # Harc trigger
        elif stype == "BATTLE_TRIGGER":
            print("\nHarc következik...")
            enemies = spawn_enemies()
            battle(party, enemies)

        # Fejezet vége
        elif stype == "CHAPTER_END":
            for line in content:
                print(f"\n{line}")
                input()
            break

        # Karakter dialógus vagy narráció
        elif stype in CHARACTER_STYLES:
            prefix = CHARACTER_STYLES[stype]
            if "{name}" in prefix:
                prefix = prefix.replace("{name}", player.name)
            for line in content:
                print(f"\n{prefix}: {line}")
                input()

        # Egyéb típusok (pl. sima szöveg)
        else:
            for line in content:
                print(f"\n{line}")
                input()

        i += 1
