from .abstract_prohibit_replacer import AbstractProhibitReplacer

class BaseMantisProhibitReplacer(AbstractProhibitReplacer):
    """ Mantis用禁則文字列置換クラス
    """
    #
    # protected定数
    #
    _PROHIBIT_CHARACTERS: dict[str, str] = {
        '#': '＃',
        '$': '＄',
    }
