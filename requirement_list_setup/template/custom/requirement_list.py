from requirement_list.abstract_requirement_list import AbstractRequirementList
from custom.dirpath_prohibit_replacer import DirPathProhibitReplacer
from custom.teams_prohibit_replacer import TeamsProhibitReplacer
from custom.redmine_prohibit_replacer import RedmineProhibitReplacer
from custom.mantis_prohibit_replacer import MantisProhibitReplacer
import pandas as pd
import os
import argparse
import configparser

class RequirementList(AbstractRequirementList):
    """要件リスト処理クラス
    """
    #
    # private変数
    #
    __project: str = ''             # 機種開発コード
    __excel_book_name: str = ''     # EXCELファイル名
    __excel_sheet_name: str = ''    # EXCELシート名
    __column_id: str = ''           # IDカラム名
    __column_title: str = ''        # 機能名カラム名

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
    def import_requirement(self, input_path: str) -> pd.DataFrame:
        """要件情報をインポートする。

        Args:
            input_path (str): インポート元のパス

        Returns:
            pd.DataFrame: インポートした要件情報
        """
        # pd.DataFrame初期化
        pd_requirement = pd.DataFrame()
        # EXCELファイルを検索
        search_bookname = self.__project + self.__excel_book_name
        for root, dirs, files in os.walk(input_path):
            # input_path以下の全ファイルをチェック
            for file in files:
                # 指定されたEXCELファイル名と一致する場合
                if file.lower() == search_bookname.lower():
                    # EXCELファイル読み込み
                    excel_path = os.path.join(root, file)
                    pd_requirement = pd.read_excel(excel_path, sheet_name=self.__excel_sheet_name, skiprows=[0], usecols=[self.__column_id, self.__column_title])
                    break
        # インポートした要件情報を返す
        return pd_requirement
        
    def export_requirement(self, output_path: str, pd_requirement: pd.DataFrame):
        """要件情報をエクスポートする。
        Args:
            output_path (str): エクスポート先のパス
            pd_requirement (pd.DataFrame): エクスポートする要件情報
        """
        # 出力先フォルダパスの作成
        output_path = os.path.join(output_path, self.__project)
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        # エクスポート処理実行
        self.__export_dirpath(output_path, pd_requirement)
        self.__export_teams(output_path, pd_requirement)
        self.__export_redmine(output_path, pd_requirement)
        self.__export_mantis(output_path, pd_requirement)

    def define_arguments(self, parser: argparse.ArgumentParser) -> None:
        """引数定義の拡張
        Args:
            parser (ArgumentParser): 引数パーサーオブジェクト
        """
        parser.add_argument('project', type=str, help='機種開発コード')
        parser.add_argument('--template', default='./input/template_folder', type=str, help='テンプレートフォルダパス(デフォルト:./input/template_folder)')  

    def parse_arguments(self, args: argparse.Namespace) -> None:
        """引数解析の拡張
        Args:
            args (Namespace): 引数オブジェクト
        """
        self.__project = args.project
        self.__excel_sheet_name = self.__project.upper()
        self.__template_folder = args.template

    def load_configuration(self, config_path: str) -> None:
        """設定ファイルを読み込む。
        Args:
            config_path (str): 設定ファイルパス
        """
        try:
            config = configparser.ConfigParser()
            config.read(config_path, encoding='utf-8')
            self.__excel_book_name = config.get('EXCEL', 'BookName')
            self.__column_id = config.get('EXCEL', 'ColumnID')
            self.__column_title = config.get('EXCEL', 'ColumnTitle')
        except Exception as e:
            print(f"設定ファイルの読み込みに失敗しました: {e}")
            raise e
    
    #
    # privateメソッド
    #
    def __export_dirpath(self, output_path: str, pd_requirement: pd.DataFrame) -> None:
        """エクスポート先のディレクトリパスを取得する。

        Args:
            output_path (str): エクスポート先のベースパス
            pd_requirement (pd.DataFrame): エクスポートする要件情報
        """
        # 置換クラスのインスタンス化
        dirpath_replacer = DirPathProhibitReplacer()

        # 要件情報の行ループ
        output_row = []
        for _, row in pd_requirement.iterrows():
            # rowのIDと機能名がNaNの場合はスキップ
            if pd.isna(row[self.__column_id]):continue
            if pd.isna(row[self.__column_title]):continue

            # folder_name生成
            folder_name = f"{str(row[self.__column_id])}_{row[self.__column_title]}"
            # 禁止文字置換
            folder_name = dirpath_replacer.replace(folder_name)
            # 出力データに追加
            output_row.append(folder_name) 
        # CSV出力
        output_filepath = os.path.join(output_path, 'directory_name.csv')
        pd.DataFrame(output_row, columns=['Directory Name']).to_csv(output_filepath, encoding='utf-8-sig', header=False, index=False)

    def __export_teams(self, output_path: str, pd_requirement: pd.DataFrame) -> None:
        """Teams用の禁止文字置換を行いエクスポートする。

        Args:
            output_path (str): エクスポート先のベースパス
            pd_requirement (pd.DataFrame): エクスポートする要件情報
        """
        # 置換クラスのインスタンス化
        teams_replacer = TeamsProhibitReplacer()

        # 要件情報の行ループ
        output_row = []
        for _, row in pd_requirement.iterrows():
            # rowのIDと機能名がNaNの場合はスキップ
            if pd.isna(row[self.__column_id]):continue
            if pd.isna(row[self.__column_title]):continue

            # TeamsName生成
            teams_name = f"{str(row[self.__column_id])}_{row[self.__column_title]}"
            # 禁止文字置換
            teams_name = teams_replacer.replace(teams_name)
            # 出力データに追加
            output_row.append(teams_name)
        # CSV出力
        output_filepath = os.path.join(output_path, 'teams_channel.csv')
        pd.DataFrame(output_row, columns=['Teams Channel Name']).to_csv(output_filepath, encoding='utf-8-sig', header=False, index=False)

    def __export_redmine(self, output_path: str, pd_requirement: pd.DataFrame) -> None:
        """Redmine用の禁止文字置換を行いエクスポートする。

        Args:
            output_path (str): エクスポート先のベースパス
            pd_requirement (pd.DataFrame): エクスポートする要件情報
        """
        # 置換クラスのインスタンス化
        redmine_replacer = RedmineProhibitReplacer()

        # 要件情報の行ループ
        output_row = []
        for _, row in pd_requirement.iterrows():
            # rowのIDと機能名がNaNの場合はスキップ
            if pd.isna(row[self.__column_id]):continue
            if pd.isna(row[self.__column_title]):continue

            # redmine_name生成
            redmine_name = f"[{str(row[self.__column_id])}][{row[self.__column_title]}]"
            # 禁止文字置換
            redmine_name = redmine_replacer.replace(redmine_name)
            # 出力データに追加
            output_row.append(redmine_name)
        # CSV出力
        output_filepath = os.path.join(output_path, 'redmine_title.csv')
        pd.DataFrame(output_row, columns=['Redmine Title']).to_csv(output_filepath, encoding='utf-8-sig', header=False, index=False)
    
    def __export_mantis(self, output_path: str, pd_requirement: pd.DataFrame) -> None:
        """Mantis用の禁止文字置換を行いエクスポートする。

        Args:
            output_path (str): エクスポート先のベースパス
            pd_requirement (pd.DataFrame): エクスポートする要件情報
        """
        # 置換クラスのインスタンス化
        mantis_replacer = MantisProhibitReplacer()

        # 要件情報の行ループ
        output_row = []
        for _, row in pd_requirement.iterrows():
            # rowのIDと機能名がNaNの場合はスキップ
            if pd.isna(row[self.__column_id]):continue
            if pd.isna(row[self.__column_title]):continue

            # mantis_name生成
            mantis_name = f"[{str(row[self.__column_id])}]{row[self.__column_title]}"
            # 禁止文字置換
            mantis_name = mantis_replacer.replace(mantis_name)
            # 出力データに追加
            output_row.append(mantis_name)
        # CSV出力
        output_filepath = os.path.join(output_path, 'mantis_category.csv')
        pd.DataFrame(output_row, columns=['Mantis Category']).to_csv(output_filepath, encoding='utf-8-sig', header=False, index=False)