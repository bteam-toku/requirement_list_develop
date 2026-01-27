from typing import TypedDict
from datetime import datetime
from bteam_utils import CommonCalendar

class LoadRequirementParameters(TypedDict):
    """要件ロード用パラメータ
    """
    project_name: str       # プロジェクト名
    book_name: str          # EXCELファイル名
    sheet_name: str         # EXCELシート名
    column_id: str          # IDカラム名
    column_title: str       # 機能名カラム名
