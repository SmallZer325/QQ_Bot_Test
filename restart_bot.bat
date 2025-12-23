@echo off
REM QQ机器人重启脚本（批处理版本）
REM 使用方法：双击运行此文件

echo 正在停止机器人...

REM 停止所有运行bot.py的Python进程
taskkill /F /FI "WINDOWTITLE eq *bot.py*" 2>nul
taskkill /F /IM python.exe 2>nul

timeout /t 2 /nobreak >nul

echo 机器人已停止
echo.
echo 正在启动机器人...
echo.

REM 启动机器人
python bot.py

pause

