#from fasthtml.common import fast_app, Div, P, serve

from fh_matplotlib import matplotlib2fasthtml
from fasthtml.common import *
import numpy as np
import matplotlib.pylab as plt
import skimage as ski

def generate():
	x = np.random.randint(100, 500, 2)
	y = np.random.randint(100, 700, 2)
	r = np.random.randint(50, 250, 2)
	#e = np.random.randint(0, 50, 2)
	img = np.ones((600, 800, 3), dtype=np.uint8) * 255
	rr,cc = ski.draw.disk((x[0], y[0]), r[0], shape=img.shape)
	img[rr, cc, 2] = 0
	rr,cc = ski.draw.disk((x[1], y[1]), r[1], shape=img.shape)
	img[rr, cc, 1] = 0

            
	m1 = img[:, :, 2] == 0
	m2 = img[:, :, 1] == 0
	intersect = np.logical_and(m1, m2)
	dice = 2*np.sum(intersect) / (np.sum(m1) + np.sum(m2))
	if dice == 0:
		img, dice = generate()
	return img, dice

gguess = 50
dice = 0
app, rt = fast_app()

@matplotlib2fasthtml
def generate_chart():
    # plotdata = [np.random.exponential(1) for _ in range(num_points)]
    #plt.plot(range(len(plotdata)), plotdata)
    global dice
    img, dice = generate()
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