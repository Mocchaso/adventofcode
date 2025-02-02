from hand_list_parser import HandListParser
from hand_evaluator import *
from hand_ranker import *


if __name__ == "__main__":
    hand_list = HandListParser.parse("./hand_list_example.txt")
    # hand_list = HandListParser.parse("./hand_list_question.txt")
    print()

    hand_evaluator = HandEvaluatorImpl()
    hand_ranker = HandRankerImpl(hand_evaluator)

    sorted_hand_list = hand_ranker.rank_hands(hand_list)
    total_bounty = 0
    for i, fix_hand in enumerate(sorted_hand_list):
        print(f"{i + 1} {fix_hand}: {fix_hand.bid_price} * {i + 1}")
        total_bounty += fix_hand.bid_price * (i + 1)
    
    print()
    print(f"total_bounty: {total_bounty}")