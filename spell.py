# spell.py

class Spell:
    def __init__(self, spell_id, name, type_, element, stat, echo_tag, shout, levels, rage_cost=0, condition=None, effect=None):
        self.spell_id = spell_id
        self.name = name
        self.type = type_  # "active", "passive", "ultimate"
        self.element = element  # e.g. "magic", "shadow", "neutral"
        self.stat = stat  # e.g. "magic", "atk", "speed"
        self.echo_tag = echo_tag  # bool
        self.shout = shout  # string
        self.levels = levels  # dict: level → effects
        self.rage_cost = rage_cost  # only for ultimate
        self.condition = condition  # optional trigger condition
        self.effect = effect  # optional static effect (ultimate only)

    def get_effects(self, level):
        return self.levels.get(level, {})

    def calculate_damage(self, caster, level):
        effects = self.get_effects(level)
        base = effects.get("damage", 0)
        bonus = effects.get("bonus_damage", 0)
        scale_stat = getattr(caster, self.stat, 0)
        scaling = 1 + (level * 0.1)
        return int((base + bonus + scale_stat) * scaling)

    def to_dict(self):
        return {
            "spell_id": self.spell_id,
            "name": self.name,
            "type": self.type,
            "element": self.element,
            "stat": self.stat,
            "echo_tag": self.echo_tag,
            "shout": self.shout,
            "levels": self.levels,
            "rage_cost": self.rage_cost,
            "condition": self.condition,
            "effect": self.effect
        }

    @staticmethod
    def from_dict(d):
        return Spell(
            spell_id=d["spell_id"],
            name=d["name"],
            type_=d["type"],
            element=d.get("element", "neutral"),
            stat=d.get("stat", "magic"),
            echo_tag=d.get("echo_tag", False),
            shout=d.get("shout", ""),
            levels=d.get("levels", {}),
            rage_cost=d.get("rage_cost", 0),
            condition=d.get("condition"),
            effect=d.get("effect")
        )

def get_class_spells(pclass):
    if pclass == "thief":
        return load_thief_spells()
    return {}

def load_thief_spells():
    raw = SPELLS_THIEF_MC  # ez a nagy dict, amit már definiáltál
    spells = {}
    for spell_id, data in raw.items():
        spells[spell_id] = Spell(
            spell_id=spell_id,
            name=data["name"],
            type_=data["type"],
            element=data.get("element", "neutral"),
            stat=data.get("stat", "magic"),
            echo_tag=data.get("echo_tag", False),
            shout=data.get("shout", ""),
            levels=data.get("levels", {}),
            rage_cost=data.get("rage_cost", 0),
            condition=data.get("condition"),
            effect=data.get("effect")
        )
    return spells

SPELLS_THIEF_MC = {
    # Aktív spellek
    "echo_blade": {
        "name": "Echo Blade",
        "type": "active",
        "element": "shadow",
        "stat": "atk",
        "echo_tag": True,
        "shout": "Visszhangban születtem — Echo Blade!",
        "levels": {
            1: {"damage": 8},
            2: {"bonus_damage": 3, "condition": "enemy_damaged_last_turn"},
            3: {"crit_chance": 10, "condition": "same_enemy_as_previous_battle"},
            4: {"speed_up": 15, "duration": 1, "condition": "target_died"},
            5: {"trigger_echo_field_on_crit": True}
        }
    },
    "pulse_of_memory": {
        "name": "Pulse of Memory",
        "type": "active",
        "element": "magic",
        "stat": "magic",
        "echo_tag": True,
        "shout": "Emlékszem rád... Pulse of Memory!",
        "levels": {
            1: {"damage": 8, "condition": "enemy_known"},
            2: {"bonus_damage": 5, "condition": "fought_before"},
            3: {"crit_chance": 10, "condition": "from_save"},
            4: {"status": ["silence", "bleed"], "condition": "chapter_match"},
            5: {"status_copy": True, "condition": "enemy_similarity"}
        }
    },
    "thread_sever": {
        "name": "Thread Sever",
        "type": "active",
        "element": "neutral",
        "stat": "atk",
        "echo_tag": False,
        "shout": "Kapcsolat... megszakítva!",
        "levels": {
            1: {"damage": 6, "bonding_change": -1},
            2: {"bonus_damage": 4, "condition": "bonding_below_2"},
            3: {"status": ["stun"], "condition": "bonding_zero"},
            4: {"crit_damage_up": 10, "condition": "target_unbondable"},
            5: {"status": ["fury"], "condition": "bonding_zero_and_low_hp"}
        }
    },
    "silent_step": {
        "name": "Silent Step",
        "type": "active",
        "element": "neutral",
        "stat": "speed",
        "echo_tag": False,
        "shout": "Lépés... ami nem hagy nyomot!",
        "levels": {
            1: {"speed_up": 15, "duration": 2},
            2: {"bonus_damage": 2, "condition": "moved_this_turn"},
            3: {"status": ["vanish"], "duration": 1},
            4: {"hit_rate_up": 10, "condition": "not_targeted"},
            5: {"auto_evade": True, "condition": "hp_below_25"}
        }
    },
    "null_field": {
        "name": "Null Field",
        "type": "active",
        "element": "neutral",
        "stat": "magic",
        "echo_tag": False,
        "shout": "Semmi marad... Null Field!",
        "levels": {
            1: {"remove_buff": True},
            2: {"mana_cost_increase": 2},
            3: {"magic_def_down": 10},
            4: {"physical_def_down": 10},
            5: {"remove_all_enemy_buffs": True, "condition": "echo_field_active"}
        }
    },
    "last_ember": {
        "name": "Last Ember",
        "type": "active",
        "element": "fire",
        "stat": "magic",
        "echo_tag": False,
        "shout": "Az utolsó szikra... égjen el!",
        "levels": {
            1: {"damage": 6},
            2: {"bonus_damage": 6, "condition": "hp_below_30"},
            3: {"crit_chance_up": 20},
            4: {"status": ["bleed"], "duration": 2},
            5: {"status": ["fury"], "condition": "target_dies"}
        }
    },
    "time_fracture": {
        "name": "Time Fracture",
        "type": "active",
        "element": "neutral",
        "stat": "speed",
        "echo_tag": True,
        "shout": "Idő... széttörve!",
        "levels": {
            1: {"speed_up": 20},
            2: {"extra_action": True, "condition": "echo_field_active"},
            3: {"magic_up": 10},
            4: {"status": ["vanish"], "duration": 1},
            5: {"stop_time": True, "condition": "story_flag_active"}
        }
    },
    "grave_mark": {
        "name": "Grave Mark",
        "type": "active",
        "element": "dark",
        "stat": "atk",
        "echo_tag": True,
        "shout": "A sír... nem felejt!",
        "levels": {
            1: {"death_trigger_damage": True},
            2: {"atk_up": 10, "condition": "target_is_undead"},
            3: {"status": ["bleed"], "spread_on_death": True},
            4: {"activate_echo_field": True, "condition": "target_is_boss"},
            5: {"status_spread": True}
        }
    },
    "ash_pulse": {
        "name": "Ash Pulse",
        "type": "active",
        "element": "magic",
        "stat": "magic",
        "echo_tag": False,
        "shout": "Hamuból... csapás!",
        "levels": {
            1: {"damage": 6, "status": ["silence"]},
            2: {"bonus_damage": 4, "condition": "target_is_caster"},
            3: {"status": ["silence"], "duration": 2},
            4: {"mana_cost_increase": 3},
            5: {"spell_lock": True, "duration": 3}
        }
    },
    "shadow_bloom": {
        "name": "Shadow Bloom",
        "type": "active",
        "element": "shadow",
        "stat": "magic",
        "echo_tag": True,
        "shout": "Virágzik... az árnyék!",
        "levels": {
            1: {"damage": 7},
            2: {"bonus_damage": 5, "condition": "target_is_debuffed"},
            3: {"status": ["bleed", "poison"], "duration": 2},
            4: {"crit_chance_up": 10, "condition": "target_moved"},
            5: {"aoe_damage_to_debuffed": True}
        }
    },
    "mind_pierce": {
        "name": "Mind Pierce",
        "type": "active",
        "element": "magic",
        "stat": "magic",
        "echo_tag": False,
        "shout": "Elméd... megtöröm!",
        "levels": {
            1: {"damage": 5, "status": ["stun"], "chance": 50},
            2: {"guaranteed_stun": True, "condition": "target_is_caster"},
            3: {"magic_up": 10, "condition": "target_is_silenced"},
            4: {"crit_damage_up": 20},
            5: {"action_block": True, "duration": 2}
        }
    },
    "flicker_veil": {
        "name": "Flicker Veil",
        "type": "active",
        "element": "neutral",
        "stat": "magic_def",
        "echo_tag": False,
        "shout": "Fátyol... villanjon!",
        "levels": {
            1: {"physical_def_up": 2},
            2: {"reflect_debuff": True},
            3: {"magic_def_up": 10},
            4: {"status": ["vanish"], "duration": 1},
            5: {"reflect_all_debuffs": True}
        }
    },
    "soul_thread": {
        "name": "Soul Thread",
        "type": "active",
        "element": "neutral",
        "stat": "magic",
        "echo_tag": True,
        "shout": "Lélek... összefonódik!",
        "levels": {
            1: {"bonding_up": 1},
            2: {"speed_up": 5, "condition": "bonding_zero"},
            3: {"activate_echo_field": True, "condition": "bonding_zero_and_low_hp"},
            4: {"magic_up": 10, "condition": "not_in_bonding_file"},
            5: {"status_immunity": True, "duration": 1}
        }
    },
    "veinstep": {
        "name": "Veinstep",
        "type": "active",
        "element": "physical",
        "stat": "atk",
        "echo_tag": False,
        "shout": "Lépj... az erek mentén!",
        "levels": {
            1: {"bonus_damage": 3, "condition": "moved_this_turn"},
            2: {"bonus_damage": 5, "condition": "target_moved"},
            3: {"status": ["bleed"], "duration": 2},
            4: {"crit_chance_up": 15},
            5: {"aoe_damage_to_moving_targets": True}
        }
    },
    "glass_echo": {
        "name": "Glass Echo",
        "type": "active",
        "element": "illusion",
        "stat": "magic",
        "echo_tag": True,
        "shout": "Törjön... az üveg visszhang!",
        "levels": {
            1: {"damage": 5, "status": ["illusion"]},
            2: {"status": ["miss"], "duration": 1},
            3: {"physical_def_up": 10},
            4: {"status": ["vanish"], "duration": 1},
            5: {"targeting_block": True}
        }
    },
    # Passzív spellek
    "unseen_bond": {
        "name": "Unseen Bond",
        "type": "passive",
        "levels": {
            1: {"physical_def_up": 2, "condition": "no_bonding"},
            2: {"speed_up": 5, "condition": "lua_lance_absent"},
            3: {"crit_chance_up": 10, "condition": "silent_in_camp"}
        }
    },
    "fate_divergence": {
        "name": "Fate Divergence",
        "type": "passive",
        "levels": {
            1: {"xp_bonus": 5},
            2: {"mana_regen": 1},
            3: {"magic_up": 10, "condition": "not_in_bonding_file"}
        }
    },
    "quiet_resolve": {
        "name": "Quiet Resolve",
        "type": "passive",
        "levels": {
            1: {"magic_def_up": 2, "condition": "silent_in_camp"},
            2: {"hit_rate_up": 5},
            3: {"extra_action": True, "condition": "not_targeted_2_turns"}
        }
    },
    "echo_guard": {
        "name": "Echo Guard",
        "type": "passive",
        "levels": {
            1: {"physical_def_up": 2, "condition": "self_damaged"},
            2: {"magic_def_up": 2, "condition": "ally_damaged"},
            3: {"team_speed_up": 10, "duration": 2, "condition": "self_death"}
        }
    },
    "echo_rebirth": {
        "name": "Echo Rebirth",
        "type": "passive",
        "levels": {
            1: {"echo_spells_boosted": True, "condition": "lua_bonding_3"},
            2: {"activate_echo_field_on_death": True},
            3: {"summon_echo_entity": True, "condition": "lua_bonding_5_and_lance_alive"}
        }
    },
    # Ultimate spellek
    "final_whisper": {
        "name": "Final Whisper",
        "type": "ultimate",
        "element": "shadow",
        "stat": "atk",
        "rage_cost": 100,
        "condition": "hp_below_10",
        "shout": "Ez... az utolsó szavam!",
        "effect": {
            "crit_damage": "max",
            "status": ["silence", "bleed"],
            "activate_echo_field": True
        }
    },
    "memory_collapse": {
        "name": "Memory Collapse",
        "type": "ultimate",
        "element": "magic",
        "stat": "magic",
        "rage_cost": 100,
        "condition": "bonding_zero",
        "shout": "Emlékek... omlanak!",
        "effect": {
            "break_all_enemy_bonding": True,
            "status": ["stun"],
            "speed_down": 20
        }
    },
    "thread_reversal": {
        "name": "Thread Reversal",
        "type": "ultimate",
        "element": "neutral",
        "stat": "magic",
        "rage_cost": 100,
        "condition": "story_flag_active",
        "shout": "Forduljon... a sors fonala!",
        "effect": {
            "revive_ally": ["lua", "lance"],
            "status": ["fury"],
            "target": "enemy_team"
        }
    }
}

