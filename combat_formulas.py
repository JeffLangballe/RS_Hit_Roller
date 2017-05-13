"""
Exposes functions for calculating maximum hit and accuracy for OSRS
Formulas taken from official RuneScape forums
http://services.runescape.com/m=forum/forums.ws?317,318,712,65587452
"""

import random

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

def accuracy(effective_attack_level, attack_bonus,
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
