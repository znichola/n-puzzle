# n-puzzle



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

- [x] stats prints (size of states, opened stated, closes states)
- [x] return print the subject  demands
- [ ] test system? file in result out
- [ ] resolve the extremly long solve time for an unsolvable
- [ ] differente heurisitc (manhattan, custom)
- [ ] Solvable/Unsolvable for 4x4
- [ ] Solving progress prints

### Imediate TODO

- [ ] fix input parsing (following the rules form the docs)
- [ ] testing/benchmark python script
- [ ] heuristic algo correct tiles in place
- [ ] heuristic algo correct adjacent tiles
- [ ] what is the bonus about (configure the g(x) and h(x) functions), uniform-cost and greedy searches


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
- [Wikipedia A*](https://en.wikipedia.org/wiki/A*_search_algorithm)
- [Wikipedia IDA](https://en.wikipedia.org/wiki/Iterative_deepening_A*#IDA*_on_Trees:_Slow_Threshold_Growth)