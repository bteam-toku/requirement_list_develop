from .abstract_prohibit_replacer import AbstractProhibitReplacer

class BaseTeamsProhibitReplacer(AbstractProhibitReplacer):
    """ Teams用禁則文字列置換クラス
    """
    #
    # protected定数
    #
    _PROHIBIT_CHARACTERS: dict[str, str] = {
        '~': '～',
        '#': '＃',
        '%': '％',
        '&': '＆',
        '*': '＊',
        ':': '：',
        '<': '＜',
        '>': '＞',
        '?': '？',
        '/': '／',
        '\\': '￥',
        '{': '｛',
        '}': '｝',
        '|': '｜',
        '\"': '＂',
    }
    _RESERVED_WORDS: dict[str, str] = {
        'General': '_general_',
        'Files': '_files_',
        'forms': '_forms_',
        'Documents': '_documents_',
        '一般': '_general_',
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
        while text.endswith('.'):
            text = text[:-1] + '．'
        return text 