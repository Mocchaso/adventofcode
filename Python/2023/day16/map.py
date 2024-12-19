from enum import Enum
from pathlib import Path


class MapElement(Enum):
    """マップ情報の要素を表現する列挙型。
    """
    EMPTY = "." # 空きスペース、ビームは同じ方向に進む
    MIRROR1 = "/" # ミラー、ビームは角度に応じて90度反射される
    MIRROR2 = "\\" # ミラー、ビームは角度に応じて90度反射される
    SPLITTER1 = "-" # スプリッター：平らな側面にビームが遭遇した場合、尖端が指している2つの方向に分割する
    SPLITTER2 = "|" # スプリッター：尖端にビームが遭遇した場合、空きスペースであるかのように通過する

    @classmethod
    def value_of(cls, target_value: str):
        for e in MapElement:
            if e.value == target_value:
                return e
        raise ValueError(f"invalid value: {target_value} in {cls.__name__}.")


class Direction(Enum):
    """ビームの方向を表現するクラス。

    x軸: 右方向、y軸: 下方向をそれぞれ正とする。
    """
    RIGHT = (1, 0) # x+1, y
    LEFT = (-1, 0) # x-1, y
    UP = (0, -1) # x, y-1
    DOWN = (0, 1) # x, y+1

    @classmethod
    def reflect_beam(cls, mirror_type: MapElement, current_direction: "Direction"):
        """ビームが反射される際に方向転換させる。
        反射後の向きは、ビーム視点ではなく、常にマップを正面から見た時の向きとして転換させるものとする。

        Args:
            mirror_type (MapElement): ミラーの種類。これによって反射の仕方が変わってくる。
            current_direction (Direction): 現在のビームの方向。
        """
        match current_direction:
            case Direction.RIGHT: # 右方向へ照射された時
                match mirror_type:
                    case MapElement.MIRROR1:
                        return Direction.UP
                    case MapElement.MIRROR2:
                        return Direction.DOWN
            case Direction.LEFT: # 左方向へ照射された時
                match mirror_type:
                    case MapElement.MIRROR1:
                        return Direction.DOWN
                    case MapElement.MIRROR2:
                        return Direction.UP
            case Direction.UP: # 上方向へ照射された時
                match mirror_type:
                    case MapElement.MIRROR1:
                        return Direction.RIGHT
                    case MapElement.MIRROR2:
                        return Direction.LEFT
            case Direction.DOWN: # 下方向へ照射された時
                match mirror_type:
                    case MapElement.MIRROR1:
                        return Direction.LEFT
                    case MapElement.MIRROR2:
                        return Direction.RIGHT


class Map:
    """マップの情報保持や操作のロジックをまとめたクラス。

    Attributes:
        grid (list[list[str]]): マップ情報を盤面としてリスト化したもの。
        x_size (int): マップ情報のx方向のマス数。
        y_size (int): マップ情報のy方向のマス数。
        shotting_beam_patterns (list[tuple(int, int, Direction)]): マップ情報を基に、初期ビーム位置・方向のパターンを列挙するためのリスト。
        passed_tiles (list[tuple(int, int, Direction)]): ビームが通過したタイル。(x座標, y座標, どの向きから入ってきたか)
    """
    def __init__(self, map_info_path_str: str):
        """
        Args:
            map_info_path_str (str): マップ情報のテキストファイルのパス。
        """
        with Path(map_info_path_str).open(mode="r") as f:
            map_info = f.read()
        self.grid = map_info.split("\n")
        print("map:")
        print(map_info)

        map_each_row_count = set(map(len, self.grid))
        if len(map_each_row_count) > 1:
            # マップの行ごとのマス数がズレていたら弾く
            raise Exception(f"map rows is not equal. (map_each_row_count: {map_each_row_count})")
        
        self.x_size = len(self.grid[0])
        self.y_size = len(self.grid)
        print(f"map size = ({self.x_size}, {self.y_size})")

        self.shotting_beam_patterns = []
        # ビームを発射できる全パターンを記録しておく。
        # ※四辺以外はマップの内部となるため発射不可。
        for x in range(self.x_size):
            # 最上段の辺
            self.shotting_beam_patterns.append((x, 0, Direction.DOWN))
            # 最下段の辺
            self.shotting_beam_patterns.append((x, self.y_size - 1, Direction.UP))
        for y in range(self.y_size):
            # 最左列の辺
            self.shotting_beam_patterns.append((0, y, Direction.RIGHT))
            # 最右列の辺
            self.shotting_beam_patterns.append((self.x_size - 1, y, Direction.LEFT))

        self.passed_tiles = []
    
    def is_in_map(self, x: int, y: int) -> bool:
        """マップ内の座標かどうかを判定する。
        
        Args:
            x (int): x座標。
            y (int): y座標。
        """
        # 配列の添え字なので終端はイコール無し
        return 0 <= x < self.x_size and 0 <= y < self.y_size
    
    def get_tile(self, x: int, y: int) -> MapElement:
        """指定した座標のタイルの情報を取得する。

        Args:
            x (int): x座標。
            y (int): y座標。
        """
        if self.is_in_map(x, y):
            return MapElement.value_of(self.grid[y][x])
        return None # マップの範囲外
    
    def mark_passed_tiles(self, x: int, y: int, direction: Direction) -> None:
        """指定した座標・方向の情報を基に、通過済みのタイル一覧へマーキングする。

        Args:
            x (int): x座標。
            y (int): y座標。
            direction (Direction): 指定した位置のタイルへビームが入ってきた方向。
        """
        self.passed_tiles.append((x, y, direction))
    
    def has_already_passed(self, x: int, y: int, direction: Direction) -> bool:
        """指定した座標のタイルに、指定した方向から既に通過済みかどうかをチェックする。
        （無限ループ対策）
        
        Args:
            x (int): x座標。
            y (int): y座標。
            direction (Direction): 指定した位置のタイルへビームが入ってきた方向。
        """
        return (x, y, direction) in self.passed_tiles
    
    def count_passed_tiles(self) -> int:
        """通過済みのタイル数をカウントする。
        同じタイルを違う方向から複数回通過するケースで
        重複してカウントされないように、ビームが通過した方向は無視する。
        """
        # setにすることで、座標情報の重複を除去する。
        return len({(tile[0], tile[1]) for tile in self.passed_tiles})
