from .abstract_prohibit_replacer import AbstractProhibitReplacer

class BaseDirPathProhibitReplacer(AbstractProhibitReplacer):
    """ ディレクトリパス用禁則文字列置換クラス
    """
    #
    # protected定数
    #
    _PROHIBIT_CHARACTERS: dict[str, str] = {
        '\\': '＼',
        '/': '／',
        ':': '：',
        '*': '＊',
        '?': '？',
        '"': '＂',
        '<': '＜',
        '>': '＞',
        '|': '｜',
    }
    _RESERVED_WORDS: dict[str, str] = {
        'CON': '_con_',
        'PRN': '_prn_',
        'AUX': '_aux_',
        'NUL': '_nul_',
        'COM1': '_com1_',
        'COM2': '_com2_',
        'COM3': '_com3_',
        'COM4': '_com4_',
        'COM5': '_com5_',
        'COM6': '_com6_',
        'COM7': '_com7_',
        'COM8': '_com8_',
        'COM9': '_com9_',
        'LPT1': '_lpt1_',
        'LPT2': '_lpt2_',
        'LPT3': '_lpt3_',
        'LPT4': '_lpt4_',
        'LPT5': '_lpt5_',
        'LPT6': '_lpt6_',
        'LPT7': '_lpt7_',
        'LPT8': '_lpt8_',
        'LPT9': '_lpt9_',
    }

    #
    # publicメソッド
    #
    def replace(self, text: str) -> str:
        """ 禁則文字と予約語を置換するメソッド
        Args:
            text (str): 置換対象文字列
        Returns:
            str: 置換後文字列
        """
        text = super().replace(text)
        text = self._replace_trailing_dots(text)
        return text
    
    #
    # protectedメソッド
    #
    def _replace_trailing_dots(self, text: str) -> str:
        """ 末尾のドットを置換するメソッド
        Args:
            text (str): 置換対象文字列
        Returns:
            str: 置換後文字列
        """
        while text.endswith('.') or text.endswith(' '):
            if text.endswith(' '):
                text = text[:-1] + '＿'
            elif text.endswith('.'):
                text = text[:-1] + '．'
        return text 