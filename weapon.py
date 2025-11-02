import random
from status import blizzard_effect, poison_effect

class Weapon:
    def __init__(self, name, description, element, base_damage, level=1, special=None):
        self.name = name
        self.description = description
        self.element = element
        self.base_damage = base_damage
        self.level = level
        self.special = special  # függvény vagy None

    def upgrade(self):
        if self.level < 5:
            self.level += 1
            print(f"⬆️ {self.name} fejlesztve Lv{self.level}")
        else:
            print(f"⚠️ {self.name} már max szintű.")

    def get_damage(self):
        return self.base_damage + self.level * 2

    def try_special(self, target, user):
        if not self.special:
            return None
        chance = min(100, 20 + self.level * 10)  # pl. 30–70%
        if random.randint(1, 100) <= chance:
            return self.special(target, user)
        return None

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "element": self.element,
            "base_damage": self.base_damage,
            "level": self.level,
            "special": self.special.__name__ if self.special else None
        }

    @staticmethod
    def from_dict(d):
        specials = {
            "blizzard_special": blizzard_special,
            "poison_special": poison_special,
            "item_steal_special": item_steal_special,
            "stat_steal_special": stat_steal_special
        }
        special_fn = specials.get(d.get("special"))
        return Weapon(
            d["name"], d["description"], d["element"],
            d["base_damage"], d["level"], special_fn
        )

# === Speciális képességek ===

def blizzard_special(target, user):
    effect = StatusEffect("Blizzard", 3, blizzard_effect, "ice")
    target.status_effects.append(effect)
    print(f"❄️ Blizzard aktiválva {target.name}-ra!")
    return effect

def poison_special(target, user):
    effect = StatusEffect("Poison", 3, poison_effect, "poison")
    target.status_effects.append(effect)
    print(f"☠️ Poison aktiválva {target.name}-ra!")
    return effect

def item_steal_special(target, user):
    loot = Item("Random Potion", "Egy véletlen gyógyító ital", heal_amount=10)
    user.add_item(loot)
    print(f"🎁 {user.name} ellopott egy itemet: {loot.name}")
    return None

def stat_steal_special(target, user):
    percent = random.randint(20, 50) / 100
    stolen_attack = int(target.attack * percent)
    stolen_defense = int(target.defense * percent)
    stolen_magic = int(target.magic * percent)
    effect = StatusEffect("Stat Steal", 5, lambda t: None)
    user.attack += stolen_attack
    user.defense += stolen_defense
    user.magic += stolen_magic
    print(f"🧠 {user.name} ellopta {target.name} statjainak {int(percent*100)}%-át 5 körre!")
    return effect

# === Előre definiált fegyverek ===

def get_weapon_by_id(weapon_id):
    weapons = {
        "sétapálca": Weapon(
            "Sétapálca", "Egyszerű mágikus pálca kezdőknek.",
            "arcane", 5
        ),
        "lich-kard": Weapon(
            "Lich King Kardja", "Fagyos penge, blizzard eséllyel.",
            "ice", 8, special=blizzard_special
        ),
        "lopó-kés": Weapon(
            "Lopó Kés", "Mérgez és néha ellop egy itemet.",
            "poison", 6, special=poison_special
        ),
        "toll": Weapon(
            "Toll", "Legendás tárgy, stat lopás eséllyel.",
            "arcane", 4, special=stat_steal_special
        )
    }
    return weapons.get(weapon_id)
