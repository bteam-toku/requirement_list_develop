from requirement_list.base_mantis_prohibit_replacer import BaseMantisProhibitReplacer
from requirement_list.common_prohibit_replacer import CommonProhibitReplacer

class MantisProhibitReplacer(BaseMantisProhibitReplacer, CommonProhibitReplacer):
    """ Mantis用禁則文字列置換クラス
    """
    #
    # protectedメソッド
    #
    # CSV出力用にカンマを置換する
    def replace(self, text: str) -> str:
        """ 禁則文字を置換するメソッド
        Args:
            text (str): 置換対象文字列
        Returns:
            str: 置換後文字列
        """
        # 親クラスの置換処理を実行
        text = super().replace(text)
        # CSV出力用にカンマを置換
        text = self._replace_csv_splitter(text)
        # 最大長を超過している場合は切り詰める
        text = self._truncate_max_length(text, max_length=250)
        # 置換後文字列を返却
        return text
    