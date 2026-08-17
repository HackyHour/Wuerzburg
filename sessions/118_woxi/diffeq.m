
diffEq = f'[t] == Power[t, 2] - f[t];

sol = DSolve[diffEq, f[t], t]

Print["Solutions for f[t]"]
Print[sol]
