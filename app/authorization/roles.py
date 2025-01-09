from enum import Enum

class Roles(str, Enum):
    AUTHORIZED_USER="AUTHORIZED_USER"
    ADMIN="ADMIN"
    UNAUTHORIZED_USER = "UNAUTHORIZED_USER"

    @classmethod
    def from_str(cls, s:str):
        try:
            return Roles.__members__[s]
        except:
            raise ValueError("invalid string")