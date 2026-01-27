from abc import ABC, abstractmethod
from pathlib import Path

class AbstractConverter(ABC):
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
    def execute(self, output_path: Path) -> None:
        """要件情報から各種登録用データを生成する。

        Args:
            output_path: 出力先のディレクトリパス
        """
        pass
