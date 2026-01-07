from custom.requirement_list import RequirementList
import os
import sys
import argparse
import configparser

def main():
    """メイン処理
    """
    # RequirementListのインスタンス化
    requirement_list = RequirementList()

    # argument取得
    parser = argparse.ArgumentParser()
    requirement_list.define_arguments(parser)
    parser.add_argument('--input_path', type=str, default='./input', help='入力元のフォルダパス. デフォルト:./input')
    parser.add_argument('--output_path', type=str, default='./output', help='出力先のフォルダパス. デフォルト:./output')
    parser.add_argument('--config', type=str, default='./inifile/config.ini', help='configファイルのパス. デフォルト:./inifile/config.ini')
    args = parser.parse_args()

    # 引数解析
    requirement_list.parse_arguments(args)
    # 入力データパスの確認
    input_path = os.path.abspath(args.input_path)
    if not os.path.exists(input_path):
        print(f"入力パスが存在しません: {input_path}")
        sys.exit(1)
    # 出力データパスの確認・作成
    output_path = os.path.abspath(args.output_path)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    # 設定ファイル読み込み
    config_path = os.path.abspath(args.config)
    if os.path.exists(config_path):
        requirement_list.load_configuration(config_path)

    # 要件情報インポート
    pd_requirement = requirement_list.import_requirement(input_path)
    # 要件情報エクスポート
    requirement_list.export_requirement(output_path, pd_requirement)

if __name__ == "__main__":
    main()