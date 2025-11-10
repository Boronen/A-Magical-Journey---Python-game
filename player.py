from item import Item
from characters import Character
import json

class Player:
    def __init__(self):
        self.gold = 0
        self.exp = 0
        self.skill_points = 0
        self.inventory = []
        self.party = []  # List of Character instances

    def add_character(self, character):
        self.party.append(character)

    def add_item(self, item):
        self.inventory.append(item)
        print(f"✅ {item.name} hozzáadva az inventoryhoz.")

    def show_inventory(self):
        if not self.inventory:
            print("📦 Inventory üres")
            return
        for i, it in enumerate(self.inventory, 1):
            print(f"{i}. {it.name} - {it.description}")
        from utils import safe_input_int
        idx = safe_input_int("Használsz valamit? (0 = nem): ", 0, len(self.inventory))
        if idx != 0:
            self.inventory[idx-1].use(self)
            self.inventory.pop(idx-1)

    def to_dict(self):
        return {
            "gold": self.gold,
            "exp": self.exp,
            "skill_points": self.skill_points,
            "inventory": [i.to_dict() for i in self.inventory],
            "party": [c.to_dict() for c in self.party]
        }

    @staticmethod
    def from_dict(d):
        p = Player()
        p.gold = d["gold"]
        p.exp = d["exp"]
        p.skill_points = d.get("skill_points", 0)
        p.inventory = [Item.from_dict(i) for i in d["inventory"]]
        p.party = [Character.from_dict(c) for c in d.get("party", [])]
        return p
