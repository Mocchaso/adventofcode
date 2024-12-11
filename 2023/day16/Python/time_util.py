def getElapsedTime(start_time: float, end_time: float) -> float:
    """
    開始時間と終了時間から経過時間を計算する。

    Args:
        start_time (float): 開始時間。
        end_time (float): 終了時間。
    
    Returns:
        float: 経過時間。秒単位。
    """
    if start_time > end_time:
        raise Exception("start_time should be earlier than end_time.")
    return end_time - start_time

def getElapsedTimeInfo(start_time: float, end_time: float) -> tuple[int, int, float]:
    """
    経過時間を計算して、時間・分・秒の情報に分けて抽出する。

    Args:
        start_time (float): 開始時間。
        end_time (float): 終了時間。
    
    Returns:
        tuple[int, int, float]: (時間, 分, 秒)。
    """
    elapsed_time = getElapsedTime(start_time, end_time)
    return (int(elapsed_time // 3600), int((elapsed_time % 3600) // 60), elapsed_time % 60)

def getFormattedElapsedTimeInfo(start_time: float, end_time: float) -> str:
    """
    経過時間の時間・分・秒の情報を文字列としてフォーマットする。

    Args:
        start_time (float): 開始時間。
        end_time (float): 終了時間。
    
    Returns:
        str: 時間・分・秒の情報を整形した文字列。
    """
    hours, minutes, seconds = getElapsedTimeInfo(start_time, end_time)
    return f"{hours:02}h {minutes:02}m {seconds:06.3f}s"
