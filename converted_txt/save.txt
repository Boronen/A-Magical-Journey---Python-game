import json
import os
from pathlib import Path
from player import Player

SAVE_DIR = Path.home() / "Documents" / "MagicalJourney" / "Saves"
os.makedirs(SAVE_DIR, exist_ok=True)

class SaveManager:
    @staticmethod
    def path(slot):
        return SAVE_DIR / f"save{slot}.json"

    @staticmethod
    def save_party(party, slot):
        data = [p.to_dict() for p in party]
        with open(SaveManager.path(slot), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ Mentés kész Slot {slot}-ba.")

    @staticmethod
    def load_party(slot):
        path = SaveManager.path(slot)
        if not path.exists():
            print("❌ Nincs mentés ebben a slotban.")
            return None
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Player.from_dict(p) for p in data]
