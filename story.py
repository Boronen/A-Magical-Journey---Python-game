from player import Player
from utils import safe_input_int

def add_side_character(new_character, party):
    print(f"\n📣 Új karakter csatlakozna: {new_character.name} ({new_character.race} {new_character.pclass})")
    main_character = party[0]
    current_side = party[1:]

    if len(party) < 3:
        party.append(new_character)
        print(f"✅ {new_character.name} csatlakozott a partyhoz.")
    else:
        print("⚠️ A party tele van. Válassz ki egy side karaktert, akit lecserélsz:")
        for i, p in enumerate(current_side, 1):
            print(f"{i}. {p.name} ({p.race} {p.pclass})")
        print("0. Mégsem")
        idx = safe_input_int("> ", 0, len(current_side))
        if idx == 0:
            print("❌ Mégsem történt csere.")
        else:
            replaced = current_side[idx - 1]
            party[1 + idx - 1] = new_character
            print(f"🔄 {replaced.name} lecserélve {new_character.name}-re.")
