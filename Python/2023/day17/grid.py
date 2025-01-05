from pathlib import Path


class Grid:
    """グリッドを読み込むためのクラス。

    Attributes:
        grid (list[list[int]]): グリッドのテキストデータをパースした結果。
        x_size (int): グリッド情報のx方向のマス数。
        y_size (int): グリッド情報のy方向のマス数。
    """
    def __init__(self, grid_text_path_str: str):
        """
        Args:
            grid_text_path_str (str): グリッドのテキストファイルのパス。
        """
        with Path(grid_text_path_str).open(mode="r") as f:
            grid_texts = f.read()
        self.grid = [[int(node) for node in row] for row in grid_texts.split("\n")]
        print("grid:")
        print(grid_texts)

        grid_each_row_count = set(map(len, self.grid))
        if len(grid_each_row_count) > 1:
            # グリッドの行ごとのマス数がズレていたら弾く
            raise Exception(f"grid rows is not equal. (grid_each_row_count: {grid_each_row_count})")
        
        self.x_size = len(self.grid[0])
        self.y_size = len(self.grid)
        print(f"grid size = ({self.x_size}, {self.y_size})")
        print()


    def is_in_grid(self, x: int, y: int) -> bool:
        """グリッド内の座標かどうかを判定する。
        
        Args:
            x (int): x座標。
            y (int): y座標。
        """
        # 配列の添え字なので終端はイコール無し
        return 0 <= x < self.x_size and 0 <= y < self.y_size