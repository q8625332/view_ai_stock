# Web版使用指南

## 🚀 快速启动

### 1. 启动Web服务器
```bash
python web_app.py
```

服务器启动后会显示：
```
============================================================
股票K线图Web服务启动
============================================================
访问地址: http://localhost:5000
按 Ctrl+C 停止服务
============================================================
```

### 2. 访问Web界面
在浏览器中打开：
```
http://localhost:5000
```

或者在局域网内其他设备访问：
```
http://你的IP地址:5000
```

## 📱 Web界面功能

### 主要功能
1. **股票查询**
   - 输入框输入股票代码
   - 支持单个或多个股票（逗号分隔）
   - 点击"查询"按钮获取数据

2. **快速示例**
   - 点击示例标签快速填充代码
   - 贵州茅台、平安银行、宁德时代等
   - 多股票对比示例

3. **实时统计**
   - 当前价格
   - 涨跌幅（红涨绿跌）
   - 最高价/最低价
   - 数据天数

4. **交互式K线图**
   - 红色K线：上涨
   - 绿色K线：下跌
   - 成交量柱状图
   - 鼠标悬停显示详情
   - 拖动缩放查看

5. **缓存管理**
   - 自动缓存24小时
   - 一键清除缓存按钮
   - 避免频繁请求

## 🎨 界面特点

### 美观设计
- 渐变色背景
- 卡片式布局
- 响应式设计
- 动画效果

### 用户体验
- 加载动画
- 错误提示
- 快速示例
- 回车键查询

## 🔧 API接口

### 1. 查询股票数据
```
POST /api/stock
Content-Type: application/json

{
  "codes": "600519,000001"
}

响应：
{
  "success": true,
  "chart": "<html>...</html>",
  "stats": {
    "600519.SS": {
      "total_days": 90,
      "price": {...},
      "change": {...}
    }
  }
}
```

### 2. 清除缓存
```
POST /api/cache/clear
Content-Type: application/json

{
  "code": "600519.SS"  // 可选，不传则清除所有
}

响应：
{
  "success": true,
  "message": "已清除缓存"
}
```

### 3. 获取缓存信息
```
GET /api/cache/info

响应：
{
  "total_files": 3,
  "cache_dir": "cache",
  "files": [...]
}
```

## 💡 使用技巧

### 1. 多股票对比
输入多个代码，用逗号分隔：
```
600519,000001,600036
```

### 2. 支持的代码格式
- `600519` - 自动识别上海主板
- `000001` - 自动识别深圳主板
- `300750` - 自动识别创业板
- `sh600036` - 指定上海市场
- `00700` - 香港股票

### 3. 快速查询
- 使用快速示例标签
- 回车键直接查询
- 浏览器收藏常用查询

### 4. 性能优化
- 首次查询会缓存数据
- 24小时内使用缓存
- 需要最新数据时清除缓存

## 🌐 部署到服务器

### 本地网络访问
修改 `web_app.py` 最后一行：
```python
app.run(host='0.0.0.0', port=5000, debug=False)
```

然后局域网内其他设备可以通过你的IP访问。

### 生产环境部署
使用 Gunicorn 或 uWSGI：

```bash
# 安装 Gunicorn
pip install gunicorn

# 启动服务
gunicorn -w 4 -b 0.0.0.0:5000 web_app:app
```

### Docker部署
创建 `Dockerfile`：
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "web_app.py"]
```

构建和运行：
```bash
docker build -t stock-chart .
docker run -p 5000:5000 stock-chart
```

## 🔒 安全建议

### 1. 生产环境
- 关闭 debug 模式
- 使用 HTTPS
- 添加身份验证
- 限制请求频率

### 2. 防火墙设置
```bash
# 仅允许特定IP访问
# 在防火墙中配置规则
```

### 3. 环境变量
将敏感配置放入环境变量：
```python
import os
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
```

## 📊 监控和日志

### 添加日志
```python
import logging
logging.basicConfig(level=logging.INFO)
```

### 性能监控
- 使用 Flask-Monitoring-Dashboard
- 记录请求时间
- 监控缓存命中率

## 🐛 故障排除

### 问题1：端口被占用
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <进程ID> /F

# Linux/Mac
lsof -i :5000
kill -9 <进程ID>
```

### 问题2：无法访问
- 检查防火墙设置
- 确认服务器正在运行
- 验证IP地址和端口

### 问题3：数据加载慢
- 使用缓存功能
- 减少同时查询的股票数量
- 检查网络连接

## 🎯 扩展功能

### 可以添加的功能
1. **用户系统**
   - 注册/登录
   - 收藏股票
   - 自选股列表

2. **实时更新**
   - WebSocket推送
   - 自动刷新
   - 价格预警

3. **更多图表**
   - 技术指标（MA、MACD、RSI）
   - 分时图
   - 资金流向

4. **数据导出**
   - CSV下载
   - Excel报表
   - PDF报告

5. **移动端优化**
   - 响应式设计
   - 触摸手势
   - PWA支持

## 📝 命令行 vs Web版

### 命令行版（main.py）
- 适合：一次性查询、脚本自动化
- 优点：简单直接、无需浏览器
- 缺点：每次都要重新运行

### Web版（web_app.py）
- 适合：频繁查询、多人使用
- 优点：持续运行、界面友好、支持远程访问
- 缺点：需要保持服务器运行

## 🔄 更新和维护

### 更新代码
```bash
git pull  # 如果使用Git
python web_app.py  # 重启服务
```

### 清理缓存
```bash
# 手动清理
rm -rf cache/*

# 或使用Web界面的清除缓存按钮
```

### 备份数据
```bash
# 备份缓存
tar -czf cache_backup.tar.gz cache/

# 备份配置
cp config.py config.py.bak
```

## 📞 技术支持

遇到问题请查看：
1. 本文档
2. README.md
3. USAGE.md
4. ARCHITECTURE.md

或提交Issue到项目仓库。

---

**享受使用股票K线图Web查询系统！** 📈