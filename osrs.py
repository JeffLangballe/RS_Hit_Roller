"""
Exposes functions for calculating maximum hit, accuracy, and level in OSRS.
Provides Player class
Formulas taken from official RuneScape forums
http://services.runescape.com/m=forum/forums.ws?317,318,712,65587452
"""

import math
import random

SECONDS_PER_TICK = 0.6   # Clock speed of OSRS
BASE_EXP_PER_DAMAGE = 4

def hit(max_hit, accuracy):
    """
    Checks for a miss then generates a hit between 0 and max_hit (inclusive)
    """
    if (accuracy > random.random()):
        # Attack lands. Generate a hit between 0 and max_hit
        hit = random.choice(range(max_hit+1))
    else:
        # Attack misses
        hit = 0
    
    return hit

def max_hit(effective_strength_level, strength_bonus):
    """
    Returns maximum hit value for melee and ranged attacks

    Keyword arguments:
    effective_strenth_level -- visible strength level + modifiers
    strength_bonus -- strength bonus given by the in-game equipment interface
    """
    hit = 0.5 * effective_strength_level * (strength_bonus + 64) / 640
    return math.floor(hit)

def accuracy(
        effective_attack_level, attack_bonus,
        effective_defence_level, defence_bonus):
    """
    Returns number from 0-1 indicating chance to hit with a melee or ranged attack

    Keyword arguments:
    effective_attack_level -- visible attacking level (of attacker) + modifiers,
        where the attacking stat is attack or ranged
    attack_bonus -- equipment bonus given by the in-game equipment interface
        for the appropriate attack style (ranged, stab, slash, crush)
    effective_defence_level -- visible defence level (of defender) + modifiers
        Value is given for NPCs in the RuneScape bestiary
    defence_bonus -- equipment bonus given by the in-game equipment interface
        for the appropriate attack style (ranged, magic, stab, slash, crush)
        Value is given for NPCs in the RuneScape bestiary
    """
    attack_roll = _accuracy_roll(effective_attack_level, attack_bonus)
    defence_roll = _accuracy_roll(effective_defence_level, defence_bonus)

    if attack_roll > defence_roll:
        accuracy = 1 - (defence_roll + 2) / (2 * (attack_roll + 1))
    else:
        accuracy = attack_roll / (2 * (defence_roll + 1))
    
    return accuracy

def _accuracy_roll(effective_level, bonus):
    """
    Returns attack (or defence) roll used internally for accuracy calculation
    """
    return effective_level * (bonus + 64)

def effective_level(level, prayer_multiplier, stance_adder, void_multiplier):
    """
    Returns effective strength level after factoring in real level and bonuses

    Keyword arguments:
    level -- Actual level
    prayer_multiplier -- Multiplier given by prayer bonus
    stance_adder -- Adder given by from combat stance selection
    void_multiplier -- Multiplier given by void armour bonus
    """
    effective_level = math.floor(level * prayer_multiplier) + stance_adder + 8
    effective_level = math.floor(effective_level * void_multiplier)
    return effective_level

def get_level(user_experience):
    """ Returns skill level for a given experience value """
    i = 99
    while i > 0:
        if experience[i] <= user_experience:
            return i
        i -= 1
    return null

# Level indicated by index
experience = [
    0, 0, 83, 174, 276, 388, 512, 650, 801, 969, 1154, 1358, 1584, 1833, 2107,
    2411, 2746, 3115, 3523, 3973, 4470, 5018, 5624, 6291, 7028, 8740, 9730,
    10824, 12031, 13363, 14833, 16456, 18247, 20224, 22406, 24815, 27473,
    30408, 33648, 37224, 41171, 45529, 50339, 55649, 61512, 67983, 75127,
    83014, 91721, 111945, 123660, 136594, 150872, 166636, 184040, 203254,
    224466, 247886, 273742, 302288, 333804, 368599, 407015, 449428, 496254,
    547953, 605032, 668051, 737627, 814445, 899257, 992895, 1096278, 1336443,
    1475581, 1629200, 1798808, 1986068, 2192818, 2421087, 2673114, 2951373,
    3258594, 3597792, 3972294, 4385776, 4842295, 5346332, 5902831, 6517253,
    7195629, 7944614, 8771558, 9684577, 10692629, 11805606, 13034431
]