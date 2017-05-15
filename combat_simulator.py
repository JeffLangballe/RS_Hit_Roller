#!/usr/bin/python
"""
Command line tool for calculating time to achieve a desired exp gain in OSRS
with static stats
"""

import sys
import osrs_formulas as osrs

SECONDS_PER_TICK = 0.6   # Clock speed of OSRS
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
                damage = osrs.hit(max_hit, accuracy)
                
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
        i += 1


    average_ticks = total_ticks / iterations
    return average_ticks

if __name__ == '__main__':
    if len(sys.argv) < 12:
        print('Not enough arguments for OSRS combat simulator', file=sys.stderr)
        sys.exit(1)

    # Read in user stats
    effective_attack = int(sys.argv[1])
    attack_bonus = int(sys.argv[2])
    effective_strength = int(sys.argv[3])
    strength_bonus = int(sys.argv[4])
    ticks_per_attack = int(sys.argv[5])
    desired_exp_gain = int(sys.argv[6])

    # Read in enemy stats
    effective_defence = int(sys.argv[7])
    defence_bonus = int(sys.argv[8])
    enemy_health = int(sys.argv[9])
    exp_multiplier = float(sys.argv[10])

    num_iterations = int(sys.argv[11])

    # Calculate combat stats
    max_hit = osrs.max_hit(effective_strength, strength_bonus)
    accuracy = osrs.accuracy(effective_attack, attack_bonus,
                               effective_defence, defence_bonus)
    exp_per_damage = BASE_EXP_PER_DAMAGE * exp_multiplier

    if max_hit == 0:
        print('Error, max hit is 0. Check effective strength and bonuses',
            file=sys.stderr)
        sys.exit(1)

    # Calculate time for desired exp gain
    ticks = ticks_until_exp(max_hit, accuracy, ticks_per_attack, enemy_health,
                            desired_exp_gain, exp_per_damage, num_iterations)
    total_seconds = ticks * SECONDS_PER_TICK
    total_minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(total_minutes, 60)

    print('Max hit = ', max_hit)
    print('Accuracy = ', accuracy)
    print('It will take %d:%02d:%02d to gain %d experience'
        % (hours, minutes, seconds, desired_exp_gain))
