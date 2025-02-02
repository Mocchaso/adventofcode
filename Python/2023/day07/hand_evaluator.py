from abc import ABC, abstractmethod
from collections import Counter
from hand import Hand, HandRank


class HandEvaluator(ABC):
    """手札の役を評価するクラス。
    """

    @abstractmethod
    def evaluate(self, hand: Hand) -> HandRank:
        """手札の情報から役を評価する。

        Args:
            hand (Hand): 手札。5枚分のカードで構成される。
        
        Returns:
            HandRank: 手札の役。
        """
        pass


class HandEvaluatorImpl(HandEvaluator):
    """手札の役を評価するクラスの、実装クラス。
    """

    def evaluate(self, hand: Hand) -> HandRank:
        """手札の情報から役を評価する。

        Args:
            hand (Hand): 手札。5枚分のカードで構成される。
        
        Returns:
            HandRank: 手札の役。
        """
        counter = Counter(hand.cards)
        matching_count_list = counter.values()
        max_matching_count = max(matching_count_list)

        if max_matching_count == 5:
            return HandRank.FIVE_CARD
        elif max_matching_count == 4:
            return HandRank.FOUR_CARD
        elif max_matching_count == 3:
            if 2 in matching_count_list:
                return HandRank.FULL_HOUSE
            else:
                return HandRank.THREE_CARD
        elif max_matching_count == 2:
            if list(matching_count_list).count(2) == 2:
                # 要素数は最大でも3なので、list.count()を使っても大きな問題にはならない。
                return HandRank.TWO_PAIR
            else:
                return HandRank.ONE_PAIR
        elif max_matching_count == 1:
            return HandRank.HIGH_CARD
        else:
            raise Exception(f"invalid hand. ({hand})")