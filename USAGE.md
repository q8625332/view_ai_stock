# 使用指南

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 运行程序
```bash
python main.py
```

### 3. 输入股票代码
程序会提示输入股票代码，支持以下格式：

**单个股票：**
```
600519
```

**多个股票（逗号分隔）：**
```
600519,000001,600036
```

**支持的代码格式：**
- `600519` - 自动识别为上海主板（贵州茅台）
- `000001` - 自动识别为深圳主板（平安银行）
- `300750` - 自动识别为深圳创业板（宁德时代）
- `sh600036` - 指定上海市场（招商银行）
- `00700` - 香港股票（腾讯控股）

### 4. 查看结果
程序会生成两个HTML文件：
- `output/stock_chart.html` - K线图和成交量图
- `output/stock_comparison.html` - 多股票涨跌幅对比图（仅多股票时）

## 功能说明

### K线图特性
- **红色K线**：当日上涨（收盘价 > 开盘价）
- **绿色K线**：当日下跌（收盘价 < 开盘价）
- **成交量柱状图**：与K线颜色对应
- **交互功能**：
  - 鼠标悬停显示详细信息
  - 拖动缩放查看特定时间段
  - 双击重置视图
  - 时间范围选择器

### 数据来源
1. **优先使用缓存**：如果24小时内有缓存数据，直接使用
2. **尝试爬取MSN**：无缓存时尝试从MSN网站爬取
3. **自动模拟数据**：爬取失败时自动生成模拟数据用于演示

### 缓存机制
- 缓存位置：`cache/` 目录
- 缓存格式：JSON文件
- 有效期：24小时
- 文件命名：`{股票代码}_{日期}.json`

## 配置选项

编辑 `config.py` 修改配置：

```python
# 缓存有效期（小时）
CACHE_EXPIRY_HOURS = 24

# 获取数据天数
DATA_DAYS = 90

# 浏览器模式（True=无头模式，False=显示浏览器）
HEADLESS_BROWSER = True

# 重试次数
RETRY_TIMES = 3

# 重试延迟（秒）
RETRY_DELAY = 2
```

## 常见问题

### Q1: ChromeDriver错误
**问题**：`[WinError 193] %1 不是有效的 Win32 应用程序`

**解决**：程序会自动使用模拟数据，无需手动处理。如需真实数据：
1. 确保安装了Chrome浏览器
2. 检查Python版本是否为64位
3. 手动下载对应版本的ChromeDriver

### Q2: 数据爬取失败
**问题**：无法从MSN获取数据

**解决**：
- 程序会自动使用模拟数据
- 检查网络连接
- 尝试关闭无头模式查看浏览器状态：
  ```python
  # config.py
  HEADLESS_BROWSER = False
  ```

### Q3: 图表不显示
**问题**：HTML文件打开后无内容

**解决**：
- 检查 `output/` 目录是否有HTML文件
- 尝试用不同浏览器打开
- 查看浏览器控制台是否有JavaScript错误

### Q4: 清除缓存
**方法1**：删除 `cache/` 目录下的文件

**方法2**：使用Python脚本
```python
from modules.cache_manager import CacheManager
cache = CacheManager()
cache.clear()  # 清除所有缓存
cache.clear('600519.SS')  # 清除指定股票缓存
```

## 高级用法

### 1. 仅测试模块
```bash
python test_modules.py
```

### 2. 单独测试某个模块
```python
# 测试代码转换
python modules/code_converter.py

# 测试数据处理
python modules/data_processor.py

# 测试图表生成
python modules/chart_generator.py
```

### 3. 自定义数据源
修改 `modules/scraper.py` 中的 `fetch_stock_data` 方法，可以接入其他数据源：
- Yahoo Finance API
- 新浪财经API
- Tushare
- AKShare

### 4. 添加技术指标
在 `modules/chart_generator.py` 中添加技术指标计算和绘制：
```python
# 示例：添加MA均线
df['MA5'] = df['Close'].rolling(window=5).mean()
df['MA10'] = df['Close'].rolling(window=10).mean()

fig.add_trace(go.Scatter(x=df['Date'], y=df['MA5'], name='MA5'))
fig.add_trace(go.Scatter(x=df['Date'], y=df['MA10'], name='MA10'))
```

## 性能优化

### 1. 使用缓存
- 避免频繁爬取相同股票
- 缓存有效期内直接读取本地数据

### 2. 批量处理
- 一次输入多个股票代码
- 程序会依次处理并生成对比图

### 3. 无头模式
- 默认使用无头浏览器，速度更快
- 调试时可关闭无头模式查看过程

## 数据说明

### 模拟数据特点
- 基于随机游走算法生成
- 价格波动符合正态分布
- 成交量随机生成
- 仅用于演示和测试

### 真实数据来源
- MSN财经网站
- 包含开盘价、最高价、最低价、收盘价、成交量
- 数据更新频率取决于MSN网站

## 扩展建议

1. **实时数据**：接入WebSocket实时数据流
2. **更多指标**：MACD、RSI、布林带等
3. **预警功能**：价格突破、成交量异常等
4. **数据导出**：CSV、Excel格式
5. **Web界面**：Flask/Django Web应用
6. **移动端**：响应式设计或原生应用

## 技术支持

遇到问题请查看：
1. `README.md` - 项目概述
2. `ARCHITECTURE.md` - 架构设计
3. 本文档 - 使用指南

或提交Issue到项目仓库。