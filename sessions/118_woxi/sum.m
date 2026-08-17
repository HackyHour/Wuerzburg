timing = AbsoluteTiming[Evaluate /@ {
    Apart[
        1/((x + 1) (x + 2) (x + 3) (x + 4) (x + 5)),
        x
    ],

    Together[
        Sum[1/(x + k), {k, 1, 20}]
    ],

    Apart[
        Together[Sum[1/(x + k), {k, 1, 15}]],
        x
    ]

};]
Print[timing]
