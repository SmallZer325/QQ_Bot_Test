# QQ机器人重启脚本
# 使用方法：在PowerShell中运行 .\restart_bot.ps1

Write-Host "正在停止机器人..." -ForegroundColor Yellow

# 停止所有运行bot.py的Python进程
$processes = Get-Process python -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*bot.py*" -or $_.Path -like "*bot.py*"
}

if ($processes) {
    foreach ($proc in $processes) {
        Write-Host "停止进程 PID: $($proc.Id)" -ForegroundColor Yellow
        Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue
    }
    Start-Sleep -Seconds 2
} else {
    # 如果没有找到特定进程，尝试停止所有python进程（谨慎使用）
    Write-Host "未找到运行bot.py的进程，尝试停止所有Python进程..." -ForegroundColor Yellow
    Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
}

Write-Host "机器人已停止" -ForegroundColor Green
Write-Host ""
Write-Host "正在启动机器人..." -ForegroundColor Yellow
Write-Host ""

# 启动机器人
python bot.py

