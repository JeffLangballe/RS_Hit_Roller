#!/usr/bin/python
"""
Command line tool for finding the most efficient order to level up melee stats
"""

import sys
from enum import Enum
import osrs
import combat_simulator

# Number of simulations for each level-up calculation
ITERATIONS = 100

def main():
    # Read in command-line arguments
    start_attack_level = int(sys.argv[1])
    start_strength_level = int(sys.argv[2])
    end_attack_level = int(sys.argv[3])
    end_strength_level = int(sys.argv[4])
    base_attack_bonus = int(sys.argv[5])
    base_strength_bonus = int(sys.argv[6])
    ticks_per_attack = int(sys.argv[7])

    # Check for invalid arguments
    if(
            not (1 <= start_attack_level <= 99) or
            not (1 <= start_strength_level <= 99) or
            not (1 <= end_attack_level <= 99) or
            not (1 <= end_strength_level <= 99)):
        print('Input level outside of valid OSRS bounds [1,99]',
            file=sys.stderr)
        sys.exit(1)

    if(start_attack_level >= end_attack_level or
            start_strength_level >= end_strength_level):
        print('Error. Start levels must be less than end levels',
            file=sys.stderr)
        sys.exit(1)

    # Create all level pairs and find distances between them
    graph = dict()
    start = Level_Pair(start_attack_level, start_strength_level)
    end = Level_Pair(end_attack_level, end_strength_level)
    populate_graph(graph, start, end,
        base_attack_bonus, base_strength_bonus, ticks_per_attack)
    
    # Solve for shortest path with Dijkstra's algorithm
    path = shortest_path(graph, start, end)

    # Display path
    print('Level-up order is:')
    for levels in path:
        print('Attack =', levels.attack, ' Strength =', levels.strength)

    sys.exit(0)

def shortest_path(graph, start, end):
    """
    Finds shortest path from start node to end node on weighted graph
    using Dijkstra's algorithm

    Keywork arguments:
    graph -- Dict of dicts where graph[A] is a dict mapping A's neighbours to
        their distances from A. ie. graph[A][B] is distance from A to B
    start -- Starting node. Assumed to be in graph
    end -- Ending node. Assumed to be in graph
    """
    nodes_to_visit = {start}
    visited_nodes = set()
    # Distance from start to start is 0
    distance_from_start = {start: 0}
    tentative_parents = {}

    while nodes_to_visit:
        # The next node should be the one with the smallest weight
        current = min(
            [(distance_from_start[node], node) for node in nodes_to_visit]
        )[1]

        # The end was reached
        if current == end:
            break

        nodes_to_visit.discard(current)
        visited_nodes.add(current)

        edges = graph[current]
        unvisited_neighbours = set(edges).difference(visited_nodes)
        for neighbour in unvisited_neighbours:
            neighbour_distance = distance_from_start[current] + \
                                 edges[neighbour]
            if neighbour_distance < distance_from_start.get(neighbour,
                                                            float('inf')):
                distance_from_start[neighbour] = neighbour_distance
                tentative_parents[neighbour] = current
                nodes_to_visit.add(neighbour)

    return _deconstruct_path(tentative_parents, end)

def _deconstruct_path(tentative_parents, end):
    """ Returns list of nodes from """
    if end not in tentative_parents:
        return None
    cursor = end
    path = []
    while cursor:
        path.append(cursor)
        cursor = tentative_parents.get(cursor)
    return list(reversed(path))

def populate_graph(
        graph, start, end, attack_bonus, strength_bonus, ticks_per_attack):
    """
    Recursively creates Level_Pair nodes from start up to end.
    Assumes that end's attack and strength are greater than start's.
    Neighbours for a node are stored in graph[node].
    Distances between neighbours are stored in graph[nodeA][nodeB].
    """

    # Check if already created
    if start in graph:
        return
    
    graph[start] = dict()

    # Recursively create neighbouring level pairs
    if start.attack < end.attack:
        inc_attack = Level_Pair(start.attack + 1, start.strength)
        graph[start][inc_attack] = level_time(start, Attack_Style.ATTACK,
            attack_bonus, strength_bonus, ticks_per_attack)
        populate_graph(graph, inc_attack, end,
            attack_bonus, strength_bonus, ticks_per_attack)
    
    if start.strength < end.strength:
        inc_strength = Level_Pair(start.attack, start.strength + 1)
        graph[start][inc_strength] = level_time(start, Attack_Style.STRENGTH,
            attack_bonus, strength_bonus, ticks_per_attack)
        populate_graph(graph, inc_strength, end,
            attack_bonus, strength_bonus, ticks_per_attack)

def level_time(start_levels, attack_style, attack_bonus, strength_bonus, ticks_per_attack):
    """
    Runs simulations to determine time to level up attack or strength from
    starting level
    Enemy is set as sand crab (60hp, 1 def, 0 def bonus)
    """
    max_hit, accuracy = get_max_hit_and_accuracy(start_levels, attack_style,
        attack_bonus, strength_bonus)
    
    if attack_style == Attack_Style.ATTACK:
        start_exp = osrs.experience[start_levels.attack]
        end_exp = osrs.experience[start_levels.attack+1]
    elif attack_style == Attack_Style.STRENGTH:
        start_exp = osrs.experience[start_levels.strength]
        end_exp = osrs.experience[start_levels.strength+1]
    
    #experience = end_exp - start_exp
    #avg_ticks = combat_simulator.ticks_until_exp(max_hit, accuracy,
    #    ticks_per_attack, 60, experience, osrs.BASE_EXP_PER_DAMAGE, ITERATIONS)
    #return avg_ticks
    weight = 1 / (accuracy * max_hit / 2)
    return weight
        
def get_dps(max_hit, accuracy, ticks_per_attack):
    """ Returns estimated damage per second (dps) """
    average_hit = max_hit / 2 * accuracy
    attacks_per_second = 1 / (ticks_per_attack * osrs.SECONDS_PER_TICK)
    return average_hit * attacks_per_second

def get_max_hit_and_accuracy(
        levels, attack_style, attack_bonus, strength_bonus):
    """
    Returns tuple of the form, (max_hit, accuracy), for the given levels after
    factoring in the weapons available and the selected attack style.
    Assumes enemy has level 1 defence and 0 defence bonus
    """
    weapon_attack, weapon_strength = get_best_scimitar(levels.attack)
    attack_bonus += weapon_attack
    strength_bonus += weapon_strength

    if attack_style == Attack_Style.ATTACK:
        effective_attack = osrs.effective_level(levels.attack, 1, 3, 1)
        effective_strength = osrs.effective_level(levels.strength, 1, 0, 1)
    elif attack_style == Attack_Style.STRENGTH:
        effective_attack = osrs.effective_level(levels.attack, 1, 0, 1)
        effective_strength = osrs.effective_level(levels.strength, 1, 3, 1)

    enemy_effective_defence = osrs.effective_level(1, 1, 0, 1)

    max_hit = osrs.max_hit(effective_strength, strength_bonus)
    accuracy = osrs.accuracy(effective_attack, attack_bonus,
                             enemy_effective_defence, 0)

    return (max_hit, accuracy)

def get_best_scimitar(attack_level):
    """
    Returns tuple of the form (attack_bonus, strength_bonus)
    for the best scimitar (weapon) at a given attack level.
    Scimitars are almost always the most efficient weapon
    """
    if attack_level >= 60:
        # Dragon scimitar
        return (67, 66)
    elif attack_level >= 40:
        # Rune scimitar
        return (45, 44)
    elif attack_level >= 30:
        # Adamant scimitar
        return (29, 28)
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
        start_strength_level, end_strength_level,
        strength_bonus, stance_adder):
    """
    Returns list of tuples of the form (level, max_hit) for levels between
    start_strength_level and end_strength_level that increase max_hit.
    Assumes start_strength_level < end_strength_level and no multipliers

    Keyword arguments:
    start_strength_level -- Current (starting) strength level
    end_strength_level -- Target (end) strength level
    stance_adder -- Adder given by from combat stance selection
    """
    greatest_max_hit = 0
    max_hit_increases = []
    cur_strength_level = start_strength_level
    while cur_strength_level < end_strength_level:
        effective_strength = osrs.effective_level(
            cur_strength_level, 1, stance_adder, 1)
        max_hit = osrs.max_hit(effective_strength, strength_bonus)

        if max_hit > greatest_max_hit:
            greatest_max_hit = max_hit
            max_hit_increases.append((cur_strength_level, max_hit))

        cur_strength_level += 1

class Attack_Style(Enum):
    ATTACK = 1      # Gain attack exp and give +3 effective attack
    STRENGTH = 2    # Gain strength exp and give +3 effective strength

# Contains attack, strength level pairs for use with Dijkstra's algorithm
class Level_Pair(object):
    def __init__(self, attack, strength):
        self.attack = attack
        self.strength = strength
    
    # Make pair usable as dictionary keys
    def __hash__(self):
        return hash((self.attack, self.strength))

    def __eq__(self,other):
        return(self.attack, self.strength) == (other.attack, other.strength)
    
    def __ne__(self, other):
        return not(self == other)

if __name__ == "__main__":
    main()
