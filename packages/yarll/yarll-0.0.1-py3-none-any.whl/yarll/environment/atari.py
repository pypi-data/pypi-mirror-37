# -*- coding: utf8 -*-

from typing import Optional
import gym

from yarll.environment.environment import Environment

class Atari(Environment):
    """Atari environment wrapper."""

    changeable_parameters = [  # TODO: use dict instead of list of dicts
        {
            "name": "difficulty",
            "type": "choice",
            "options": []  # Depends on the environment; updated at runtime
        }
    ]

    def __init__(self, old_env_name: str, difficulty: Optional[int] = None, **kwargs) -> None:
        super(Atari, self).__init__(gym.make(old_env_name), extra_attrs={"difficulty": difficulty}, **kwargs)
        self.changeable_parameters[0]["options"] = self.unwrapped.ale.getAvailableDifficulties()
        self.unwrapped.difficulty = difficulty
        self.change_parameters(difficulty=difficulty)

    def change_parameters(self, difficulty: Optional[int] = None):
        """Change an Atari environment using a different difficulty."""
        if difficulty is not None:
            self.unwrapped.difficulty = difficulty
            self.unwrapped.ale.setDifficulty(difficulty)
