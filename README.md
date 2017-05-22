# OSRS Efficiency Planner

Simulates combat in Old School Runescape for efficiency planning using Python.

## Features:
 - Plans most efficient level-up order based on equipment and current level
 - Automatic weapon selection based on level
 - exp/hr simulations against enemies of varying hitpoints and defence
 - Python module exposing OSRS combat formulas and variables

### Requirements:
 - Python 3.x

### Usage:
From the command line:
```
python efficiency_planner.py <start_ATK> <start_STR> <end_ATK> <end_STR> <ATK_bonus> <STR_bonus>
```
The program automatically selects the best scimitar available for a given attack level. The input ATK and STR bonuses should NOT include any bonus from the weapon.

### In Progress:
 - Optimize combat simulation
 - Optimize level-up time calculations (from simulation)

### Planned:
 - Graphical frontend
 - Weapon and armour database
 - Enemy database
 - Effect of defensive stats on efficiency (resupply frequency)
 - Documentation