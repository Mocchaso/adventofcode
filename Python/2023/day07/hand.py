from enum import Enum


class Card(Enum):
    """カードの種類を表す列挙型。

    Attributes:
        category (str): カードの種類。
            数字のカードの名前を列挙子にそのまま使えないケースを考慮して、
            列挙子のパラメータの1個として情報を持たせる。
        strength (int): カードの強さ。値が大きいほど強い。
    """
    TWO = ("2", 1)
    THREE = ("3", 2)
    FOUR = ("4", 3)
    FIVE = ("5", 4)
    SIX = ("6", 5)
    SEVEN = ("7", 6)
    EIGHT = ("8", 7)
    NINE = ("9", 8)
    T = ("T", 9)
    JACK = ("J", 10)
    QUEEN = ("Q", 11)
    KING = ("K", 12)
    ACE = ("A", 13)

    def __init__(self, category: str, strength: int) -> None:
        """コンストラクタ。

        Args:
            category (str): カードの種類。
            strength (int): カードの強さ。値が大きいほど強い。
        """
        self.category = category
        self.strength = strength
    
    @classmethod
    def fromName(cls, target_name: str) -> "Card":
        """列挙子の名前から列挙子を逆引きする。
        """
        for e in Card:
            if e.category == target_name:
                return e
        raise ValueError(f"invalid enum name: {target_name} in {cls.__name__}.")


class HandRank(Enum):
    """手札の役を表す列挙型。

    Attributes:
        strength (int): カードの強さ。値が大きいほど強い。
    """
    HIGH_CARD = 1 # =ノーペア
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_CARD = 4
    FULL_HOUSE = 5
    FOUR_CARD = 6
    FIVE_CARD = 7

    def __init__(self, strength: int) -> None:
        """コンストラクタ。

        Args:
            strength (int): 手札の役の強さ。値が大きいほど強い。
        """
        self.strength = strength


class Hand:
    """手札のデータクラス。

    Attributes:
        cards (list[Card]): 手札。5枚分のカードで構成される。
        bid_price (int): 入札額。
        rank (HandRank): 役。実際に評価する際に初めて、値がセットされる。
    """

    def __init__(self, cards: list[Card], bid_price: int) -> None:
        """コンストラクタ。

        Args:
            cards (list[Card]): 手札。5枚分のカードで構成される。
            bid_price (int): 入札額。
        """
        self.cards = cards
        self.bid_price = bid_price
        self.rank = None
    
    def __str__(self) -> str:
        """オブジェクトの文字列表現を定義するメソッド。

        Returns:
            str: オブジェクトの文字列表現。オブジェクトをそのままprintすると出力される。
        """
        return f"{''.join([hand_card.category for hand_card in self.cards])}"