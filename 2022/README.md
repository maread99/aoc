# 2022 aoc solutions

See the [main README](https://github.com/maread99/aoc) for notes on how I go about aoc. There are also some decent references there.

## Reference

### Summary of key features of solutions

[1](./day01.py) #accumulation

[2](./day02.py) #accumulation &nbsp;#mappings

[3](./day03.py) #sets &nbsp;#codepoints-ord &nbsp;#accumulation

[4](./day04.py) #sets &nbsp;#counting

[5](./day05.py) #stack

[6](./day06.py) #sets &nbsp;#iteration

**No Space Left On Device**. Evaluate directory sizes.  
[7](./day07.py) #recursion  
[7_rev](./day07_rev.py) #stack  
[7_alt2](./day07_alt2.py) Holy Grail solution. #stuctural-pattern-matching and uses `itertools.accumulate` to create all locations on route to a directory.  

[8](./day08.py) represent and query a #grid using numpy #arrays.  
[8_alt](./day08_alt.py) use #vectors to navigate a #grid represented with a dict.  

[9](./day09.py) #arrays and #vectors to navigate a grid  
[9_alt](./day09_alt.py) #complex-numbers and #vectors to navigate a grid  

[10](./day10.py) #functional-programming  

[11_rev](./day11_rev.py) #exponential. Reduce an exponentially growing value in such a way as to maintain its integrity. Here by dividing by lowest-commmon-multiple #LCM. Also #stack  

**Hill Climbing Algorithm**  
[12_rev](./day12_rev.py) Breadth-first search #BFS. Using #vectors to navigate a #grid represented with a dict. Also #codepoints-ord &nbsp;#counting

**Distress Signal**
[13_rev](./day13_rev.py) #sort with a comparison function. Also #codify-rules &nbsp;#compare  
[13_rev2](./day13_rev2.py) Also #stuctural-pattern-matching

**Regolith Reservoir**  
[14](./day14.py) #sets to represent content in a #grid. Also #recursion  

**Beacon Exclusion Zone**  
[15](./day15.py)  #intervals  
[15](./day15_rev.py)  #intervals  

**Proboscidea Volcanium**  
[16](./day16_rev.py)  Both depth-first search (#DFS) and #BFS. Also #bitwise-ops  
[16](./day16_rev2.py)  Improved #bitwise-ops for part b  

**Pyroclastic Flow** (Tetris)  
[17](./day17.py) #sets and #complex-numbers to represent content in a #grid. Also identifying #patterns  

**Boiling Boulders**  
[18](./day18.py) using #sets to represent content in #3d space. Also #BFS  

**Not Enough Minerals** (Robots)  
[19](./day19.py) #DFS in which optimizations are key and #tuples used to record states  

**Grove Positioning System**  
[20](./day20.py) list manipulation  

**Monkey Math**  
[21](./day21.py) #trial-and-error  

**Monkey Map** (The notorious cube)  
[22](./day22.py) #sets to represent content of a #grid navigated with #complex-numbers. deque of complex numbers to represent direction and use of deque.rotate to turn. Mapped wraps  

**Unstable Diffusion**  
[23](./day23.py) #sets to represent content in a grid navigated around with #complex-numbers. Also #codify-rules  

**Blizzard Basin**  
[24](./day24.py) over complicated #DFS when all that was needed was a...  
[24_rev](./day24_rev.py) #BFS. numpy #arrays to represent content in a grid that's navigated with #complex-numbers.  
[24_alt](./day24_alt.py) Within #BFS evaluates as-you-go only what's required, via transformation to original state, rather than evaluating state of all content on every iteration.  

**Full of Hot Air**  
[25](./day25.py)  coverting between arbitrary #number-base  
[25_alt](./day25_alt.py)  
