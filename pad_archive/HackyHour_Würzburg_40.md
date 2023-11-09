# HackyHour Würzburg 40

- **When:** :warning: ~~November 28<sup>th</sup>~~ **December 12<sup>th</sup>**, 2019 at 5:00pm 
 - **Where:** [Center for Computational and Theoretical Biology (CCTB)](https://www.google.de/maps/search/cctb/@49.7850979,9.9030254,12z)
 - **Info:** [HackyHour Website](http://hackyhour.github.io/Wuerzburg/)

## Topic Suggestions
> Add your :+1: to the end of a line you are interested in
 - Say it challenge (hacker.org) [pyAudioAnalysis](https://github.com/tyiannak/pyAudioAnalysis)
 - organizing a fun coding competition (fbctf?)
 - Text Mining / Fact Extraction / Knowledge Graphs / WikiData -> [BioGrakn](https://github.com/graknlabs/biograkn) 
 - Make the computer play computer games (Reinforcement Learning, [gym](https://gym.openai.com/), [OpenSpiel](https://github.com/deepmind/open_spiel)) &rarr; continue with cart pole challenge
 - Fun variants of Chess: https://pippinbarr.github.io/chesses/
 - https://www.unixgame.io
 - Visual Explanations: http://setosa.io/ev/
 - [Bionitio](https://academic.oup.com/gigascience/article/8/9/giz109/5572530/)
 - Exploring language models: [exBERT](https://exbert.net), [talktotransformer](https://talktotransformer.com/), [AI Dungeon](http://www.aidungeon.io/)
 - Natural Language processing in Python with [NLTK](https://www.nltk.org/)
 - Practice Data Science Skills: [TidyTuesday](https://github.com/rfordatascience/tidytuesday)
 - [Git Exercises](https://gitexercises.fracz.com/)
 - Data Science GUI: [PennAI](https://epistasislab.github.io/pennai/quickstart.html)
 - [The measure of intelligence](https://github.com/fchollet/ARC)
 - Dimensionality Reduction ([PCA](http://setosa.io/ev/principal-component-analysis/), [more PCA](https://benediktehinger.de/blog/science/scatterplots-regression-lines-and-the-first-principal-component/),[t-SNE](https://distill.pub/2016/misread-tsne/),[UMAP](https://pair-code.github.io/understanding-umap/))
 - Data Visualization [data2viz](https://www.data-to-viz.com/)

### Ideas for another time
 - revisit GANs [maybe with this tutorial](https://medium.com/ai-society/gans-from-scratch-1-a-deep-introduction-with-code-in-pytorch-and-tensorflow-cb03cdcdba0f)
 - AutoML ([PennAI](https://epistasislab.github.io/pennai))
 - [Voice Cloning](https://github.com/CorentinJ/Real-Time-Voice-Cloning)


## Participants
 - Markus :pizza:
 - Matthias :sushi: :pizza:
 - Rick (probably late, ~ 6pm) :pizza: 


## Code

```python=3
import numpy as np
from scipy.io import wavfile
from pydub import AudioSegment
from pydub.playback import play

wav=wavfile.read("../sayit/text.wav")

begin = np.array([np.abs(wav[1][i*800:(i+1)*800]).sum() for i in range(60)])

# https://stackoverflow.com/a/24892274/4969760
def zero_runs(a, min_len=3):
    # Create an array that is 1 where a is 0, and pad each end with an extra 0.
    iszero = np.concatenate(([0], np.equal(a, 0).view(np.int8), [0]))
    absdiff = np.abs(np.diff(iszero))
    # Runs start and end where absdiff is 1.
    ranges = np.where(absdiff == 1)[0].reshape(-1,2)
    # Filter stretches smaller than min_len
    ranges = np.array(list(filter(lambda x: x[1]-x[0]>=min_len, ranges)))
    return ranges

np.split(wav[1][:160000], zero_runs(wav[1][:16000],min_len=100).flatten()

def play_fragment(data):
	audio_segment = AudioSegment(data.tobytes(),frame_rate=wav[0],sample_width=wav[1].dtype.itemsize,channels=1)
	play(audio_segment)

play_fragment(wav[1][:160000])

first10 = list(filter(lambda x: np.abs(x).sum()>0, np.split(wav[1][:160000], zero_runs(wav[1][:160000],min_len=100).flatten())))

first1000 = list(filter(lambda x: np.abs(x).sum()>0, np.split(wav[1][:16000000], zero_runs(wav[1][:16000000],min_len=100).flatten())))

# out of memory
# allWords = list(filter(lambda x: np.abs(x).sum()>0, np.split(wav[1], zero_runs(wav[1],min_len=100).flatten())))

# find chimera
longest = np.argmax([x.shape[0] for x in first1000])
play_fragment(first1000[longest])

# check shortest
shortest = np.argmax([x.shape[0] for x in first1000])
play_fragment(first1000[shortest])

# save for inspection in audacity
wavfile.write("chimera.wav",wav[0],first1000[longest])

```

## Cross Links
 - [previous pad](https://hackmd.io/ZVt5BmQgStyqBdvYK3wVLw)
 - [next pad](https://hackmd.io/FeEXN14sQWuIHJ9W1LrPnQ)
