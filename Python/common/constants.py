from enum import Enum


class Direction(Enum):
    """方向を表現するクラス。

    x軸: 右方向、y軸: 下方向をそれぞれ正とする。
    """
    RIGHT = (1, 0) # x+1, y
    LEFT = (-1, 0) # x-1, y
    UP = (0, -1) # x, y-1
    DOWN = (0, 1) # x, y+1

    @classmethod
    def fromName(cls, target_name: str) -> "Direction":
        """列挙子の名前から列挙子を逆引きする。
        """
        for e in Direction:
            if e.name == target_name:
                return e
        raise ValueError(f"invalid enum name: {target_name} in {cls.__name__}.")