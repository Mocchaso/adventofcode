from abc import ABC, abstractmethod
from functools import lru_cache

from map import Map, MapElement, Direction


class Simulator(ABC):
    """ビームをマップへ発射する処理をシミュレートするためのクラス。
    入力されたマップに対してビームを放ち、通過したタイルを数える。
    ※ビームは他のビームとぶつかっても相互作用しない
    ※タイルは同時に複数のビームを通過可能

    Attributes:
        map_obj (Map): マップ情報のインスタンス。
    """

    def __init__(self, map_info_path_str: str) -> None:
        """
        Args:
            map_info_path_str (str): マップ情報のテキストファイルのパス。
        """
        self.map_obj = Map(map_info_path_str)
    
    @abstractmethod
    def simulate(self, orig_x: int, orig_y: int, orig_direction: Direction) -> int:
        """ビームの発射・移動を再帰的にシミュレートする。
        ビームが通過したタイルの情報はMapインスタンスへ逐一記録される。

        Args:
            orig_x (int): 初期位置のx座標。
            orig_y (int): 初期位置のy座標。
            orig_direction (Direction): 初期位置から照射するビームの方向。
        
        Returns:
            int: 最終的に通過したタイルの枚数。
        """
        pass

    def calculate_max_passed_tiles_count(self):
        """
        初期ビーム位置を変更して、最も多くのタイルを通過する際の枚数を計算する。
        """
        self.map_obj.passed_tiles.clear()
        
        passed_tiles_results = {}
        for (x, y, direction) in self.map_obj.shotting_beam_patterns:
            passed_tiles_results[(x, y, direction)] = self.simulate(x, y, direction)
            # 次のパターンのシミュレーションを行う前に、履歴をリセット
            self.map_obj.passed_tiles.clear()
        
        return max(passed_tiles_results.values())


class RecursionSimulator(Simulator):
    """
    再帰を用いてシミュレートする。

    Attributes:
        map_obj (Map): マップ情報のインスタンス。
    """

    def __init__(self, map_info_path_str: str) -> None:
        """
        Args:
            map_info_path_str (str): マップ情報のテキストファイルのパス。
        """
        super().__init__(map_info_path_str)

    def simulate(self, orig_x: int, orig_y: int, orig_direction: Direction) -> int:
        # マップの範囲外に出たら再帰終了
        if not self.map_obj.is_in_map(orig_x, orig_y):
            return 0
        
        # 同じタイルを同じ向きから通過しようとする場合は、ループと見なして再帰終了
        if self.map_obj.has_already_passed(orig_x, orig_y, orig_direction):
            return 0
        
        # 現在のタイルを通過
        self.map_obj.mark_passed_tiles(orig_x, orig_y, orig_direction)

        # ビームを進める
        current_tile = self.map_obj.get_tile(orig_x, orig_y)
        # （確認用）
        # print(f"current_title: 「{current_tile.value}」({current_tile}), (x, y) = ({orig_x}, {orig_y}), direction: {orig_direction}, passed_tiles: {self.map_obj.passed_tiles}")
        match current_tile:
            case MapElement.EMPTY:
                # そのまま通過
                dx, dy = orig_direction.value
                self.simulate(orig_x + dx, orig_y + dy, orig_direction)
            case MapElement.MIRROR1:
                # 反射しながら通過
                reflected_direction = Direction.reflect_beam(MapElement.MIRROR1, orig_direction)
                dx, dy = reflected_direction.value
                self.simulate(orig_x + dx, orig_y + dy, reflected_direction)
            case MapElement.MIRROR2:
                # 反射しながら通過
                reflected_direction = Direction.reflect_beam(MapElement.MIRROR2, orig_direction)
                dx, dy = reflected_direction.value
                self.simulate(orig_x + dx, orig_y + dy, reflected_direction)
            case MapElement.SPLITTER1:
                if orig_direction in (Direction.DOWN, Direction.UP):
                    # 左右に分割
                    self.simulate(orig_x - 1, orig_y, Direction.LEFT)
                    self.simulate(orig_x + 1, orig_y, Direction.RIGHT)
                else:
                    # そのまま通過
                    dx, dy = orig_direction.value
                    self.simulate(orig_x + dx, orig_y + dy, orig_direction)
            case MapElement.SPLITTER2:
                if orig_direction in (Direction.RIGHT, Direction.LEFT):
                    # 上下に分割
                    self.simulate(orig_x, orig_y - 1, Direction.UP)
                    self.simulate(orig_x, orig_y + 1, Direction.DOWN)
                else:
                    # そのまま通過
                    dx, dy = orig_direction.value
                    self.simulate(orig_x + dx, orig_y + dy, orig_direction)
            
        return self.map_obj.count_passed_tiles()


class StackSimulator(Simulator):
    """スタックを用いてシミュレートする。

    Attributes:
        map_obj (Map): マップ情報のインスタンス。
    """

    def __init__(self, map_info_path_str: str) -> None:
        """
        Args:
            map_info_path_str (str): マップ情報のテキストファイルのパス。
        """
        super().__init__(map_info_path_str)

    def simulate(self, orig_x: int, orig_y: int, orig_direction: Direction) -> int:
        stack = [(orig_x, orig_y, orig_direction)]
        while stack:
            x, y, direction = stack.pop()

            # マップの範囲外はスキップ
            if not self.map_obj.is_in_map(x, y):
                continue
            
            # 同じタイルを同じ向きから通過しようとする場合は、ループと見なしてスキップ
            if self.map_obj.has_already_passed(x, y, direction):
                continue

            # 現在のタイルを通過
            self.map_obj.mark_passed_tiles(x, y, direction)

            # ビームを進める
            current_tile = self.map_obj.get_tile(x, y)
            # （確認用）
            # print(f"current_title: 「{current_tile.value}」({current_tile}), (x, y) = ({x}, {y}), direction: {direction}, passed_tiles: {self.map_obj.passed_tiles}")
            match current_tile:
                case MapElement.EMPTY:
                    # そのまま通過
                    dx, dy = direction.value
                    stack.append((x + dx, y + dy, direction))
                case MapElement.MIRROR1:
                    # 反射しながら通過
                    reflected_direction = Direction.reflect_beam(MapElement.MIRROR1, direction)
                    dx, dy = reflected_direction.value
                    stack.append((x + dx, y + dy, reflected_direction))
                case MapElement.MIRROR2:
                    # 反射しながら通過
                    reflected_direction = Direction.reflect_beam(MapElement.MIRROR2, direction)
                    dx, dy = reflected_direction.value
                    stack.append((x + dx, y + dy, reflected_direction))
                case MapElement.SPLITTER1:
                    if direction in (Direction.DOWN, Direction.UP):
                        # 左右に分割
                        stack.append((x - 1, y, Direction.LEFT))
                        stack.append((x + 1, y, Direction.RIGHT))
                    else:
                        # そのまま通過
                        dx, dy = direction.value
                        stack.append((x + dx, y + dy, direction))
                case MapElement.SPLITTER2:
                    if direction in (Direction.RIGHT, Direction.LEFT):
                        # 上下に分割
                        stack.append((x, y - 1, Direction.UP))
                        stack.append((x, y + 1, Direction.DOWN))
                    else:
                        # そのまま通過
                        dx, dy = direction.value
                        stack.append((x + dx, y + dy, direction))
        
        return self.map_obj.count_passed_tiles()
