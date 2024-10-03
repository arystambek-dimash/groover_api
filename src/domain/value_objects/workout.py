from enum import Enum as PyEnum


class LevelsEnum(PyEnum):
    BEGINNER = 'beginner'
    INTERMEDIATE = 'intermediate'
    IMPOSSIBLE = 'impossible'

    @classmethod
    def get_value(cls, level):
        if isinstance(level, cls):
            return level
        if isinstance(level, str):
            try:
                return cls(level.lower())
            except ValueError:
                return None
        return None
