# enemy_spellbook.py

from spell import Spell

ENEMY_SPELLS = {
    "fire_bolt": Spell(
        spell_id="fire_bolt",
        name="Fire Bolt",
        type_="active",
        element="fire",
        stat="magic",
        echo_tag=False,
        shout="Láng... csapj le!",
        levels={
            1: {"damage": 6},
            2: {"bonus_damage": 4, "condition": "target_is_poisoned"},
            3: {"status": ["burn"], "duration": 2}
        }
    ),
    "curse": Spell(
        spell_id="curse",
        name="Curse",
        type_="active",
        element="dark",
        stat="magic",
        echo_tag=False,
        shout="Átok... hulljon rád!",
        levels={
            1: {"status": ["weak"], "duration": 2},
            2: {"magic_def_down": 10},
            3: {"action_block": True, "duration": 1}
        }
    ),
    "shadow_bite": Spell(
        spell_id="shadow_bite",
        name="Shadow Bite",
        type_="active",
        element="shadow",
        stat="atk",
        echo_tag=False,
        shout="Az árnyék harap!",
        levels={
            1: {"damage": 5},
            2: {"status": ["bleed"], "duration": 1},
            3: {"crit_chance_up": 10}
        }
    )
}
