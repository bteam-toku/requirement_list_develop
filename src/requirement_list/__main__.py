from requirement_list.factories import Factory
from requirement_list import Config
import os
import sys
import argparse
from pathlib import Path

def main():
    """メイン処理
    """
    # argument取得
    parser = argparse.ArgumentParser()
    parser.add_argument('project_name', type=str, help='プロジェクト名')
    parser.add_argument('--input_path', type=str, default='', help='入力元のフォルダパス（デフォルトは設定ファイルのinput_path）')
    parser.add_argument('--output_path', type=str, default='', help='出力先のフォルダパス（デフォルトは設定ファイルのoutput_pathにproject_nameを結合したパス）')
    args = parser.parse_args()
    # 設定ファイル読み込み
    config = Config()

    # 引数解析
    project_name = args.project_name
    # 入力データパスの確認
    input_path = Path(args.input_path) if args.input_path else Path(config.input_path())
    if not input_path.exists():
        print(f"入力パスが存在しません: {input_path}")
        sys.exit(1)
    # 出力データパスの確認・作成
    output_path = Path(args.output_path) if args.output_path else Path(config.output_path()) / project_name
    if not output_path.exists():
        output_path.mkdir(parents=True, exist_ok=True)
    
    # Adaptorの生成
    adaptor_type_name = config.adaptor_type_name() if config.adaptor_type_name() else None
    exporter = Factory.create(project_name, adaptor_type_name)
    # 要件情報を各種登録用データに変換する
    exporter.execute(input_path, output_path)

if __name__ == "__main__":
    main()