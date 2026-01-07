from .abstract_prohibit_replacer import AbstractProhibitReplacer

class BaseRedmineProhibitReplacer(AbstractProhibitReplacer):
    """ Redmine用禁則文字列置換クラス
    """
    #
    # protected定数
    #
    _PROHIBIT_CHARACTERS: dict[str, str] = {
        '#': '＃',
    }
