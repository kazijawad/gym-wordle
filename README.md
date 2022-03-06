# Wordle Gym Environment

An OpenAI gym environment for Wordle.

## Usage

```{python}
import gym
import gym_wordle

env = gym.make("wordle-v0")
observation = env.reset()

for i in range(100):
    env.render()
    action = policy(observation)
    observation, reward, done, info = env.step(action)
    if done:
        observation = env.reset()

env.close()
```

## Acknowledgements

- [Wordle](https://www.nytimes.com/games/wordle/index.html)
- [Word List](https://gist.github.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b)
