import marimo

__generated_with = "0.14.13"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import numpy as np
    import matplotlib.pyplot as plt
    return np, plt


@app.cell
def _(T_slider):
    # --- Simulation Parameters ---
    L = 32               # Lattice size (LxL)
    T = T_slider.value             # Temperature
    steps = 500          # Number of simulation steps
    J = 1                # Interaction strength
    k_B = 1              # Boltzmann constant
    N = L * L            # Total number of spins
    return J, L, N, T, k_B, steps


@app.cell
def _(J, L, N, T, k_B, mo, np, plt, steps):
    # --- Initialize lattice ---
    spins = np.random.choice([-1, 1], size=(L, L))

    # --- Lists to track observables ---
    magnetization_list = []
    energy_list = []
    # --- Periodic boundary conditions ---
    def get_neighbors(spins, i, j):
        return (spins[i, (j - 1) % L] + spins[i, (j + 1) % L] +
                spins[(i - 1) % L, j] + spins[(i + 1) % L, j])

    # --- Energy of entire system ---
    def total_energy(spins):
        E = 0
        for i in range(L):
            for j in range(L):
                S = spins[i, j]
                neighbors = get_neighbors(spins, i, j)
                E += -J * S * neighbors
        return E / 2  # Each pair counted twice

    # --- Metropolis update step ---
    def metropolis_step(spins, T):
        for _ in range(N):
            i = np.random.randint(0, L)
            j = np.random.randint(0, L)
            dE = 2 * J * spins[i, j] * get_neighbors(spins, i, j)
            if dE <= 0 or np.random.rand() < np.exp(-dE / (k_B * T)):
                spins[i, j] *= -1
        return spins

    # --- Plot setup ---
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    mo.mpl.interactive(fig)
    img_ax, data_ax = axs

    # Spin lattice image
    img = img_ax.imshow(spins, cmap='gray', interpolation='nearest')
    img_ax.set_title(f"2D Ising Model @ T = {T}")
    img_ax.axis('off')

    # Magnetization and energy plot
    mag_line, = data_ax.plot([], [], label='|Magnetization| per spin', color='red')
    energy_line, = data_ax.plot([], [], label='Energy per spin', color='blue')
    data_ax.set_xlim(0, steps)
    data_ax.set_ylim(-2, 2)
    data_ax.set_xlabel("Step")
    data_ax.set_ylabel("Value")
    data_ax.legend()
    data_ax.grid(True)

    # --- Animation update function ---
    def update(frame):
        global spins
        spins = metropolis_step(spins, T)

        # Current magnetization and energy per spin
        M = np.sum(spins) / N
        E = total_energy(spins) / N
        magnetization_list.append(np.abs(M))
        energy_list.append(E)

        # Print current step values
        print(f"Step {frame+1:4d}: |M|/N = {np.abs(M):.4f}, E/N = {E:.4f}")

        # Update plots
        img.set_data(spins)
        mag_line.set_data(range(len(magnetization_list)), magnetization_list)
        energy_line.set_data(range(len(energy_list)), energy_list)

        # Stop the animation after last step
        if frame == steps - 1:
            avg_mag = np.mean(magnetization_list)
            avg_energy = np.mean(energy_list)
            print("\n=== Simulation Complete ===")
            print(f"Final average |M|/N = {avg_mag:.4f}")
            print(f"Final average E/N    = {avg_energy:.4f}")

        mo.output.replace((img, mag_line, energy_line))
    return (update,)


@app.cell
def _(mo):
    T_slider = mo.ui.slider(0,10,debounce=True, show_value=True, value=5, step=0.1)
    T_slider
    return (T_slider,)


@app.cell
def _(steps, update):
    for i in range(steps):
        x = update(i)
    return


if __name__ == "__main__":
    app.run()
