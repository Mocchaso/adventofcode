import time

from shortest_route_searcher import DijkstraSearcher
from common.time_util import getFormattedElapsedTimeInfo

def execute_dijkstra_search(grid_info_path_str: str, min_straight_count: int, max_straight_count: int):
    start_time = time.perf_counter()
    dijkstra_searcher = DijkstraSearcher(grid_info_path_str, min_straight_count, max_straight_count)
    total_cost = dijkstra_searcher.search()
    print(f"total_cost: {total_cost}")
    end_time = time.perf_counter()
    print()

    print(f"Process time: {getFormattedElapsedTimeInfo(start_time, end_time)}")


if __name__ == "__main__":
    GRID_EXAMPLE_TEXT_PATH = "./grid_example.txt"
    GRID_QUESTION_TEXT_PATH = "./grid_question.txt"

    # 問題1の例題
    execute_dijkstra_search(GRID_EXAMPLE_TEXT_PATH, 0, 3)
    print()
    print("====================================================================================================")
    print()

    # 問題1の問題
    execute_dijkstra_search(GRID_QUESTION_TEXT_PATH, 0, 3)
    print()
    print("====================================================================================================")
    print()

    # 問題2の例題
    execute_dijkstra_search(GRID_EXAMPLE_TEXT_PATH, 4, 10)
    print()
    print("====================================================================================================")
    print()

    # 問題2の問題
    execute_dijkstra_search(GRID_QUESTION_TEXT_PATH, 4, 10)