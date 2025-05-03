## Conway's Game of Life

Conway's Game of Life, created in Python for the command line.

Features:

- Automatic start with psudorandom "seed"
- Automatic restart on:
    - An extinction event (no live cells)
    - Complete stasis (no deaths/births since previous generation)
    - Partial stasis with remainder of cells stuck in a 2-4 step repeating pattern
- Runs 1000 times before automatically stopping.

### The game runs with the following rules:
- 1. Any live vell with fewer than 2 live neighbors dies (to represent underpopulation)
- 2. Any live cell with 2-3 live neighbors lives on to the next generation
- 3. Any live cell with more than 3 live neighbors dies (to represent overpopulation)
- 4. Any dead cell with exactly 3 live neighbors becomes alive (to represent reproduction occuring)

### Options
- to reduce size modify the ``row`` and ``col`` numbers
- to reduce (or increase) the speed of the simulation, change the ``sleep()`` number higher (slower) or lower (faster)