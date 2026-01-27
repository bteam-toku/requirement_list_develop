# バッチ実行関数
function Invoke-Batch {
    param (
        [string]$project
    )
    # requirement_listモジュールの実行
    py -m requirement_list $project
}

# 一つ上の親ディレクトリをカレントフォルダリに設定（環境に合わせて変更してください）
Set-Location -Path (Join-Path $PSScriptRoot "..")
# 仮想環境の有効化
.\scripts\env.ps1

# 分析対象の要件リストはローカルに複製して配置してください.
# requirement_listの実行
# Invoke-Batch -project project_name
