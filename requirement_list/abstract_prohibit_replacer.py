from abc import ABCMeta, abstractmethod 

class AbstractProhibitReplacer(metaclass=ABCMeta):
    """ 禁則文字列置換抽象クラス
    """
    #
    # protected定数
    #
    _PROHIBIT_CHARACTERS: dict[str, str] = {}
    _RESERVED_WORDS: dict[str, str] = {}

    #
    # コンストラクタ/デストラクタ
    #
    def __init__(self):
        pass

    def __del__(self):
        pass
    
    #
    # publicメソッド
    #
    def replace(self, text: str) -> str:
        """ 禁則文字と予約語を置換する抽象メソッド
        Args:
            text (str): 置換対象文字列
        Returns:
            str: 置換後文字列
        """
        text = self._replace_prohibit_characters(text)
        text = self._replace_reserved_words(text)
        return text

    #
    # protectedメソッド
    #
    def _replace_prohibit_characters(self, text: str) -> str:
        """ 禁則文字を置換するメソッド
        Args:
            text (str): 置換対象文字列
        Returns:
            str: 置換後文字列
        """
        for prohibited, safe in self._PROHIBIT_CHARACTERS.items():
            text = text.replace(prohibited, safe)
        return text
    
    def _replace_reserved_words(self, text: str) -> str:
        """ 予約語を置換するメソッド
        Args:
            text (str): 置換対象文字列
        Returns:
            str: 置換後文字列
        """
        # 予約語を完全一致していた場合に置換する
        for reserved, safe in self._RESERVED_WORDS.items():
            if text.upper() == reserved.upper():
                text = safe
                break
        return text
