timing = AbsoluteTiming[Evaluate /@ {

    (* Polynomial / algebraic integrals *)
    Integrate[(x + 1)^20, x],
    Integrate[(x^2 + 3 x + 1)^10, x],
    Integrate[Expand[(x + 1)^8 (x - 2)^7], x],
    Integrate[x^12/(1 + x^2), x],
    Integrate[(x^4 + 3 x^2 + 1)/(x^2 + 1), x],
    Integrate[Sqrt[1 + x], x],
    Integrate[x Sqrt[1 + x^2], x],
    Integrate[x^3 Sqrt[1 + x^2], x],

    (* Trigonometric integrals *)
    Integrate[Sin[x]^2, x],
    Integrate[Sin[x]^4, x],
    Integrate[Sin[x]^6, x],
    Integrate[Cos[x]^8, x],
    Integrate[Sin[x]^4 Cos[x]^6, x],
    Integrate[Sin[2 x] Cos[3 x], x],
    Integrate[Sin[x] Sin[2 x] Sin[3 x], x],
    Integrate[Cos[x] Cos[2 x] Cos[3 x], x],
    Integrate[Sin[x]^2 Cos[2 x]^2, x],
    Integrate[Sin[x]/(1 + Cos[x]), x],
    Integrate[1/(1 + Sin[x]), x],
    Integrate[1/(2 + Cos[x]), x],
    Integrate[Sin[x]/(2 + Cos[x]^2), x],
    Integrate[Tan[x]^4, x],
    Integrate[Sec[x]^4, x],

    (* Exponential / logarithmic integrals *)
    Integrate[x^8 Exp[x], x],
    Integrate[x^6 Exp[2 x], x],
    Integrate[x^4 Exp[-x], x],
    Integrate[x^5 Log[x], x],
    Integrate[Log[x]^2, x],
    Integrate[x Log[x]^3, x],
    Integrate[Exp[x] Sin[x], x],
    Integrate[Exp[2 x] Cos[3 x], x],

    (* Derivatives *)
    D[(x^2 + 3 x + 1)^20, {x, 10}],
    D[Sin[x]^20, {x, 8}],
    D[Sin[x^2]^5, {x, 6}],
    D[Cos[x^3 + x]^4, {x, 5}],
    D[Exp[Sin[x]], {x, 8}],
    D[Exp[x^2] Sin[x]^3, {x, 7}],
    D[Log[1 + x^2]^5, {x, 6}],
    D[Tan[x]^8, {x, 5}],
    D[Sin[x] Cos[2 x] Exp[3 x], {x, 8}],
    D[(Sin[x] + Cos[x])^15, {x, 6}],
    D[(x^3 + Sin[x])^10, {x, 5}],
    D[Exp[Sin[x^2]], {x, 6}],

    (* Trigonometric simplification *)
    TrigExpand[Sin[10 x]],
    TrigExpand[Cos[12 x]],
    TrigExpand[Sin[x + y + z]^6],
    TrigExpand[Cos[2 x + 3 y]^8],
    TrigReduce[Sin[x]^10],
    TrigReduce[Cos[x]^12],
    TrigReduce[Sin[x]^6 Cos[x]^8],
    TrigReduce[Sin[x] Sin[2 x] Sin[3 x] Sin[4 x]],
    TrigReduce[Cos[x] Cos[2 x] Cos[3 x] Cos[4 x]],
    TrigFactor[Sin[x] + Sin[3 x] + Sin[5 x]],
    TrigFactor[Cos[x] + Cos[3 x] + Cos[5 x]],

   (* General simplification *)
    Simplify[Sin[x]^2 + Cos[x]^2],
    Simplify[Sin[x]^4 + 2 Sin[x]^2 Cos[x]^2 + Cos[x]^4],
    Simplify[(1 - Cos[2 x])/Sin[x]^2],
    Simplify[(1 + Cos[2 x])/Cos[x]^2],
    Simplify[Sin[2 x]^2 + Cos[2 x]^2],
    Simplify[Exp[Log[x]]],
    Simplify[Log[Exp[x]]],
    Simplify[(x^4 - 1)/(x^2 - 1)],
    Simplify[(x^10 - 1)/(x^5 - 1)],

    (* Expand / factor workloads *)
    Expand[(x + y + z)^12],
    Expand[(x + y)^15 (x - y)^15],
    Expand[(x^2 + x + 1)^15],
    Factor[Expand[(x + 1)^10 (x - 2)^10]],
    Factor[x^20 - 1],
    Factor[x^24 - 1],
    Factor[x^30 - 1],

    (* Rational manipulation *)
    Together[
        1/(x + 1) +
        1/(x + 2) +
        1/(x + 3) +
        1/(x + 4) +
        1/(x + 5) +
        1/(x + 6) +
        1/(x + 7) +
        1/(x + 8)
    ],

    Apart[
        1/((x + 1) (x + 2) (x + 3) (x + 4) (x + 5)),
        x
    ]

};]
Print[timing]
