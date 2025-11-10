class Item:
    def __init__(self, name, description="", heal_amount=0):
        self.name = name
        self.description = description
        self.heal_amount = heal_amount

    def use(self, player):
        player.hp = min(player.max_hp, player.hp + self.heal_amount)
        print(f"💊 {self.name} +{self.heal_amount} HP (új HP: {player.hp}/{player.max_hp})")

    def to_dict(self):
        return {"name": self.name, "description": self.description, "heal_amount": self.heal_amount}

    @staticmethod
    def from_dict(d):
        return Item(d["name"], d.get("description", ""), d.get("heal_amount", 0))
