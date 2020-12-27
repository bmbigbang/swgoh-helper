

unit_stat_enum = [
  "None",
  "Health",
  "Strength",
  "Agility",
  "Intelligence",
  "Speed",
  "AttackDamage",
  "AbilityPower",
  "Armor",
  "Suppression",
  "ArmorPenetration",
  "SuppressionPenetration",
  "DodgeRating",
  "DeflectionRating",
  "AttackCriticalRating",
  "AbilityCriticalRating",
  "CriticalDamage",
  "Accuracy",
  "Resistance",
  "DodgePercentAdditive",
  "DeflectionPercentAdditive",
  "AttackCriticalPercentAdditive",
  "AbilityCriticalPercentAdditive",
  "ArmorPercentAdditive",
  "SuppressionPercentAdditive",
  "ArmorPenetrationPercentAdditive",
  "SuppressionPenetrationPercentAdditive",
  "HealthSteal",
  "MaxShield",
  "ShieldPenetration",
  "HealthRegen",
  "AttackDamagePercentAdditive",
  "AbilityPowerPercentAdditive",
  "DodgeNegatePercentAdditive",
  "DeflectionNegatePercentAdditive",
  "AttackCriticalNegatePercentAdditive",
  "AbilityCriticalNegatePercentAdditive",
  "DodgeNegateRating",
  "DeflectionNegateRating",
  "AttackCriticalNegateRating",
  "AbilityCriticalNegateRating",
  "Offense",
  "Defense",
  "DefensePenetration",
  "EvasionRating",
  "CriticalRating",
  "EvasionNegateRating",
  "CriticalNegateRating",
  "OffensePercentAdditive",
  "DefensePercentAdditive",
  "DefensePenetrationPercentAdditive",
  "EvasionPercentAdditive",
  "EvasionNegatePercentAdditive",
  "CriticalChancePercentAdditive",
  "CriticalNegateChancePercentAdditive",
  "MaxHealthPercentAdditive",
  "MaxShieldPercentAdditive",
  "SpeedPercentAdditive",
  "CounterAttackRating",
  "Taunt"
]

mod_set_stats = {
    1: {
        "name": "Health",
        "setCount": 2,
        "stat": ["UNITSTATMAXHEALTHPERCENTADDITIVE", 10]
    },
    2: {
        "name": "Offence",
        "setCount": 4,
        "stat": ["UNITSTATOFFENSEPERCENTADDITIVE", 15]
    },
    3: {
        "name": "Defense",
        "setCount": 2,
        "stat": ["UNITSTATDEFENSEPERCENTADDITIVE", 25]
    },
    4: {
        "name": "Speed",
        "setCount": 4,
        "stat": ["UNITSTATSPEEDPERCENTADDITIVE", 10]
    },
    5: {
        "name": "Crit Chance",
        "setCount": 2,
        "stat": ["UNITSTATCRITICALCHANCEPERCENTADDITIVE", 8]
    },
    6: {
        "name": "Crit Damage",
        "setCount": 4,
        "stat": ["UNITSTATCRITICALDAMAGE", 30]
    },
    7: {
        "name": "Potency",
        "setCount": 2,
        "stat": ["UNITSTATACCURACY", 15]
    },
    8: {
        "name": "Tenacity",
        "setCount": 2,
        "stat": ["UNITSTATRESISTANCE", 20]
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