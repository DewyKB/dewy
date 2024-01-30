from enum import Enum


class DistanceMetric(str, Enum):
    COSINE = "cosine"
    IP = "ip"
    L2 = "l2"

    def __str__(self) -> str:
        return str(self.value)
