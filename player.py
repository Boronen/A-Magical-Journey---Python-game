from spell import get_class_spells, Spell
from item import Item
from status import StatusEffect
import json

class Player:
    def __init__(self, name, race, pclass):
        self.name = name
        self.race = race
        self.pclass = pclass
        self.level = 1
        self.hp = self.max_hp = 30
        self.mana = self.max_mana = 10
        self.attack = 3
        self.defense = 2
        self.magic = 2
        self.gold = 0
        self.exp = 0
        self.skill_points = 0
        self.energy = self.max_energy = 10
        self.inventory = []
        self.all_spells = get_class_spells(pclass)
        self.unlocked_spells = {
            list(self.all_spells.keys())[0]: self.all_spells[list(self.all_spells.keys())[0]]
        }
        self.weapon = None
        self.apply_race_bonus()
        self.apply_class_bonus()
        self.status_effects = []
        self.stunned = False
        self.weakness = None
        self.resistance= None

    # ✅ Ezek már a Player osztály metódusai, nem az __init__ belsejében

    def equip_weapon(self, weapon):
        self.weapon = weapon
        print(f"🗡️ {self.name} felszerelte: {weapon.name} ({weapon.element})")

    def get_attack_element(self):
        return self.weapon.element if self.weapon else "physical"

    def get_attack_damage(self):
        base = self.attack + (self.weapon.bonus_attack if self.weapon else 0)
        return base

    def try_weapon_special(self, target):
        if self.weapon:
            return self.weapon.try_special(target, self)

    # === Bónuszok ===
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

    # === Statok ===
    def show_stats(self):
        print(f"\n--- {self.name} ---")
        print(f"Race: {self.race}, Class: {self.pclass}, Level: {self.level}")
        print(f"HP: {self.hp}/{self.max_hp} | Mana: {self.mana}/{self.max_mana}")
        print(f"Attack: {self.attack}, Magic: {self.magic}, Defense: {self.defense}")
        print(f"Gold: {self.gold}, EXP: {self.exp}, Skill Points: {self.skill_points}")

    # === Inventory ===
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

    def cast_spell(self, return_all=False):
        spell_list = list(self.unlocked_spells.values())
        print("\n--- Spellek ---")
        for i, s in enumerate(spell_list, 1):
            print(f"{i}. {s.name} (Mana: {s.mana_cost}, DMG: {s.damage(self.magic)}) Lv{s.level}")
        from utils import safe_input_int
        idx = safe_input_int("> Spell választás: ", 1, len(spell_list))
        spell = spell_list[idx - 1]
        if self.mana >= spell.mana_cost:
            self.mana -= spell.mana_cost
            dmg = spell.damage(self.magic)
            element = getattr(spell, "element", "arcane")
            effect = getattr(spell, "status_effect", None)
            if return_all:
                return spell, dmg, element, effect
            return dmg
        else:
            print("❌ Nincs elég mana!")
            if return_all:
                return None, 0, "arcane", None
            return 0

    def unlock_spell(self):
        locked = [name for name in self.all_spells if name not in self.unlocked_spells]
        if not locked or self.skill_points <= 0:
            print("❌ Nincs új spell vagy skill pont.")
            return
        print("--- Elérhető spellek ---")
        for i, name in enumerate(locked, 1):
            print(f"{i}. {name}")
        from utils import safe_input_int
        idx = safe_input_int("> Válassz spell-t: ", 1, len(locked))
        chosen = locked[idx-1]
        self.unlocked_spells[chosen] = self.all_spells[chosen]
        self.skill_points -= 1
        print(f"✅ {chosen} feloldva!")

    # === EXP / Level ===
    def gain_exp(self, amount):
        self.exp += amount
        needed = self.level * 20
        if self.exp >= needed:
            self.exp -= needed
            self.level += 1
            self.max_hp += 5
            self.max_mana += 3
            self.attack += 1
            self.magic += 1
            self.skill_points += 1
            print(f"🎉 {self.name} szintet lépett ({self.level})! Skill pont kapva!")

    # === Status effektek ===
    def apply_status_effects(self):
        for effect in self.status_effects[:]:
            effect.apply(self)
            if effect.duration <= 0:
                self.status_effects.remove(effect)

    # === Mentés / Betöltés ===
    def to_dict(self):
        return {
            "name": self.name, "race": self.race, "pclass": self.pclass,
            "level": self.level,
            "hp": self.hp, "max_hp": self.max_hp,
            "mana": self.mana, "max_mana": self.max_mana,
            "attack": self.attack, "defense": self.defense, "magic": self.magic,
            "gold": self.gold, "exp": self.exp,
            "skill_points": self.skill_points,
            "inventory": [i.to_dict() for i in self.inventory],
            "spells": {n: s.to_dict() for n, s in self.unlocked_spells.items()}
        }

    @staticmethod
    def from_dict(d):
        p = Player(d["name"], d["race"], d["pclass"])
        p.level = d["level"]
        p.hp = d["hp"]; p.max_hp = d["max_hp"]
        p.mana = d["mana"]; p.max_mana = d["max_mana"]
        p.attack = d["attack"]; p.defense = d["defense"]; p.magic = d["magic"]
        p.gold = d["gold"]; p.exp = d["exp"]
        p.skill_points = d.get("skill_points", 0)
        p.inventory = [Item.from_dict(i) for i in d["inventory"]]
        p.unlocked_spells = {n: Spell.from_dict(s) for n, s in d["spells"].items()}
        return p
