# 机器人重启指南

## 方法1：使用重启脚本（推荐）

### PowerShell脚本
在PowerShell中运行：
```powershell
.\restart_bot.ps1
```

### 批处理脚本
双击运行 `restart_bot.bat` 文件

## 方法2：手动重启

### 步骤1：停止机器人

如果机器人在终端中运行：
- 按 `Ctrl + C` 停止程序

如果机器人在后台运行：
- 打开PowerShell，运行：
  ```powershell
  taskkill /F /IM python.exe
  ```
  或者更精确地：
  ```powershell
  Get-Process python | Where-Object {$_.Path -like "*bot.py*"} | Stop-Process -Force
  ```

### 步骤2：重新启动

在项目目录中运行：
```powershell
python bot.py
```

## 方法3：使用任务管理器

1. 打开任务管理器（`Ctrl + Shift + Esc`）
2. 找到 `python.exe` 进程
3. 右键点击 → 结束任务
4. 重新运行 `python bot.py`

## 注意事项

- 重启前确保已保存所有代码更改
- 如果机器人正在处理消息，等待几秒再重启
- 重启后检查终端输出，确认机器人成功启动

## 快速检查机器人状态

检查是否有Python进程在运行：
```powershell
tasklist | findstr python
```

如果看到 `python.exe` 进程，说明机器人可能正在运行。

