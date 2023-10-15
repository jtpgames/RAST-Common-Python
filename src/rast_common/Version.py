from enum import Enum


class TrainingDataEntityVersion(Enum):
    V1 = 1
    CURRENT = 2


SELECTED_VERSION = TrainingDataEntityVersion.CURRENT
