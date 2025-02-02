from abc import ABC, abstractmethod
from collections import Counter
from hand import Card, Hand, HandRank


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


class HandEvaluatorImpl2(HandEvaluator):
    """手札の役を評価するクラスの、問題2用の実装クラス。
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
        pair_count = list(matching_count_list).count(2) # 1ならワンペア、2ならツーペア
        joker_count = counter[Card.JACK]

        if max_matching_count == 5:
            return HandRank.FIVE_CARD
        elif max_matching_count == 4:
            if joker_count in (1, 4): # ex: AJAAA, JJJJA
                return HandRank.FIVE_CARD
            else: # ジョーカー無し
                return HandRank.FOUR_CARD
        elif max_matching_count == 3:
            if joker_count == 3:
                if pair_count == 1: # ex: AJJJA
                    return HandRank.FIVE_CARD
                else: # ex: AJJJK
                    return HandRank.FOUR_CARD
            elif joker_count == 2: # ex: AAJJA
                return HandRank.FIVE_CARD
            elif joker_count == 1: # ex: AAAJ7
                return HandRank.FOUR_CARD
            else: # ジョーカー無し
                if 2 in matching_count_list:
                    return HandRank.FULL_HOUSE
                else:
                    return HandRank.THREE_CARD
        elif max_matching_count == 2:
            # 要素数は最大でも3なので、list.count()を使っても大きな問題にはならない。
            has_two_pair = pair_count == 2
            if joker_count == 2:
                if has_two_pair: # ex: AJJA5
                    return HandRank.FOUR_CARD
                else: # ex: AJJ56
                    return HandRank.THREE_CARD
            elif joker_count == 1:
                if has_two_pair: # ex: AA7J7
                    return HandRank.FULL_HOUSE
                else: # ex: AA3J7
                    return HandRank.THREE_CARD
            else:
                if has_two_pair:
                    return HandRank.TWO_PAIR
                else:
                    return HandRank.ONE_PAIR
        elif max_matching_count == 1:
            if joker_count == 1: # ex: T91J6
                return HandRank.ONE_PAIR
            else:
                return HandRank.HIGH_CARD
        else:
            raise Exception(f"invalid hand. ({hand})")