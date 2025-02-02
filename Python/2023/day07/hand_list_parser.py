from pathlib import Path
from hand import Card, Hand


class HandListParser:
    """手札一覧を読み込むためのクラス。
    """

    @staticmethod
    def parse(hand_list_text_path_str: str) -> list[Hand]:
        """コンストラクタ。

        Args:
           hand_list_text_path_str (str): 手札一覧のテキストファイルのパス。 
        
        Returns:
            list[Hand]: 手札一覧をパースした結果。
        """
        hand_list = []
        with Path(hand_list_text_path_str).open(mode="r") as f:
            for line in f.readlines():
                cards, prize_money = line.split()
                hand = Hand([Card.fromName(card_str) for card_str in cards], int(prize_money))
                print(f"hand: {hand}")
                hand_list.append(hand)
        
        return hand_list


if __name__ == "__main__":
    hand_list = HandListParser.parse("./hand_list_example.txt")
    # hand_list = HandList.parse("./hand_list_question.txt")