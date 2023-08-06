from abc import ABC, abstractmethod

import numpy as np

from .checks import is_binary_message


class Demodulator(ABC):
    """Abstract modulator class"""
    def __init__(self, *args, **kwargs): pass

    @abstractmethod
    def demodulate_symbols(self, messages): pass


class IdentityDemodulator(Demodulator):
    @staticmethod
    def demodulate_symbols(messages):
        messages = np.array(messages)
        return messages


class BpskDemodulator(Demodulator):
    @staticmethod
    def demodulate_symbols(messages):
        messages = np.array(messages)
        idx = messages > 0
        messages[idx] = 1
        messages[~idx] = 0
        return messages
