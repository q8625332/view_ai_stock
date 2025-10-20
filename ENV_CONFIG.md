# 环境配置说明

## 📋 配置文件

项目使用 `.env` 文件进行环境配置，支持灵活的参数调整。

## 🚀 快速开始

### 1. 复制配置文件
```bash
cp .env.example .env
```

### 2. 编辑配置
使用文本编辑器打开 `.env` 文件，根据需要修改配置。

### 3. 安装依赖
```bash
pip install python-dotenv
```

## ⚙️ 配置项说明

### Web服务器配置

#### FLASK_HOST
- **说明**: Flask服务器监听的主机地址
- **默认值**: `0.0.0.0`
- **可选值**: 
  - `0.0.0.0` - 允许所有IP访问（局域网可访问）
  - `127.0.0.1` - 仅本机访问
  - 具体IP地址 - 指定IP访问
- **示例**: 
  ```
  FLASK_HOST=0.0.0.0
  ```

#### FLASK_PORT
- **说明**: Flask服务器监听的端口号
- **默认值**: `5000`
- **可选值**: `1024-65535` 之间的任意端口
- **注意**: 
  - 1024以下的端口需要管理员权限
  - 确保端口未被占用
- **示例**: 
  ```
  FLASK_PORT=8080
  ```

#### FLASK_DEBUG
- **说明**: 是否启用Flask调试模式
- **默认值**: `False`
- **可选值**: 
  - `True` - 开启调试模式（开发环境）
  - `False` - 关闭调试模式（生产环境）
- **注意**: 生产环境必须设置为 `False`
- **示例**: 
  ```
  FLASK_DEBUG=True
  ```

### 缓存配置

#### CACHE_EXPIRY_HOURS
- **说明**: 缓存有效期（小时）
- **默认值**: `24`
- **可选值**: 任意正整数
- **建议**: 
  - 开发测试: `1-6` 小时
  - 正常使用: `24` 小时
  - 长期缓存: `72-168` 小时
- **示例**: 
  ```
  CACHE_EXPIRY_HOURS=24
  ```

#### CACHE_DIR
- **说明**: 缓存文件存储目录
- **默认值**: `cache`
- **可选值**: 任意有效的目录路径
- **注意**: 程序会自动创建目录
- **示例**: 
  ```
  CACHE_DIR=cache
  ```

### 数据配置

#### DATA_DAYS
- **说明**: 获取股票历史数据的天数
- **默认值**: `90`
- **可选值**: `1-365` 天
- **建议**: 
  - 短期分析: `30-60` 天
  - 中期分析: `90-180` 天
  - 长期分析: `180-365` 天
- **示例**: 
  ```
  DATA_DAYS=90
  ```

### 浏览器配置

#### HEADLESS_BROWSER
- **说明**: 是否使用无头浏览器模式
- **默认值**: `True`
- **可选值**: 
  - `True` - 无头模式（后台运行，速度快）
  - `False` - 显示浏览器（调试用）
- **示例**: 
  ```
  HEADLESS_BROWSER=True
  ```

#### RETRY_TIMES
- **说明**: 数据爬取失败时的重试次数
- **默认值**: `3`
- **可选值**: `1-10` 次
- **建议**: `3-5` 次
- **示例**: 
  ```
  RETRY_TIMES=3
  ```

#### RETRY_DELAY
- **说明**: 重试之间的延迟时间（秒）
- **默认值**: `2`
- **可选值**: `1-10` 秒
- **建议**: `2-5` 秒
- **示例**: 
  ```
  RETRY_DELAY=2
  ```

### 输出配置

#### OUTPUT_DIR
- **说明**: 生成的图表文件存储目录
- **默认值**: `output`
- **可选值**: 任意有效的目录路径
- **注意**: 程序会自动创建目录
- **示例**: 
  ```
  OUTPUT_DIR=output
  ```

### 日志配置

#### LOG_LEVEL
- **说明**: 日志输出级别
- **默认值**: `INFO`
- **可选值**: 
  - `DEBUG` - 详细调试信息
  - `INFO` - 一般信息
  - `WARNING` - 警告信息
  - `ERROR` - 错误信息
  - `CRITICAL` - 严重错误
- **示例**: 
  ```
  LOG_LEVEL=INFO
  ```

## 📝 配置示例

### 开发环境配置
```env
# 开发环境 - 本地调试
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
FLASK_DEBUG=True
CACHE_EXPIRY_HOURS=1
DATA_DAYS=30
HEADLESS_BROWSER=False
LOG_LEVEL=DEBUG
```

### 生产环境配置
```env
# 生产环境 - 服务器部署
FLASK_HOST=0.0.0.0
FLASK_PORT=8080
FLASK_DEBUG=False
CACHE_EXPIRY_HOURS=24
DATA_DAYS=90
HEADLESS_BROWSER=True
LOG_LEVEL=INFO
```

### 测试环境配置
```env
# 测试环境 - 快速测试
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
FLASK_DEBUG=True
CACHE_EXPIRY_HOURS=6
DATA_DAYS=60
HEADLESS_BROWSER=True
LOG_LEVEL=INFO
```

## 🔧 常见配置场景

### 场景1: 更改Web服务端口
如果5000端口被占用，修改为其他端口：
```env
FLASK_PORT=8080
```

### 场景2: 允许局域网访问
让局域网内其他设备访问：
```env
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
```

### 场景3: 调试爬虫问题
查看浏览器操作过程：
```env
HEADLESS_BROWSER=False
FLASK_DEBUG=True
LOG_LEVEL=DEBUG
```

### 场景4: 减少缓存时间
频繁更新数据：
```env
CACHE_EXPIRY_HOURS=1
```

### 场景5: 获取更多历史数据
分析长期趋势：
```env
DATA_DAYS=180
```

## 🔒 安全建议

### 1. 不要提交.env文件
`.env` 文件已添加到 `.gitignore`，不会被提交到版本控制。

### 2. 生产环境关闭调试
```env
FLASK_DEBUG=False
```

### 3. 限制访问IP
如果不需要远程访问：
```env
FLASK_HOST=127.0.0.1
```

### 4. 使用非标准端口
避免使用常见端口：
```env
FLASK_PORT=8888
```

## 🐛 故障排除

### 问题1: 配置不生效
**原因**: `.env` 文件不存在或格式错误

**解决**: 
```bash
# 检查文件是否存在
ls -la .env

# 重新复制配置文件
cp .env.example .env
```

### 问题2: 端口被占用
**错误**: `Address already in use`

**解决**: 修改端口号
```env
FLASK_PORT=8080
```

### 问题3: 无法远程访问
**原因**: HOST设置为127.0.0.1

**解决**: 
```env
FLASK_HOST=0.0.0.0
```

### 问题4: 缓存不更新
**原因**: 缓存有效期太长

**解决**: 
```env
CACHE_EXPIRY_HOURS=1
```
或使用Web界面的"清除缓存"按钮

## 📚 相关文档

- [README.md](README.md) - 项目概述
- [WEB_GUIDE.md](WEB_GUIDE.md) - Web版使用指南
- [USAGE.md](USAGE.md) - 命令行版使用指南

## 💡 最佳实践

1. **开发时**: 使用 `FLASK_DEBUG=True` 和 `LOG_LEVEL=DEBUG`
2. **生产时**: 使用 `FLASK_DEBUG=False` 和 `LOG_LEVEL=INFO`
3. **测试时**: 使用较短的缓存时间和较少的数据天数
4. **部署时**: 备份 `.env` 文件，避免配置丢失
5. **更新时**: 参考 `.env.example` 查看新增的配置项