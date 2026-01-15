# n-puzzle

```
python puzzle.py test_cases/3x3_0.txt
```

## Profiling
```
# Generate the profiling data
python npuzzle-gen.py -s 5 | python -m cProfile -o profile.prof main.py

# View the flamegraph
snakeviz profile.prof

# Testing
cd test_cases
ls -1 | xargs -{} python ../main.py {}
```

## TODO

- [x] add flags (algo, ...)
- [x] greedy and uniform search options
- [x] 3 admissible heuristics
- [x] Implement N-Puzzle Generator (subject file) 15min
- [x] check prints, size & time complexity 10-30min
- [x] bonus : 
    - [x] progress prints, 
    - [x] IDA (RECURSIVITY !) 15-30min
    - [x] animated solve sequence,
    - [x] test arena, 10min
    - [x] Time handling 10min
- [ ] error handelling 10 min
- [ ] final checks 15min
- [ ] handin and corrections 3days


## Pseudo-implementation of A*

```
set opened <- { initial states }
            // States to be examined and candidates to expansion
set closed <- empty
            // States already selected by the algoryth, compared
            // to the solution, and expanded
bool success  <- false

While (opened != empty) and ( not success) do
    state e <- select_according_to_Astar_strategy_in ( opened )
    If is_final ( e ) // Compares 'e' to a solustion state
        Then success <- true
        Else opened <- opened - e
             closed <- closed + e
             ForEach state s in expand(e) do
                If (s not in opened) and (s not in closed)
                    Then opened <- opened + s
                         predecessor(s) <- e
                         g(s) <- g(e) + C(e-->s)
                    Else // s is in `opened` or in 'closed'
                        If g(s) + h(s) > g(e) + C(e-->s)
                        // i.e. f value > 'potentially new' f value
                            predecessor(s) <- e
                            If s in closed
                                Then closed <- closed - s
                                     opened <- opened + s
                EndIf EndIf EndIf
            EndForEach
    EndIf
EndWhile
If succes Then ... Else ... EndIf
```

## Links

- [A Star - Computerphile](https://www.youtube.com/watch?v=ySN5Wnu88nE)
- [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [Solvable function Logic](https://www.youtube.com/watch?v=bhmCmbj9VAg)
- [heapq - Python](https://docs.python.org/3/library/heapq.html)
- [triangle - number](https://oeis.org/A046092)
- [Linear Algo](https://algorithmsinsight.wordpress.com/graph-theory-2/a-star-in-general/implementing-a-star-to-solve-n-puzzle/)
- [Wikipedia A*](https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode)
- [Wikipedia IDA](https://en.wikipedia.org/wiki/Iterative_deepening_A*#Pseudocode)