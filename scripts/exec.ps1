# バッチ実行関数
function Invoke-Batch {
    param (
        [string]$project
    )
    # requirement_listモジュールの実行
    $fullCurrentPath = Get-Location
    $fullCustomizePath = Join-Path $fullCurrentPath "customizes"
    docker run -it --rm `
        -v "$($fullCurrentPath):/data" `
        -v "$($fullCustomizePath):/app/src/requirement_list/customizes" `
        ghcr.io/bteam-toku/requirement_list:latest $project
}

# 一つ上の親ディレクトリをカレントフォルダリに設定（環境に合わせて変更してください）
Set-Location -Path (Join-Path $PSScriptRoot "..")

# 分析対象の要件リストはローカルに複製して配置してください.
# requirement_listの実行
# Invoke-Batch -project project_name
