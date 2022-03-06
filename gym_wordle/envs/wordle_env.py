import os
import random
import pkg_resources

import numpy as np
import gym
from gym import error, spaces, utils
from gym.utils import seeding
from colorama import Fore, Style


NUM_ALPHABET = 26
NUM_WORDS = 6
NUM_CHARS = 5
WORD_LIST = []


with open(pkg_resources.resource_filename("gym_wordle", "data/words.txt")) as f:
    lines = f.readlines()
    for line in lines:
        word = line.strip()
        word = word.lower()
        assert len(word) == 5, "Invalid Word"
        WORD_LIST.append(tuple(ord(char) - 97 for char in word))


class WordleEnv(gym.Env):
    metdata = {"render.modes": ["human"]}

    def __init__(self):
        super(WordleEnv, self).__init__()
        self.observation_space = spaces.Dict({
            "alphabet": spaces.Box(low=1, high=2, shape=(NUM_ALPHABET,), dtype=int),
            "board": spaces.Box(low=1, high=2, shape=(NUM_WORDS, NUM_CHARS), dtype=int)
        })
        self.action_space = spaces.MultiDiscrete([NUM_ALPHABET] * NUM_CHARS)
        self.guesses = []

    @property
    def observation(self):
        return {"board": self.board, "alphabet": self.alphabet}

    def step(self, action):
        assert self.action_space.contains(action), "Invalid Action"

        for i, char in enumerate(action):
            if self.word[i] == char:
                encoding = 2
            elif char in self.word:
                encoding = 1
            else:
                encoding = 0
            self.board[self.row, i] = encoding
            self.alphabet[char] = encoding

        if all(self.board[self.row, :] == 2):
            reward = 1.0
            done = True
        else:
            if self.row < NUM_WORDS - 1:
                reward = 0.0
                done = False
            else:
                reward = -1.0
                done = True

        self.guesses.append(action)
        self.row += 1

        return self.observation, reward, done, {}

    def reset(self):
        self.row = 0
        self.guesses = []
        self.word = random.choice(WORD_LIST)
        self.board = np.negative(np.ones(shape=(NUM_WORDS, NUM_CHARS), dtype=int))
        self.alphabet = np.negative(np.ones(shape=(NUM_ALPHABET,), dtype=int))
        return self.observation

    def render(self, mode="human"):
        os.system("cls" if os.name == 'nt' else "clear")
        print("+" + "-" * NUM_CHARS + "+")
        for i in range(NUM_WORDS):
            print("+", end="")
            for j in range(NUM_CHARS):
                if any(self.board[i] > -1):
                    value = self.board[i][j]
                    char = chr(ord("a") + self.guesses[i][j])
                    if value == 0:
                        print(Fore.BLACK, end="")
                    elif value == 1:
                        print(Fore.YELLOW, end="")
                    elif value == 2:
                        print(Fore.GREEN, end="")
                    print(char, end="")
                    print(Style.RESET_ALL, end="")
                else:
                    print(" ", end="")
            print("+")
        print("+" + "-" * NUM_CHARS + "+")
