from abc import ABCMeta, abstractmethod
import pandas as pd
import argparse
import configparser

class AbstractRequirementList(metaclass=ABCMeta):
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
    def import_requirement(self, input_path: str) -> pd.DataFrame:
        """要件情報をインポートする。
        Args:
            input_path: インポート元のパス
        Returns:
            インポートした要件情報
        """
        pass

    @abstractmethod
    def export_requirement(self, output_path: str, requirement: pd.DataFrame):
        """要件情報をエクスポートする。
        Args:
            output_path: エクスポート先のパス
            requirement: エクスポートする要件情報
        """
        pass

    @abstractmethod
    def define_arguments(self, parser: argparse.ArgumentParser) -> None:
        """引数を定義する。
        Args:
            parser: 引数パーサーオブジェクト
        """
        pass

    @abstractmethod
    def parse_arguments(self, args: argparse.Namespace) -> None:
        """引数を解析する。
        Args:
            args: 引数オブジェクト
        """
        pass

    @abstractmethod
    def load_configuration(self, config_path: str) -> None:
        """設定ファイルを読み込む。
        Args:
            config_path: 設定ファイルパス
        """
        pass