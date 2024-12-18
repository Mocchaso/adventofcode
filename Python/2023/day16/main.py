import time

from beam_simulator import RecursionSimulator, StackSimulator
from map import Direction
from common.time_util import getFormattedElapsedTimeInfo


if __name__  == "__main__":
    map_info1_path = "./map_info1.txt" # 例題
    map_info2_path = "./map_info2.txt" # 例題
    map_info3_path = "./map_info3.txt" # 問題

    
    # 問題1. 左上から右に向かってビームを発射する際に通過するタイルの枚数を計算する。
    print("- Question 1")
    print()

    # マップ1: 9が正解。（例題）
    print("* Map 1 (Example)")
    print()
    # 再帰
    print("Recursion")
    start_time = time.perf_counter()
    recursion_simulator1 = RecursionSimulator(map_info1_path)
    recursion_result1 = recursion_simulator1.simulate(0, 0, Direction.RIGHT)
    end_time = time.perf_counter()
    print(f"recursion_result1: {recursion_result1}")
    print(f"Process time: {getFormattedElapsedTimeInfo(start_time, end_time)}")
    print()
    # スタック
    print("Stack")
    start_time = time.perf_counter()
    stack_simulator1 = StackSimulator(map_info1_path)
    stack_result1 = stack_simulator1.simulate(0, 0, Direction.RIGHT)
    end_time = time.perf_counter()
    print(f"stack_result1: {stack_result1}")
    print(f"Process time: {getFormattedElapsedTimeInfo(start_time, end_time)}")
    print()

    # マップ2: 46が正解。（例題）
    print("* Map 2 (Example)")
    print()
    # 再帰
    print("Recursion")
    start_time = time.perf_counter()
    recursion_simulator2 = RecursionSimulator(map_info2_path)
    recursion_result2 = recursion_simulator2.simulate(0, 0, Direction.RIGHT)
    end_time = time.perf_counter()
    print(f"recursion_result2: {recursion_result2}")
    print(f"Process time: {getFormattedElapsedTimeInfo(start_time, end_time)}")
    print()
    # スタック
    print("Stack")
    start_time = time.perf_counter()
    stack_simulator2 = StackSimulator(map_info2_path)
    stack_result2 = stack_simulator2.simulate(0, 0, Direction.RIGHT)
    end_time = time.perf_counter()
    print(f"stack_result2: {stack_result2}")
    print(f"Process time: {getFormattedElapsedTimeInfo(start_time, end_time)}")
    print()

    # マップ3: 7562が正解。（メインの問題）
    print("* Map 3 (Main)")
    print()
    # 再帰
    print("Recursion")
    start_time = time.perf_counter()
    recursion_simulator3 = RecursionSimulator(map_info3_path)
    recursion_result3 = recursion_simulator3.simulate(0, 0, Direction.RIGHT)
    end_time = time.perf_counter()
    print(f"recursion_result3: {recursion_result3}")
    print(f"Process time: {getFormattedElapsedTimeInfo(start_time, end_time)}")
    print()
    # スタック
    print("Stack")
    start_time = time.perf_counter()
    stack_simulator3 = StackSimulator(map_info3_path)
    stack_result3 = stack_simulator3.simulate(0, 0, Direction.RIGHT)
    end_time = time.perf_counter()
    print(f"stack_result3: {stack_result3}")
    print(f"Process time: {getFormattedElapsedTimeInfo(start_time, end_time)}")
    print()
    

    # 問題2. 初期ビーム位置を変更して、最も多くのタイルを通過する際の枚数を計算する。
    print()
    print("- Question 2")
    print()

    # マップ2: 51が正解。（例題）
    print("* Map 2 (Example)")
    print()
    # 再帰
    print("Recursion")
    start_time = time.perf_counter()
    print(f"max passed tiles count (recursion): {recursion_simulator2.calculate_max_passed_tiles_count()}")
    end_time = time.perf_counter()
    print(f"Process time: {getFormattedElapsedTimeInfo(start_time, end_time)}")
    print()
    # スタック
    print("Stack")
    start_time = time.perf_counter()
    print(f"max passed tiles count (stack): {stack_simulator2.calculate_max_passed_tiles_count()}")
    end_time = time.perf_counter()
    print(f"Process time: {getFormattedElapsedTimeInfo(start_time, end_time)}")
    print()

    # マップ3: 7793が正解。（メインの問題）
    print("* Map 3 (Main)")
    print()
    # 再帰
    print("Recursion")
    start_time = time.perf_counter()
    print(f"max passed tiles count (recursion): {recursion_simulator3.calculate_max_passed_tiles_count()}")
    end_time = time.perf_counter()
    print(f"Process time: {getFormattedElapsedTimeInfo(start_time, end_time)}")
    print()
    # スタック
    print("Stack")
    start_time = time.perf_counter()
    print(f"max passed tiles count (stack): {stack_simulator3.calculate_max_passed_tiles_count()}")
    end_time = time.perf_counter()
    print(f"Process time: {getFormattedElapsedTimeInfo(start_time, end_time)}")
    print()
