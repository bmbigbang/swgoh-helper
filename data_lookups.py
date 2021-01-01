

unit_stats = {
  0: "None",
  1: "Health",
  2: "Strength",
  3: "Agility",
  4: "Intelligence",
  5: "Speed",
  6: "AttackDamage",
  7: "AbilityPower",
  8: "Armor",
  9: "Suppression",
  10: "ArmorPenetration",
  11: "SuppressionPenetration",
  12: "DodgeRating",
  13: "DeflectionRating",
  14: "AttackCriticalRating",
  15: "AbilityCriticalRating",
  16: "CriticalDamage",
  17: "Accuracy",
  18: "Resistance",
  19: "DodgePercentAdditive",
  20: "DeflectionPercentAdditive",
  21: "AttackCriticalPercentAdditive",
  22: "AbilityCriticalPercentAdditive",
  23: "ArmorPercentAdditive",
  24: "SuppressionPercentAdditive",
  25: "ArmorPenetrationPercentAdditive",
  26: "SuppressionPenetrationPercentAdditive",
  27: "HealthSteal",
  28: "MaxShield",
  29: "ShieldPenetration",
  30: "HealthRegen",
  31: "AttackDamagePercentAdditive",
  32: "AbilityPowerPercentAdditive",
  33: "DodgeNegatePercentAdditive",
  34: "DeflectionNegatePercentAdditive",
  35: "AttackCriticalNegatePercentAdditive",
  36: "AbilityCriticalNegatePercentAdditive",
  37: "DodgeNegateRating",
  38: "DeflectionNegateRating",
  39: "AttackCriticalNegateRating",
  40: "AbilityCriticalNegateRating",
  41: "Offense",
  42: "Defense",
  43: "DefensePenetration",
  44: "EvasionRating",
  45: "CriticalRating",
  46: "EvasionNegateRating",
  47: "CriticalNegateRating",
  48: "OffensePercentAdditive",
  49: "DefensePercentAdditive",
  50: "DefensePenetrationPercentAdditive",
  51: "EvasionPercentAdditive",
  52: "EvasionNegatePercentAdditive",
  53: "CriticalChancePercentAdditive",
  54: "CriticalNegateChancePercentAdditive",
  55: "MaxHealthPercentAdditive",
  56: "MaxShieldPercentAdditive",
  57: "SpeedPercentAdditive",
  58: "CounterAttackRating",
  59: "Taunt"
}

mod_set_stats = {
    1: {
        "name": "Health",
        "setCount": 2,
        "stat": [unit_stats[55], 10]
    },
    2: {
        "name": "Offence",
        "setCount": 4,
        "stat": [unit_stats[48], 15]
    },
    3: {
        "name": "Defense",
        "setCount": 2,
        "stat": [unit_stats[49], 25]
    },
    4: {
        "name": "Speed",
        "setCount": 4,
        "stat": [unit_stats[57], 10]
    },
    5: {
        "name": "Crit Chance",
        "setCount": 2,
        "stat": [unit_stats[53], 8]
    },
    6: {
        "name": "Crit Damage",
        "setCount": 4,
        "stat": [unit_stats[16], 30]
    },
    7: {
        "name": "Potency",
        "setCount": 2,
        "stat": [unit_stats[17], 15]
    },
    8: {
        "name": "Tenacity",
        "setCount": 2,
        "stat": [unit_stats[18], 20]
    },
}

mod_slots = {
    0: "Square",
    1: "Arrow",
    2: "Diamond",
    3: "Triangle",
    4: "Circle",
    5: "Cross"
}