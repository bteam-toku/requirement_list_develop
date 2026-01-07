class CommonProhibitReplacer:
    """ 共通禁則文字列置換クラス
    """
    # コンストラクタ/デストラクタ
    def __init__(self):
        pass

    def __del__(self):
        pass

    #
    # protectedメソッド
    #
    def _replace_csv_splitter(self, text: str) -> str:
        """ CSV区切り文字を置換するメソッド
        Args:
            text (str): 置換対象文字列
        Returns:
            str: 置換後文字列
        """
        text = text.replace(',', '，')
        return text

    
    def _truncate_max_length(self, text: str, max_length: int) -> str:
        """ 最大長を超過した場合に切り詰めるメソッド
        Args:
            text (str): 置換対象文字列
            max_length (int): 最大長
        Returns:
            str: 置換後文字列
        """
        if len(text) > max_length:
            text = text[:max_length]
        return text