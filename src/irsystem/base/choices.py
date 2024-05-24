from dataclasses import dataclass
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


@dataclass
class WeightingTriplet:
    """
    A triplet representing term weighting method.
    """

    tf: TFMode
    """
    The term frequency valuation method.
    """
    idf: IDFMode
    """
    Represents whether the weighting method should use idf or not.
    """
    norm: NormMode
    """
    The normalization method.
    """

    @staticmethod
    def from_str(repr: str) -> "WeightingTriplet":
        """
        Converts a 3-characters string into `WeightingTriplet`.

        Args:
            `repr`: 3-characters string representing weighting method

        Returns:
            A `WeightingTriplet` corresponding the weighting method. 
        """
        if len(repr) != 3:
            raise Exception(
                "Term weighting triplet must be a 3-characters string.")

        repr = repr.lower()
        triplet = WeightingTriplet(
            TFMode.N,
            IDFMode.N,
            NormMode.N,
        )

        match repr[0]:
            case "n":
                triplet.tf = TFMode.N
            case "l":
                triplet.tf = TFMode.L
            case "a":
                triplet.tf = TFMode.A
            case "b":
                triplet.tf = TFMode.B
            case _:
                raise Exception(f"Invalid value for tf mode: {repr[0]}")

        match repr[1]:
            case "n":
                triplet.idf = IDFMode.N
            case "t":
                triplet.idf = IDFMode.T
            case _:
                raise Exception(f"Invalid value for idf mode: {repr[1]}")

        match repr[2]:
            case "n":
                triplet.norm = NormMode.N
            case "c":
                triplet.norm = NormMode.C
            case _:
                raise Exception(f"Invalid value for norm mode: {repr[2]}")

        return triplet
