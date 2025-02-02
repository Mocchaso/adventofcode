import sys
import time

from hand_list_parser import HandListParser
from hand_evaluator import *
from hand_ranker import *
from common.time_util import getFormattedElapsedTimeInfo


def execute(hand_list_text_path_str: str, question: int) -> None:
    start_time = time.perf_counter()

    hand_list = HandListParser.parse(hand_list_text_path_str)
    print()

    if question == 1:
        hand_evaluator = HandEvaluatorImpl()
        hand_ranker = HandRankerImpl(hand_evaluator)
    elif question == 2:
        hand_evaluator = HandEvaluatorImpl2()
        hand_ranker = HandRankerImpl2(hand_evaluator)
    else:
        print(f"Unsupported question: {question}")
        sys.exit()
    
    sorted_hand_list = hand_ranker.rank_hands(hand_list)
    total_bounty = 0
    for i, fix_hand in enumerate(sorted_hand_list):
        print(f"{i + 1} {fix_hand}: {fix_hand.bid_price} * {i + 1}")
        total_bounty += fix_hand.bid_price * (i + 1)
    
    print()
    print(f"total_bounty: {total_bounty}")

    end_time = time.perf_counter()

    print(f"Process time: {getFormattedElapsedTimeInfo(start_time, end_time)}")


if __name__ == "__main__":
    HAND_LIST_EXAMPLE_TEXT_PATH = "./hand_list_example.txt"
    HAND_LIST_QUESTION_TEXT_PATH = "./hand_list_question.txt"

    # 問題1の例題
    print("[Part 1 - example]")
    execute(HAND_LIST_EXAMPLE_TEXT_PATH, 1)
    print()
    print("====================================================================================================")
    print()

    # 問題1の問題
    print("[Part 1 - question]")
    execute(HAND_LIST_QUESTION_TEXT_PATH, 1)
    print()
    print("====================================================================================================")
    print()

    # 問題2の例題
    print("[Part 2 - example]")
    execute(HAND_LIST_EXAMPLE_TEXT_PATH, 2)
    print()
    print("====================================================================================================")
    print()

    # 問題2の問題
    print("[Part 2 - question]")
    execute(HAND_LIST_QUESTION_TEXT_PATH, 2)