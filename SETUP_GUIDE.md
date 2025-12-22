# 快速设置指南

## 当前问题

您的Python版本是 **3.6.5**，但 `qq-botpy` 需要 **Python 3.8+**。

## 推荐解决方案

### 方案1：直接安装Python 3.9（最简单）

1. 访问 [Python官网](https://www.python.org/downloads/)
2. 下载 Python 3.9 或 3.10（推荐3.10）
3. 安装时**务必勾选** "Add Python to PATH"
4. 安装完成后，重新打开PowerShell
5. 验证版本：
   ```powershell
   python --version
   ```
6. 安装依赖：
   ```powershell
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

### 方案2：使用Conda（如果镜像源正常）

```powershell
# 使用conda默认源
conda create -n qqbot python=3.9

# 激活环境
conda activate qqbot

# 安装依赖
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 方案3：使用Miniconda（轻量级）

如果Anaconda有问题，可以安装Miniconda：

1. 下载 [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
2. 安装后创建环境：
   ```powershell
   conda create -n qqbot python=3.9
   conda activate qqbot
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

## 验证安装

安装完成后，运行：

```powershell
python --version
# 应该显示 Python 3.9.x 或更高

python -c "import botpy; print('qq-botpy安装成功！')"
```

## 运行机器人

```powershell
python bot.py
```

## 注意事项

- 如果使用方案1（直接安装Python），确保PATH中Python 3.9的路径在Python 3.6之前
- 如果使用conda环境，每次运行前需要先激活：`conda activate qqbot`
- 建议使用Python 3.9或3.10，兼容性最好

