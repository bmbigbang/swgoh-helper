from initialise_data_structures import initialise_data_structures
import re
import json

saved_data = initialise_data_structures()


def use_scaled_effect_if_exists(t, effect_ref_id, using_previous=None):
    effect_id = effect_ref_id.replace("_BASE", "_u0{}".format(t))
    if effect_id not in saved_data["effects"]:
        effect_id = effect_ref_id.replace("_BASE", "_u{}".format(t))

    if effect_id in saved_data["effects"]:
        if using_previous:
            effect_id = re.sub(
                r"\d$",
                str(t + 2),
                effect_id
            )
            return [using_previous, effect_id]
        return [saved_data["effects"][effect_id], effect_id]
    else:
        return None


decimal_scaling_factor = 10000
skill_modifiers = {}
for defId, character in saved_data["toons"].items():
    character_skill_modifiers = {}
    for skill_ref in character['skillReferenceList']:
        c = 0
        skill = saved_data["skills"][skill_ref["skillId"]]
        ability = saved_data["abilities"][skill["abilityReference"]]
        for tier in ability["tierList"]:
            last_effect = None
            for effect_ref in ability["effectReferenceList"]:
                effect = saved_data["effects"][effect_ref["id"]]
                if (
                    ("ATTACK_DAMAGE" in effect['paramList'] or "ABILITY_POWER" in effect['paramList']) and
                    'CONTEXT_MAX_MULTIPLIER' not in effect['paramList']
                ):

                    # skip buffs
                    if any([tag["tag"].endswith("buff") for tag in effect["descriptiveTagList"]]):
                        continue

                    scaled_effect_arr = use_scaled_effect_if_exists(c, effect_ref["id"])
                    if not scaled_effect_arr:
                        if c < 1:
                            scaled_effect_arr = [saved_data["effects"][effect_ref["id"]], effect_ref["id"]]
                        else:
                            scaled_effect_arr = use_scaled_effect_if_exists(
                                c - 1,
                                effect_ref["id"],
                                using_previous=last_effect
                            )

                            if not scaled_effect_arr:
                                # error_effect = scaled_effect_arr[0]
                                # print("Could not find effect: {} at tier {}".format(effect_ref["id"], c))
                                continue

                    new_skill = character_skill_modifiers.get(ability['nameKey'], {})
                    new_tier = new_skill.get(c, {})
                    new_tier[scaled_effect_arr[1]] = [
                        scaled_effect_arr[0]["multiplierAmountDecimal"] / decimal_scaling_factor,
                        scaled_effect_arr[0]["additiveAmountDecimal"] / decimal_scaling_factor,
                        scaled_effect_arr[0]['contextMultiplierDecimal'] / decimal_scaling_factor,
                        scaled_effect_arr[0]['additiveAmountDecimal'] / decimal_scaling_factor,
                    ]
                    new_skill[c] = new_tier
                    character_skill_modifiers[ability['nameKey']] = new_skill

                    last_effect = scaled_effect_arr[0]
            c += 1

    skill_modifiers[defId] = character_skill_modifiers

with open('skill-modifiers.json', 'w', encoding='utf-8') as f:
    json.dump(skill_modifiers, f, ensure_ascii=False, indent=4)
