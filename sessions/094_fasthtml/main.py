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

dice = 0
app, rt = fast_app()

@matplotlib2fasthtml
def generate_chart():
    global dice
    img, dice = generate()
    plt.imshow(img)

@app.get("/")
def homepage():
    return Div(
        H3("Guess the Sørensen–Dice coefficient for the two circles"),
        Div(update_chart(), id="chart"),
        Form(
            Input(name="guess", type="range", min="0", max="1", value="0.5", step="0.01", oninput="this.nextElementSibling.value = this.value", style="max-width: 800px"),
            Output(0.5, id="slider_value"), # Show slider value as text (updated via JS)
            Br(),
            Button(
                "Check",
                name='button'
            ),
            get=check,
            hx_target="#check_div"
        ),
        H3(id="slider"),
        Div(id="check_div"),
        Div(
            Button(
                "Generate new chart",
                get=update_chart, hx_target="#chart",
                name='button',
                onclick="document.getElementById('check_div').innerText = '';" # Hide previous check result
            )
        ),
    )

@app.get("/update_charts")
def update_chart():
    return Div(
        generate_chart(),
    )

@app.get("/check")
def check(guess: float):
    off = np.abs(dice.round(2) - guess)
    return Div(
        P(f"Dice: {dice.round(2)}"),
        P(f"You are {off.round(2)} off")
    )

serve()