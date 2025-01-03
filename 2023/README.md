# 2023 aoc solutions

See the [main README](https://github.com/maread99/aoc) for notes on how I go about aoc. There are also some decent references there.

Not a bad year. Got them all out albeit needing...
- a peek elsewhere to realise I'd neglected to include a cache in day 12 😱
- a peek elsewhere to discover sympy for 24b
- to use someone else's solution to get the answer out for 21b which in turn allowed me to debug my own solution by working backwards

## Reference

### Summary of key features of solutions

[1](./01.py) #search &nbsp;#iteration  

[2](./02.py) #loops-nested &nbsp;#defaultdict  &nbsp;#reduce  

[3](./03.py) navigate a #grid with #complex-numbers  
[3_rev](./03_rev.py) #tuples &nbsp;#grid  

[4](./04.py) #sets &nbsp;#defaultdict  

**If You Give A Seed A Fertilizer**  
[5](./05.py) #intervals &nbsp;#mappings  
[5_rev](./05_rev.py) #intervals &nbsp;#mappings &nbsp;#stack &nbsp;#shift  

[6](./06.py) conditional #count and an unnecessary but efficient #binary-search  

[7](./07.py) #codify-rules &nbsp;#sort  
[7_rev](./07_rev.py) #codify-rules &nbsp;#sort &nbsp;#compare  
[7_alt](./07_alt.py) #codify-rules &nbsp;#sort &nbsp;#counting &nbsp;#stuctural-pattern-matching  

[8](./08.py) #LCM  

[9](./09.py) #arrays  
[9_rev](./09_rev.py) #recursion  

[10](./10.py) navigate a #grid with #complex-numbers  (requires hard-coding symbol for S)  
[10_rev](./10_rev.py) navigate a #grid with #complex-numbers  (general solution)  

[11](./11.py) #arrays to represent #grid and #sets to store grid contents. Also #manhattan  

[12](./12.py) #recursion &nbsp;#memoization  
[12_alt](./12_alt.py) #recursion &nbsp;#brute-force.  NB Part a only.  

[13](./13_rev.py) manipulation of #arrays. Also #zip  

[14](./14.py) navigate a #grid with #complex-numbers. Also identifying #patterns &nbsp;#sort  
[14_rev](./14_rev.py) represent grid with numpy #matrix. Also identifying #patterns  

[15](./15.py) #mappings  

[16](./16.py) #complex-numbers and #vectors to navigate a grid  

[17](./17.py) optimized #BFS  
[17_rev](./17_rev.py) #Dijkstra  

[18](./18.py) #BFS &nbsp;#complex-numbers  #areas

[19](./19.py) #recursion  

[20](./20.py) #classes &nbsp;#queue &nbsp;#patterns &nbsp;#LCM  

**Step Counter**  
[21_a](./21_a.py) #BFS  
[21_b](./21_b.py) identifying #patterns &nbsp;#series &nbsp;#BFS  

[22](./22.py) #sets  

**A Long Walk**  
[23_a](./23_a.py) #DFS and navigate a #grid with #complex-numbers  
[23_b](./23_a.py) #DFS &nbsp;#graph  
[23_b_alt](./23_a.py) #DFS &nbsp;#graph &nbsp;#recursion  

**Never Tell Me The Odds**  
[24](./24.py) #vectors &nbsp;#systems &nbsp;#linear-algebra

**Snowverload**  
[25](./25.py) #graph  
[25_vis](./25.ipynb) Using `bqplot.Graph` to visualise #graph cut  
