import os
import pathlib
import yaml
from typing import Any, Dict

class Config:
    """設定情報管理クラス
    """
    #
    # Constructor / Destructor
    #
    def __init__(self) -> None:
        """コンストラクタ
        """
        # ベースパスの初期化
        self._base_path = pathlib.Path(__file__).parent.parent.resolve()
        # 環境変数からDocker環境フラグの初期化
        self._is_docker = os.getenv('IS_DOCKER', 'false').lower() == 'true'
        # settings.yamlファイルパスの初期化
        if self._is_docker:
            # ローカル環境のssettings.yamlパスを優先的に使用する
            self._settings_file = pathlib.Path("/data/settings.yaml")
            if not os.path.exists(self._settings_file):
                # ローカル環境にsettings.yamlが存在しない場合はコンテナ内の設定を使用する
                self._settings_file = pathlib.Path("/app/settings.yaml")
        else:
            self._settings_file = self._base_path / "settings.yaml"
        # 設定データの読み込み
        self._config_data = self._load_settings()

    def __del__(self) -> None:
        """デストラクタ
        """
        pass

    #
    # public methods
    #
    def get(self, key: str, default=None):
        """設定値の取得

        Args:
            key (str): 設定キー
            default: デフォルト値（キーが存在しない場合に返される値）
        Returns:
            設定値またはデフォルト値
        """
        return self._config_data.get(key, default)
    
    def adaptor_type_name(self) -> str:
        """Adapterの型名の取得

        Returns:
            str: Adapterの型名
        """
        adapter_type_name = self._config_data.get("adapter_type_name", "")
        return adapter_type_name
    
    def excel_book_name(self) -> str:
        """Excelのブック名の取得
        Returns:
            str: Excelのブック名
        """
        excel_settings = self._config_data.get("excel_settings", {})
        excel_book_name = excel_settings.get("book_name", "")
        return excel_book_name
    
    def excel_column_id(self) -> str:
        """ExcelのカラムIDの取得
        Returns:
            str: ExcelのカラムID
        """
        excel_settings = self._config_data.get("excel_settings", {})
        excel_column_id = excel_settings.get("column_id", "")
        return excel_column_id

    def excel_column_title(self) -> str:
        """Excelのカラムタイトルの取得

        Returns:
            str: Excelのカラムタイトル
        """
        excel_settings = self._config_data.get("excel_settings", {})
        excel_column_title = excel_settings.get("column_title", "")
        return excel_column_title

    def input_path(self) -> str:
        """入力パスの取得
        Returns:
            str: 入力パス
        """
        path_settings = self._config_data.get("path_settings", {})
        temp_path = path_settings.get("input_path", "")
        if self._is_docker:
            return str(pathlib.Path('/data') / temp_path)
        else:
            # ローカル環境の場合はベースパスを考慮する
            return str(self._base_path / temp_path)
    
    def output_path(self) -> str:
        """出力パスの取得

        Returns:
            str: 出力パス
        """
        path_settings = self._config_data.get("path_settings", {})
        temp_path = path_settings.get("output_path", "")
        if not temp_path:
            return temp_path
        
        if self._is_docker:
            # Docker環境の場合はそのまま返す
            return str(pathlib.Path('/data') / temp_path)
        else:
            # ローカル環境の場合はベースパスを考慮する
            temp_abs_path = self._base_path / temp_path
            if not os.path.exists(temp_abs_path):
                # 絶対パスが存在しない場合は作成する
                os.makedirs(temp_abs_path, exist_ok=True)
            # 絶対パスを返す
            return str(temp_abs_path)

    #
    # protected methods
    #
    def _load_settings(self) -> Dict[str, Any]:
        """settings.yamlファイルの読み込み

        Returns:
            Dict[str, Any]: settings.yamlの内容を格納した辞書。settings.yamlが存在しない場合はデフォルト設定を返す。
        """
        # 一時的な辞書オブジェクトの作成
        temp_dict : Dict[str, Any] = {}
        # settings.yamlファイルの存在チェック
        if not os.path.exists(self._settings_file):
            # ファイルがない場合はデフォルト設定を返す
            temp_dict = {
                "adapter_type_name": "",
                "excel_settings": {
                    "book_name": "_requirement.xlsx",
                    "column_id": "id",
                    "column_title": "title",
                },
                "path_settings": {
                    "input_path": "input",
                    "output_path": "output",
                }
            }
        else:
            # settings.yamlファイルの読み込み
            with open(self._settings_file, 'r', encoding='utf-8') as f:
                temp_dict = yaml.safe_load(f)
        # 辞書オブジェクトを返す
        return temp_dict