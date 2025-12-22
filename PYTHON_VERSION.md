# Python版本要求

## 问题说明

`qq-botpy` 需要 **Python 3.8 或更高版本**，因为使用了 `TypedDict` 等Python 3.8+的特性。

当前检测到的Python版本：**Python 3.6.5**

## 解决方案

### 方案1：使用Conda创建新环境（推荐）

由于您使用的是Anaconda，可以使用conda创建Python 3.8+的新环境：

```powershell
# 创建新的conda环境，使用Python 3.8
conda create -n qqbot python=3.8

# 激活环境
conda activate qqbot

# 安装依赖
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --user
```

### 方案2：使用Conda安装Python 3.9或3.10

```powershell
# 创建新环境，使用Python 3.9
conda create -n qqbot python=3.9

# 或使用Python 3.10
conda create -n qqbot python=3.10

# 激活环境
conda activate qqbot

# 安装依赖
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --user
```

### 方案3：升级系统Python

如果不想使用conda环境，可以：

1. 从 [Python官网](https://www.python.org/downloads/) 下载Python 3.8或更高版本
2. 安装时选择"Add Python to PATH"
3. 重新安装依赖

### 方案4：使用pyenv（高级用户）

如果使用pyenv管理多个Python版本：

```bash
pyenv install 3.10.0
pyenv local 3.10.0
pip install -r requirements.txt
```

## 验证Python版本

创建新环境后，验证Python版本：

```powershell
python --version
```

应该显示 Python 3.8.x 或更高版本。

## 运行机器人

在正确的Python环境中：

```powershell
python bot.py
```

## 注意事项

- 每次运行机器人前，确保激活了正确的conda环境
- 如果使用conda环境，所有依赖都需要在该环境中安装
- 建议使用Python 3.9或3.10，兼容性更好

