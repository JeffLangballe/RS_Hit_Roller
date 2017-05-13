#!/usr/bin/python
"""
Command line tool for calculating time to achieve a desired exp gain in OSRS
with static stats
"""

import sys
import combat_formulas as combat

TICKS_PER_SECOND = 20.0   # Clock speed of OSRS
BASE_EXP_PER_DAMAGE = 4

def ticks_until_exp(max_hit, accuracy, ticks_per_attack, enemy_health,
                 desired_exp_gain, exp_per_damage, iterations):
    """
    Simulates battles and returns average number of ticks to achieve exp goal
    """
    total_ticks = 0
    i = 0
    while i < iterations:
        cur_exp = 0
        while cur_exp < desired_exp_gain:
            cur_health = enemy_health
            while cur_health > 0:
                # Simulate an attack
                damage = combat.hit(max_hit, accuracy)
                
                # Limit damage to maximum health
                if damage > cur_health:
                    damage = cur_health
                
                # Deal damage and update exp count
                cur_health -= damage
                cur_exp += damage * exp_per_damage
                total_ticks += ticks_per_attack

                # Check if exp goal reached before enemy is killed
                if cur_exp >= desired_exp_gain:
                    break


    average_ticks = total_ticks / iterations
    return average_ticks

if __name__ == '__main__':
    if len(sys.argv) < 11:
        print('Not enough arguments for OSRS combat simulator', file=sys.stderr)
        sys.exit(1)

    # Read in user stats
    effective_attack = sys.argv[0]
    attack_bonus = sys.argv[1]
    effective_strength = sys.argv[2]
    strength_bonus = sys.argv[3]
    ticks_per_attack = sys.argv[4]
    desired_exp_gain = sys.argv[5]

    # Read in enemy stats
    effective_defence = sys.argv[6]
    defence_bonus = sys.argv[7]
    enemy_health = sys.argv[8]
    exp_multiplier = sys.argv[9]

    num_iterations = sys.argv[10]

    # Calculate combat stats
    max_hit = combat.max_hit(effective_strength, strength_bonus)
    accuracy = combat.accuracy(effective_attack, attack_bonus,
                               effective_defence, defence_bonus)
    exp_per_damage = BASE_EXP_PER_DAMAGE * exp_multiplier
    
    # Calculate time for desired exp gain
    ticks = ticks_until_exp(max_hit, accuracy, ticks_per_attack, enemy_health,
                            desired_exp_gain, exp_per_damage, num_iterations)
    total_seconds = ticks / TICKS_PER_SECOND
    total_minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(total_minutes, 60)

    # Output formatted time
    print('It will take %d:%02d:%02d to gain %d experience'
        % (hours, minutes, seconds, desired_exp_gain))
