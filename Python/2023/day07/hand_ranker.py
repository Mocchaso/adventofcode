from abc import ABC, abstractmethod
from hand import Hand
from hand_evaluator import HandEvaluator


class HandRanker(ABC):
    """手札間の役の強さでランク付けを行うクラス。
    """

    def __init__(self, hand_evaluator: HandEvaluator) -> None:
        """コンストラクタ。

        Args:
            hand_evaluator (HandEvaluator): 手札の役を評価するロジッククラスのオブジェクト。
        """
        self.hand_evaluator = hand_evaluator
    
    @abstractmethod
    def rank_hands(self, hands: list[Hand]) -> list[Hand]:
        """各手札間の役の強さでランク付けを行い、ソートする。
        """
        pass


class HandRankerImpl(HandRanker):
    """手札間の役の強さでランク付けを行うクラスの、実装クラス。
    """

    def rank_hands(self, hands: list[Hand]) -> list[Hand]:
        """各手札間の役の強さでランク付けを行い、ソートする。
        """
        for hand in hands:
            hand.rank = self.hand_evaluator.evaluate(hand)
        
        return sorted(hands, key=lambda hand: (hand.rank.strength, *(card.strength for card in hand.cards)))