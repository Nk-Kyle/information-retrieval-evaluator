from enum import Enum


class TFMode(Enum):
    N = 0  # Raw term frequency
    L = 1  # Log normalized
    A = 2  # Augmented
    B = 3  # Binary


class IDFMode(Enum):
    N = 0  # No idf
    T = 1  # idf


class NormMode(Enum):
    N = 0  # No normalization
    C = 1  # Cosine
