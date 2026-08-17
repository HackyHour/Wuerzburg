tests = Hold /@ {
    Integrate[x^3 + 2 x^2 - 5 x + 7, x],
    Integrate[x^(1/2), x],
    Integrate[1/x, x],
    Integrate[Exp[2 x], x],
    Integrate[Sin[3 x], x],
    Integrate[Cos[x], x],
    Integrate[1/(1 + x^2), x],
    Integrate[x Exp[x], x],
    Integrate[Exp[-x^2], {x, -Infinity, Infinity}],
    Integrate[x^2, {x, 0, 1}],
    Integrate[Sin[x], {x, 0, Pi}],
    Integrate[(x^2 + 1)/(x + 1), x],
    Integrate[Log[x], x],
    Integrate[1/Sqrt[1 - x^2], x],
    Integrate[Sin[x]^2, x],
    Integrate[x^2 Exp[x], x]
};

Print /@ Map[
    Function[test,
        With[{timed = AbsoluteTiming[ReleaseHold[test]]},
            "Time: " <> ToString[timed[[1]]] <>
            " s | Result: " <> ToString[timed[[2]], InputForm]
        ]
    ],
    tests
];
