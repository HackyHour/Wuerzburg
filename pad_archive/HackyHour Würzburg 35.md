# HackyHour Würzburg 35
 - **When:** May 23<sup>rd</sup>, 2019 at 5:00pm 
 - **Where:** [Center for Computational and Theoretical Biology (CCTB)](https://www.google.de/maps/search/cctb/@49.7850979,9.9030254,12z)
 - **Info:** [HackyHour Website](http://hackyhour.github.io/Wuerzburg/)

## Topic Suggestions
> Add your :+1: to the end of a line you are interested in
 - Say it challenge (hacker.org)
 - organizing a fun coding competition (fbctf?)
 - Make the computer play computer games (Reinforcement Learning, [gym](https://gym.openai.com/))
 - Text Mining / Fact Extraction / Knowledge Graphs / WikiData
 - Proteomics
 - natural language processing
 
### Ideas for another time
 - revisit GANs [maybe with this tutorial](https://medium.com/ai-society/gans-from-scratch-1-a-deep-introduction-with-code-in-pytorch-and-tensorflow-cb03cdcdba0f)
 - Quantum computing ([for the very curious](https://quantum.country/qcvc))
 - AutoML ([PennAI](https://epistasislab.github.io/pennai))
 - [GNU Guix](https://www.gnu.org/software/guix/)


## Participants
- Markus :pizza: 
- Matthias :sushi:
- Franzi :sunflower: :sushi:
- Michaela


## Cross Links
 - [previous pad](https://hackmd.io/UJRSGr6xS0SCEeYnFinYtg)
 - [next pad](https://hackmd.io/BujOxGFrSGec2xA2Izp2oQ)

## Manual solution
```
import gym
env = gym.make('CartPole-v0')
for i_episode in range(20):
    observation = env.reset()
    last_wiggle = 0
    for t in range(1000):

        env.render()
        #print(observation)
        if observation[2] > 0.1:
            action = 1
            last_wiggle = 1
        elif observation[2] < -0.1:
            action = 0
            last_wiggle = 0
        else:
            last_wiggle = 1 - last_wiggle
            action = last_wiggle

        observation, reward, done, info = env.step(action)
        if done:
            print("Episode finished after {} timesteps".format(t+1))

            break
env.close()
```
## Link to the DQN approach I found
[Cartpole - Introduction to Reinforcement Learning (DQN - Deep Q-Learning)](https://towardsdatascience.com/cartpole-introduction-to-reinforcement-learning-ed0eb5b58288)