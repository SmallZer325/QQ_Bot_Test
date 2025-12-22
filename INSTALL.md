# 安装指南

## 解决SSL证书问题

如果遇到SSL证书错误，可以使用以下方法：

### 方法1：使用国内镜像源（推荐）

使用清华大学镜像源安装：

```powershell
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --user
```

**注意**：如果遇到权限问题，添加 `--user` 参数安装到用户目录。

或者使用阿里云镜像：

```powershell
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --user
```

### 方法2：永久配置镜像源

创建或编辑 `pip.ini` 文件（Windows）：

位置：`%APPDATA%\pip\pip.ini`

内容：
```ini
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host = pypi.tuna.tsinghua.edu.cn
```

然后直接运行：
```powershell
pip install -r requirements.txt
```

### 方法3：更新pip和证书

```powershell
python -m pip install --upgrade pip
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt --user
```

## 版本兼容性说明

由于某些镜像源的包版本可能较旧，`requirements.txt` 中的版本要求已调整为兼容旧版本：

- `httpx>=0.22.0`（镜像源最高版本）
- `requests>=2.25.0`（镜像源最高版本）
- `pyyaml>=5.0`（兼容旧版本）

如果使用官方PyPI源，可以安装更新版本。

### 方法4：使用conda（如果已安装）

```powershell
conda install -c conda-forge qq-botpy httpx aiohttp pyyaml requests
```

## 验证安装

安装完成后，运行以下命令验证：

```powershell
python -c "import botpy; print('qq-botpy安装成功！')"
```

## 如果仍然失败

1. 检查网络连接
2. 检查防火墙设置
3. 尝试使用VPN或代理
4. 联系网络管理员检查SSL证书配置

