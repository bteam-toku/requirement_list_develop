from abc import ABC, abstractmethod
from requirement_list.common import *
from bteam_utils.common_prohibit_replacer import AbstractProhibitReplacer
import pandas as pd
from pathlib import Path

class AbstractRequirementConverter(ABC):
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
    @abstractmethod
    def load_requirement(self, input_path: Path, params: LoadRequirementParameters) -> pd.DataFrame:
        """要件情報を読み込む。

        Args:
            input_path: 読み込み元のディレクトリパス
            params: 要件ロード用パラメータ

        Returns:
            読み込んだ要件情報
        """
        pass

    @abstractmethod
    def convert_requirement(self, requirement: pd.DataFrame, prohibit_replacer: AbstractProhibitReplacer, template: str="{id}_{title}") -> pd.DataFrame:
        """要件情報を加工してエクスポートする。

        要件情報を禁止文字置換し、名前テンプレートに基づいて名前を付与する。

        Args:
            requirement (pd.DataFrame): エクスポートする要件情報
            prohibit_replacer (AbstractProhibitReplacer): 禁止文字置換クラスのインスタンス
            template (str): エクスポート用の名前テンプレート文字列（デフォルトは"{id}_{title}"）
        
        Returns:
            エクスポートした要件情報
        """
        pass

    @abstractmethod
    def convert_requirement_match(self, mode:str, requirement: pd.DataFrame, prohibit_replacer: AbstractProhibitReplacer, template: str="{id}_{title}") -> pd.DataFrame:
        """指定した変換モードに基づいて要件情報を加工してエクスポートする。

        Args:
            mode (str): 変換モード
            requirement (pd.DataFrame): エクスポートする要件情報
            prohibit_replacer (AbstractProhibitReplacer): 禁止文字置換クラスのインスタンス
            template (str): エクスポート用の名前テンプレート文字列（デフォルトは"{id}_{title}"）
        
        Returns:
            エクスポートした要件情報
        """
        pass