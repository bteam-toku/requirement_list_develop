# バッチ実行関数
function Invoke-Batch {
    param (
        # /your-project-base-path/your-project-path-name/youer-requirement-list-folder
        # /your-project-base-path/your-project-path-name/your-document-folder
        # [string]$basePath = "\\omdc-fs01\z_d_firm\_aランク",
        # [string]$projectPathName,
        # [string]$requirementListFolder = "30_システム要求定義",
        # [string]$documentFolder = "70_プロジェクト工程",
        [string]$project
    )
    
    # Set-Location -Path $PSScriptRoot
    Write-Host "$project Start"

    #
    # 必要に応じて以下のコードを有効化してください
    #
    # # projectPathの設定と確認
    # $projectPath = Join-Path -Path $basePath -ChildPath $projectPathName
    # if (-Not (Test-Path -Path $projectPath)) {
    #     Write-Host "Project path not found: $projectPath"
    #     return
    # }
    # # .\inputにporoject名のフォルダを作成し要求定義書をコピー
    # $inputPath = Join-Path -Path $PSScriptRoot -ChildPath "input\$project"
    # if (-Not (Test-Path -Path $inputPath)) {
    #     New-Item -ItemType Directory -Path $inputPath | Out-Null
    # }
    # $requirementPath = Join-Path -Path $projectPath -ChildPath $requirementListFolder
    # copy-Item -Path $requirementPath\*.xlsx -Destination $inputPath -Recurse -Force

    # requirement_listモジュールの実行
    $current = (Get-Location).Path.Replace('\', '/')
    docker run -it --rm `
        -v "${current}/custom:/app/custom" `
        -v "${current}/output:/app/output" `
        -v "${current}/input:/app/input" `
        -v "${current}/inifile:/app/inifile" `
        requirement_list requirement_list $project

    #
    # 必要に応じて以下のコードを有効化してください
    #
    # # .\outputにproject名のdirectory_copy.batを実行してドキュメントをコピー
    # $batSourcePath = Join-Path -Path $PSScriptRoot -ChildPath "output\$project\directory_copy.bat"
    # if (Test-Path -Path $batSourcePath) {
    #     $documentPath = Join-Path -Path $projectPath -ChildPath $documentFolder
    #     Start-Process -FilePath "cmd.exe" -ArgumentList "/c `"$batSourcePath`" `"$documentPath`"" -NoNewWindow -Wait
    # } else {
    #     Write-Host "directory_copy.bat not found in $outputPath"
    # }

    Write-Host "$project Completed"
}
function Invoke-Setup-Batch {
    Set-Location -Path $PSScriptRoot
    Write-Host "requirement_list_setup Start"
    $current = (Get-Location).Path.Replace('\', '/')
    docker run -it --rm `
        -v "${current}/custom:/app/custom" `
        -v "${current}/inifile:/app/inifile" `
        -v "${current}/input:/app/input" `
        requirement_list requirement_list_setup
    Write-Host "requirement_list_setup Completed"
}

# # requirement_list_setupの実行
# Invoke-Setup-Batch

# # requirement_listの実行
# Invoke-Batch -project "your-project-name"

# requirement_listの実行
# Invoke-Batch -project "your-project-name" -projectPathName "your-project-path-name"