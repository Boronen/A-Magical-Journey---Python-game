# character.py

from spell import get_class_spells, Spell
from status import StatusEffect
from weapon import get_weapon_by_id

class Character:
    def __init__(self, name, race, pclass):
        self.name = name
        self.race = race
        self.pclass = pclass
        self.level = 1
        self.exp = 0
        self.max_hp = 30 + self.level * 5
        self.hp = self.max_hp
        self.mana = self.max_mana = 10
        self.attack = 3
        self.defense = 2
        self.magic = 2
        self.magic_def = 2
        self.speed = 5
        self.energy = self.max_energy = 10
        self.status_effects = []
        self.stunned = False
        self.weakness = None
        self.resistance = None
        self.weapon = None
        self.all_spells = get_class_spells(pclass)
        self.unlocked_spells = {}
        if self.all_spells:
            first = list(self.all_spells.keys())[0]
            self.unlocked_spells[first] = self.all_spells[first]

        self.apply_race_bonus()
        self.apply_class_bonus()

    def cast_spell(self, return_all=False):
        if not self.unlocked_spells:
            print("❌ Nincs elérhető spell.")
            return None if not return_all else (None, 0, "neutral", None)

        print("\n=== 🔮 Elérhető spellek ===")
        for i, (sid, s) in enumerate(self.unlocked_spells.items(), 1):
            print(f"{i}. {s.name} ({s.element}, {s.stat})")

        from utils import safe_input_int
        idx = safe_input_int("> Spell választás: ", 1, len(self.unlocked_spells))
        spell = list(self.unlocked_spells.values())[idx - 1]

        mana_cost = spell.get_effects(1).get("mana_cost", 0)
        if self.mana < mana_cost:
            print("❌ Nincs elég mana.")
            return None if not return_all else (spell, 0, spell.element, None)

        self.mana -= mana_cost
        dmg = spell.calculate_damage(self, level=1)
        element = spell.element
        status = spell.get_effects(1).get("status", None)

        if return_all:
            return spell, dmg, element, status
        return dmg

    def apply_race_bonus(self):
        races = {
            "orc": {"hp": 10, "attack": 2, "magic": 0},
            "elf": {"hp": 5, "attack": 1, "magic": 2},
            "human": {"hp": 5, "attack": 1, "magic": 1}
        }
        bonus = races.get(self.race, {})
        self.max_hp += bonus.get("hp", 0)
        self.hp = self.max_hp
        self.attack += bonus.get("attack", 0)
        self.magic += bonus.get("magic", 0)

    def apply_class_bonus(self):
        classes = {
            "warrior": {"attack": 3, "magic": 0},
            "thief": {"attack": 2, "magic": 1},
            "mage": {"attack": 0, "magic": 3}
        }
        bonus = classes.get(self.pclass, {})
        self.attack += bonus.get("attack", 0)
        self.magic += bonus.get("magic", 0)

    def get_attack_element(self):
        return self.weapon.element if self.weapon else "physical"

    def get_attack_damage(self):
        base = self.attack + (self.weapon.bonus_attack if self.weapon else 0)
        return base

    def apply_status_effects(self):
        for effect in self.status_effects[:]:
            effect.apply(self)
            if effect.duration <= 0:
                self.status_effects.remove(effect)

def to_dict(self):
    return {
        "name": self.name,
        "race": self.race,
        "pclass": self.pclass,
        "level": self.level,
        "hp": self.hp,
        "max_hp": self.max_hp,
        "mana": self.mana,
        "max_mana": self.max_mana,
        "attack": self.attack,
        "defense": self.defense,
        "magic": self.magic,
        "magic_def": self.magic_def,
        "speed": self.speed,
        "energy": self.energy,
        "max_energy": self.max_energy,
        "unlocked_spells": [s.spell_id for s in self.unlocked_spells.values()],
        "weapon": self.weapon.name if self.weapon else None
    }

@staticmethod
def from_dict(d):
    c = Character(d["name"], d["race"], d["pclass"])
    c.level = d["level"]
    c.hp = d["hp"]
    c.max_hp = d["max_hp"]
    c.mana = d["mana"]
    c.max_mana = d["max_mana"]
    c.attack = d["attack"]
    c.defense = d["defense"]
    c.magic = d["magic"]
    c.magic_def = d["magic_def"]
    c.speed = d["speed"]
    c.energy = d["energy"]
    c.max_energy = d["max_energy"]
    # Spellek visszatöltése
    all_spells = get_class_spells(d["pclass"])
    c.unlocked_spells = {sid: all_spells[sid] for sid in d.get("unlocked_spells", []) if sid in all_spells}
    # Fegyver visszatöltése
    if d.get("weapon"):
        from weapon import get_weapon_by_id
        c.weapon = get_weapon_by_id(d["weapon"])
    return c
