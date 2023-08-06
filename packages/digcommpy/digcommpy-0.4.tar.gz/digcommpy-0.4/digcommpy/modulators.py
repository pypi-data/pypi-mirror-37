from abc import ABC, abstractmethod

import numpy as np

from .checks import is_binary_message


class Modulator(ABC):
    """Abstract modulator class"""
    def __init__(self, *args, **kwargs): pass

    @abstractmethod
    def modulate_symbols(self, messages): pass


class IdentityModulator(Modulator):
    @staticmethod
    def modulate_symbols(messages):
        return messages

    @staticmethod
    def demodulate_symbols(messages):
        return messages


class BpskModulator(Modulator):
    @staticmethod
    def modulate_symbols(messages):
        if not is_binary_message(messages):
            raise ValueError("Only binary messages can be modulated.")
        messages = np.array(messages)
        mod_bits = 2*messages - 1  # maps: 0 --> -1 and 1 --> 1
        return mod_bits
