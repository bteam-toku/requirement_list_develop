from requirement_list.common import *
from requirement_list.interfaces import AbstractConverter
from requirement_list.requirement_converter import DefaultRequirementConverter
from requirement_list import Config
from bteam_utils.common_prohibit_replacer import *
from pathlib import Path

class DefaultConverterAdaptor(AbstractConverter):
    """デフォルトコンバータアダプタクラス
    """
    #
    # protected変数
    #
    _requirement_converter: DefaultRequirementConverter = None  # 要件コンバータ
    _project_name: str = None  # プロジェクト名

    #
    # コンストラクタ/デストラクタ
    #
    def __init__(self, project_name: str):
        """コンストラクタ
        Args:
            project_name (str): プロジェクト名
        """
        super().__init__()
        self._requirement_converter = DefaultRequirementConverter()
        self._project_name = project_name
    
    def __del__(self):
        super().__del__()
    
    #
    # publicメソッド
    #
    def execute(self, input_path: Path, output_path: Path) -> None:
        """要件情報から各種登録用データを生成する。

        Args:
            input_path: 入力元のディレクトリパス
            output_path: 出力先のディレクトリパス
        """
        # configインスタンスの生成
        config = Config()

        # 要件ロードパラメータの生成
        load_params = LoadRequirementParameters()
        load_params['project_name'] = self._project_name
        load_params['book_name'] = self._project_name + config.excel_book_name()
        load_params['sheet_name'] = self._project_name
        load_params['column_id'] = config.excel_column_id()
        load_params['column_title'] = config.excel_column_title()

        # 要件をロードする
        requirements = self._requirement_converter.load_requirement(input_path, load_params)

        # 要件をディレクトリ名に変換する
        path_list = self._requirement_converter.convert_requirement(
            requirements,
            PathProhibitReplacer(),
            template="{id}_{title}"
        )
        path_list.to_csv(output_path / 'directory_name.csv', header=False, index=False, encoding='utf-8-sig')

        # 要件をRedmine登録用タイトルに変換する
        redmine_list = self._requirement_converter.convert_requirement(
            requirements,
            RedmineProhibitReplacer(),
            template="[{id}][{title}]"
        )
        redmine_list.to_csv(output_path / 'redmine_title.csv', header=False, index=False, encoding='utf-8-sig')

        # 要件をTeams登録用タイトルに変換する
        teams_list = self._requirement_converter.convert_requirement(
            requirements,
            TeamsProhibitReplacer(),
            template="{id}_{title}"
        )
        teams_list.to_csv(output_path / 'teams_channel.csv', header=False, index=False, encoding='utf-8-sig')

        # 要件をMantisカテゴリ名に変換する
        mantis_list = self._requirement_converter.convert_requirement(
            requirements,
            MantisProhibitReplacer(),
            template="[{id}]{title}"
        )
        mantis_list.to_csv(output_path / 'mantis_category.csv', header=False, index=False, encoding='utf-8-sig')