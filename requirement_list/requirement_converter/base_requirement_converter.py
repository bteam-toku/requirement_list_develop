from requirement_list.interfaces import AbstractRequirementConverter
from bteam_utils.common_prohibit_replacer import AbstractProhibitReplacer
from requirement_list.common import *
import pandas as pd
from pathlib import Path

class BaseRequirementConverter(AbstractRequirementConverter):
    """要件リスト処理クラス
    """
    #
    # protected変数
    #
    _parameters: LoadRequirementParameters = {}  # 要件ロード用パラメータ

    #
    # コンストラクタ/デストラクタ
    #
    def __init__(self):
        """コンストラクタ
        """
        super().__init__()

    def __del__(self):
        """デストラクタ
        """
        super().__del__()

    #
    # publicメソッドのオーバーライド
    #
    def load_requirement(self, input_path: Path, params: LoadRequirementParameters) -> pd.DataFrame:
        """要件情報を読み込む。

        基底クラスではEXCELファイルから要件情報を読み込むメソッドを実装する。

        Args:
            input_path: 読み込み元のディレクトリパス
            params: 要件ロード用パラメータ

        Returns:
            読み込んだ要件情報
        """
        # パラメータ保存
        self._parameters = params
        # EXCELファイルを検索
        for file in input_path.rglob('*'):
            # 指定されたEXCELファイル名と一致する場合
            if file.name.lower() == params['book_name'].lower():
                # EXCELファイル読み込み
                return pd.read_excel(file, sheet_name=params['sheet_name'], skiprows=[0], usecols=[params['column_id'], params['column_title']])
        # 該当ファイルが見つからなかった場合は空のDataFrameを返す
        return pd.DataFrame()
        
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
        # 要件情報の行ループ
        output_row = []
        for _, row in requirement.iterrows():
            # rowのIDと機能名がNaNの場合はスキップ
            if pd.isna(row[self._parameters['column_id']]):continue
            if pd.isna(row[self._parameters['column_title']]):continue
            # name生成
            name = template.format(id=str(row[self._parameters['column_id']]), title=row[self._parameters['column_title']])
            # 禁止文字置換
            name = prohibit_replacer.replace(name)
            # 出力データに追加
            output_row.append(name)
        # DataFrameで復帰
        return pd.DataFrame(output_row)

    def convert_requirement_match(self, mode:str, requirement: pd.DataFrame, prohibit_replacer: AbstractProhibitReplacer, template: str="{id}_{title}") -> pd.DataFrame:
        """指定した変換モードに基づいて要件情報を加工してエクスポートする。

        基底クラスでは変換モードに関わらず通常のconvert_requirementメソッドを呼び出す。

        Args:
            mode (str): 変換モード
            requirement (pd.DataFrame): エクスポートする要件情報
            prohibit_replacer (AbstractProhibitReplacer): 禁止文字置換クラスのインスタンス
            template (str): エクスポート用の名前テンプレート文字列（デフォルトは"{id}_{title}"）
        
        Returns:
            エクスポートした要件情報
        """
        return self.convert_requirement(requirement, prohibit_replacer, template)
