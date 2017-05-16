#!/usr/bin/python
"""
Command line tool for finding the most efficient order to level up melee stats
"""

from enum import Enum
import osrs

def main():
    # TODO
    sys.exit(0)

def get_dps(max_hit, accuracy, ticks_per_attack):
    """ Returns estimated damage per second (dps) """
    average_hit = max_hit / 2 * accuracy
    attacks_per_second = 1 / (ticks_per_attack + osrs.SECONDS_PER_TICK)
    return average_hit * attacks_per_second


def get_max_hit_and_accuracy(
        attack_level, strength_level,
        attack_bonus, strength_bonus, attack_style):
    """
    Returns tuple of the form, (max_hit, accuracy), for the given levels after
    factoring in the weapons available and the selected attack style.
    Assumes enemy has level 1 defence and 0 defence bonus
    """
    weapon_attack, weapon_strength = get_best_scimitar(attack_level)
    attack_bonus += weapon_attack
    strength_bonus += weapon_strength

    if attack_style == AttackStyle.ATTACK:
        effective_attack = osrs.effective_level(attack_level, 1, 3, 1)
        effective_strength = osrs.effective_level(strength_level, 1, 0, 1)
    elif attack_style == AttackStyle.STRENGTH:
        effective_attack = osrs.effective_level(attack_level, 1, 0, 1)
        effective_strength = osrs.effective_level(strength_level, 1, 3, 1)

    enemy_effective_defence = osrs.effective_level(1, 1, 0, 1)

    max_hit = osrs.max_hit(effective_strength, strength_bonus)
    accuracy = osrs.accuracy(effective_attack, attack_bonus,
                             enemy_effective_defence, 0)

    return (max_hit, accuracy)

def get_best_scimitar(attack_level):
    """
    Returns tuple of the form (attack_bonus, strength_bonus)
    for the best scimitar (weapon) at a given attack level.
    Scimitars are almost always the most efficient weapon for a level
    """
    if attack_level >= 60:
        # Dragon scimitar
        return (67, 66)
    elif attack_level >= 40:
        # Rune scimitar
        return (45, 44)
    elif attack_level >= 30:
        # Adamant scimitar
        return (29, 28())
    elif attack_level >= 20:
        # Mithril scimitar
        return (21, 20)
    elif attack_level >= 10:
        # Black scimitar
        return (19, 14)
    elif attack_level >= 5:
        # Steel scimitar
        return (15, 14)
    else:
        # Iron scimitar
        return  (10, 9)

def get_max_hit_increases(
        start_strength_level, end_strength_level, strength_bonus,
        prayer_multiplier, stance_adder):
    """
    Returns list of tuples of the form (level, max_hit) for levels between
    start_strength_level and end_strength_level that increase max_hit.
    Assumes start_strength_level < end_strength_level and nonzero multipliers

    Keyword arguments:
    start_strength_level -- Current (starting) strength level
    end_strength_level -- Target (end) strength level
    prayer_multiplier -- Multiplier given by prayer bonus
    stance_adder -- Adder given by from combat stance selection
    void_multiplier -- Multiplier given by void armour bonus
    """
    greatest_max_hit = 0
    max_hit_increases = []
    cur_strength_level = start_strength_level
    while cur_strength_level < end_strength_level:
        effective_strength = osrs.effective_level(
            cur_strength_level,
            prayer_multiplier,
            stance_adder,
            void_multiplier)
        max_hit = osrs.max_hit(effective_strength, strength_bonus)

        if max_hit > greatest_max_hit:
            greatest_max_hit = max_hit
            max_hit_increases.append((cur_strength_level, max_hit))

        cur_strength_level += 1

class AttackStyle(Enum):
    ATTACK = 1      # Gain attack exp and give +3 effective attack
    STRENGTH = 2    # Gain strength exp and give +3 effective strength

if __name__ == "__main__":
    main()
