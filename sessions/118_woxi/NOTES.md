# Mathematica vs woxi vs mathics3

For most standard Algebra woxi seems to be comparable in speed to Mathematica, while mathics is far behind:

```sh
 ./bench
```

```txt
Benchmark 1: MathKernel -script symbolics.m
  Time (mean ± σ):     451.5 ms ±  20.7 ms    [User: 368.7 ms, System: 121.2 ms]
  Range (min … max):   432.0 ms … 491.8 ms    10 runs
 
Benchmark 1: woxi run symbolics.m
  Time (mean ± σ):     537.9 ms ±  20.2 ms    [User: 524.4 ms, System: 10.3 ms]
  Range (min … max):   500.4 ms … 570.5 ms    10 runs
 
Benchmark 1: mathics3 -f symbolics.m
  Time (mean ± σ):     12.683 s ±  0.265 s    [User: 12.435 s, System: 0.187 s]
  Range (min … max):   12.394 s … 13.185 s    10 runs
``` 

## Notes

- mathics does not support e.g. `Integrate[Exp[-a x], {x, 0, Infinity}, Assumptions -> a > 0]`
- woxi seems to have broader support for `DSolve` (cf. `diffeq.m`)
- woxi can directly evaluate Notebooks `woxi run notebook1.nb`
- for specific symbolic manipulations woxi is massively slower than Mathematica (cf. `sum.m`), most likely due to lacking support for some special functions.
