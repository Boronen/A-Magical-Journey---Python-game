# status.py

class StatusEffect:
    def __init__(self, name, duration, effect_fn, element="neutral"):
        self.name = name
        self.duration = duration
        self.effect_fn = effect_fn
        self.element = element

    def apply(self, target):
        self.effect_fn(target)
        self.duration -= 1

# === Effektfüggvények ===

def stun_effect(target):
    target.stunned = True
    print(f"😵 {target.name} elkábult és nem tud cselekedni!")

def fire_effect(target):
    dmg = 3
    target.hp = max(0, target.hp - dmg)
    print(f"🔥 {target.name} ég ({dmg} tűzsebzés)")

def blizzard_effect(target):
    dmg = 2
    target.hp = max(0, target.hp - dmg)
    target.stunned = True
    print(f"❄️ {target.name} lefagyott ({dmg} jégsebzés + stun)")

def poison_effect(target):
    dmg = 2
    target.hp = max(0, target.hp - dmg)
    print(f"☠️ {target.name} mérgezve ({dmg} sebzés)")
