#from fasthtml.common import fast_app, Div, P, serve

from fh_matplotlib import matplotlib2fasthtml
from fasthtml.common import *
import numpy as np
import matplotlib.pylab as plt
import skimage as ski

img = np.ones((600, 800, 3), dtype=np.uint8) * 255
rr,cc = ski.draw.disk((300, 400), 150, shape=img.shape)
img[rr, cc, 2] = 0
rr,cc = ski.draw.disk((350, 450), 200, shape=img.shape)
img[rr, cc, 1] = 0

m1 = img[:, :, 2] == 0
m2 = img[:, :, 1] == 0
intersect = np.logical_and(m1, m2)
dice = 2*np.sum(intersect) / (np.sum(m1) + np.sum(m2))


gguess = 50

app, rt = fast_app()

@matplotlib2fasthtml
def generate_chart():
    # plotdata = [np.random.exponential(1) for _ in range(num_points)]
    #plt.plot(range(len(plotdata)), plotdata)
    plt.imshow(img)

@app.get("/")
def homepage():
    return Div(
        Div("Fill me by clicking the button below", id="chart"),
	H3("Move the slider to change the graph"),
	Input(name="guess", type="range", min="0", max="100", value="50", get=slider_value, hx_target="#slider"),
	H3(id="slider"),
	Div(id="check_div"),
	Div(Button(
            "Check",
            # type="range",
            # min="1", max="10", value="1",
            get=check, hx_target="#check_div",
            name='button'),
	Button(
            "generate",
            # type="range",
            # min="1", max="10", value="1",
            get=update_chart, hx_target="#chart",
            name='button')),
    )

@app.get("/slider_value")
def slider_value(guess: int):
    global gguess
    gguess = guess
    return H3(f"Slider value: {guess/100}")

@app.get("/update_charts")
def update_chart():
    return Div(
        generate_chart(),
        #P(f"Dice: {dice}"),
        #P(f"You are {np.abs(dice*100 - gguess)}% off")
)

@app.get("/check")
def check():
    off = np.abs(dice.round(2)*100 - gguess)
    return Div(
        P(f"Dice: {dice.round(2)}"),
        P(f"You are {off.round(2)}% off")
)


serve()