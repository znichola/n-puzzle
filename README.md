# n-puzzle


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
        Then success < true
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