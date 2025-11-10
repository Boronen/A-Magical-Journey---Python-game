import os

def load_chapter(filepath, player):
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"A fájl nem található: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    scenes = []
    current_scene = {"type": None, "content": []}

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        if line.startswith("[") and line.endswith("]"):
            if current_scene["type"] is not None:
                scenes.append(current_scene)
            current_scene = {"type": line[1:-1], "content": []}
        else:
            if player.party and player.party[0].name:
                line = line.replace("{player_name}", player.party[0].name)
            current_scene["content"].append(line)

    if current_scene["type"]:
        scenes.append(current_scene)

    return scenes
