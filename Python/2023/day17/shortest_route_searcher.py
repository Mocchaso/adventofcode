from abc import ABC, abstractmethod
from collections import defaultdict
import heapq

from common.constants import Direction
from grid import Grid


# 真後ろのパターン
BACK_PATTERNS = {
    Direction.RIGHT: Direction.LEFT,
    Direction.LEFT: Direction.RIGHT,
    Direction.UP: Direction.DOWN,
    Direction.DOWN: Direction.UP
}


class Searcher(ABC):
    """最短経路探索のロジックの基底クラス。

    Attributes:
        grid_obj (Grid): グリッド情報のインスタンス。
        min_straight_count (int): 一度に必ず直進しなければならない最小マス数。
        max_straight_count (int): 一度に最大で直進できるマス数。
        shortest_distances_from_start_node (dict[tuple[int, int], dict[tuple[Direction, int], int]]):
            開始ノードから各ノードへの最短距離を逐次記録する。
            進行方向や直進回数も含めて記録することで、状態を細かく区別する。
            （どの方向から来たか・連続で何マス直進してきたかによって、次以降の選択肢も変わってくる）
            探索処理後に最短経路を辿る時にも再利用する。
            { (x, y): { (direction, straight_count): cost } }
        shortest_route_record (dict[tuple[tuple[int, int], Direction, int], tuple[tuple[int, int], Direction, int]]):
            最短経路の探索結果を逐次記録するための辞書。
            探索処理後に最短経路を辿る時に利用する。
            移動経路が一意に定まるように、「移動先のノード（子） -> 移動元のノード（親）」として記録する。
            ノードの形式: ((x, y), direction, straight_count)
    """

    def __init__(self, grid_info_path_str: str, min_straight_count: int, max_straight_count: int) -> None:
        """
        Args:
            grid_info_path_str (str): グリッド情報のテキストファイルのパス。
            min_straight_count (int): 一度に必ず直進しなければならない最小マス数。
            max_straight_count (int): 一度に最大で直進できるマス数。
        """
        self.grid_obj = Grid(grid_info_path_str)
        self.min_straight_count = min_straight_count
        self.max_straight_count = max_straight_count

        self.shortest_distances_from_start_node = defaultdict(lambda: defaultdict(lambda: float('inf')))
        # 開始ノードだけ、進行方向・直進回数の全パターン分を0で初期化
        for direction in Direction:
            for straight_count in range(max(self.min_straight_count, 1), self.max_straight_count+1):
                self.shortest_distances_from_start_node[(0, 0)][(direction, straight_count)] = 0
        
        self.shortest_route_record = {}
    
    @abstractmethod
    def search(self) -> int:
        """与えられたグリッドを基に、最短経路を探索する。
        
        Returns:
            int: 最終的に消費したコストの合計値。
        """
        pass

    def _trace_shortest_route(self) -> list[tuple[int, int]]:
        """最短距離を記録したノードを、ゴールから辿る。
        経路探索処理を行なってから利用する。
        """
        goal_node = (self.grid_obj.x_size - 1, self.grid_obj.y_size - 1)
        # ゴールまで辿り着いたパターンの状態を列挙する。
        goal_state_candidates = [
            (cost, (goal_node, state[0], state[1])) # (cost, ((x, y), direction, straight_count))
            for state, cost in self.shortest_distances_from_start_node[goal_node].items()
        ]
        if not goal_state_candidates:
            # どの状態でもゴールに辿り着けなかった。
            print("No path to goal found.")
            return None
        # 最終的なコスト損失が最小であるものを選ぶ。
        best_goal_cost, best_goal_state = min(goal_state_candidates, key=lambda x: x[0])

        shortest_route = []

        current_node_state = best_goal_state
        while current_node_state:
            shortest_route.append(current_node_state[0]) # 座標情報だけで十分
            if current_node_state not in self.shortest_route_record:
                break
            current_node_state = self.shortest_route_record[current_node_state]
        
        return shortest_route[::-1]

    def _print_path_with_grid(self, path: list[tuple[int, int]]) -> None:
        """グリッド上に経路を出力する。
        """
        path_set = set(path)

        for y in range(self.grid_obj.y_size):
            line = ""
            for x in range(self.grid_obj.x_size):
                current_node = (x, y)
                if current_node in path_set:
                    line += f"[{self.grid_obj.grid[y][x]}]"
                else:
                    line += f" {self.grid_obj.grid[y][x]} "
            print(line)



class DijkstraSearcher(Searcher):
    """ダイクストラ法で探索する。
    """

    def __init__(self, grid_info_path_str: str, min_straight_count: int, max_straight_count: int) -> None:
        super().__init__(grid_info_path_str, min_straight_count, max_straight_count)
    

    def search(self):
        # (x, y)
        start_node = (0, 0)
        goal_node = (self.grid_obj.x_size - 1, self.grid_obj.y_size - 1)

        # 開始ノードから各ノードまでの最短距離（最小コスト）を管理する。
        # 優先度付きキューがDirection同士を比較できるように、Direction.nameを入れる。
        # (cost, (x, y), Direction.name, straight_count)
        priority_queue = []
        # 開始ノードから移動可能なパターン2種類
        heapq.heappush(priority_queue, (0, start_node, Direction.RIGHT.name, 0))
        heapq.heappush(priority_queue, (0, start_node, Direction.DOWN.name, 0))

        while priority_queue:
            current_cost, current_node, current_direction_name, current_straight_count = heapq.heappop(priority_queue)
            current_direction = Direction.fromName(current_direction_name)

            if current_node == goal_node and current_straight_count >= self.min_straight_count:
                final_shortest_route = self._trace_shortest_route()
                print(f"final_shortest_route:")
                print(final_shortest_route)
                print()
                self._print_path_with_grid(final_shortest_route)
                print()
                return current_cost
            
            # 計算済みの結果のコストの方が安い場合、隣のノードへの移動コストを計算しても最短経路にはならないので、スキップ。
            if current_cost > self.shortest_distances_from_start_node[current_node][(current_direction, current_straight_count)]:
                continue

            for to_next_node_direction in Direction:
                # 真後ろには行けない。
                if to_next_node_direction == BACK_PATTERNS[current_direction]:
                    continue

                # 最大回数まで既に連続で直進している場合は、進行方向に対して左右に曲がらないといけない。
                if current_straight_count == self.max_straight_count:
                    if to_next_node_direction == current_direction:
                        continue
                # 最小直進回数まで連続でまだ直進していない場合は、必ず直進しないといけない。
                if current_straight_count < self.min_straight_count:
                    if to_next_node_direction != current_direction:
                        continue
                

                dx, dy = to_next_node_direction.value
                next_node = (current_node[0] + dx, current_node[1] + dy)
                if not self.grid_obj.is_in_grid(next_node[0], next_node[1]):
                    continue
                next_node_cost = self.grid_obj.grid[next_node[1]][next_node[0]]

                next_straight_count = current_straight_count + 1 # 直進
                if to_next_node_direction != current_direction:
                    next_straight_count = 1 # 左右どちらかに曲がる（曲がりながら直進もするので1）
                
                new_cost = current_cost + next_node_cost
                if new_cost >= self.shortest_distances_from_start_node[next_node][(to_next_node_direction, next_straight_count)]:
                    continue

                # 移動にかかるコストの最小値の記録を更新。
                self.shortest_distances_from_start_node[next_node][(to_next_node_direction, next_straight_count)] = new_cost
                # 最短経路を記録する。
                self.shortest_route_record[(next_node, to_next_node_direction, next_straight_count)] = (current_node, current_direction, current_straight_count)
                heapq.heappush(
                    priority_queue,
                    (new_cost, next_node, to_next_node_direction.name, next_straight_count)
                )
        
        
        # ゴールまでの経路が見つからなかった場合
        print("No path to goal found.")
        return float("inf")