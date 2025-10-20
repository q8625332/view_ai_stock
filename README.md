# 股票K线图展示系统

基于Python的股票K线图数据爬取和可视化系统，支持从MSN网站获取股票数据，生成交互式K线图。

## 功能特性

- ✅ 支持多股票代码输入和对比
- ✅ 自动转换股票代码格式（支持A股、港股）
- ✅ 使用Selenium爬取MSN网站数据
- ✅ 智能缓存机制（24小时有效期）
- ✅ 数据清洗和验证
- ✅ 交互式K线图（Plotly）
- ✅ 成交量柱状图
- ✅ 多股票涨跌幅对比图
- ✅ 90天历史数据

## 项目结构

```
ai_stock/
├── README.md                 # 项目说明
├── ARCHITECTURE.md           # 架构设计文档
├── requirements.txt          # 依赖包
├── config.py                 # 配置文件
├── main.py                   # 主程序
├── modules/                  # 功能模块
│   ├── __init__.py
│   ├── code_converter.py    # 股票代码转换
│   ├── scraper.py           # 数据爬取
│   ├── cache_manager.py     # 缓存管理
│   ├── data_processor.py    # 数据处理
│   └── chart_generator.py   # 图表生成
├── cache/                    # 缓存目录
└── output/                   # 输出目录
    ├── stock_chart.html     # K线图
    └── stock_comparison.html # 对比图
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 方式一：命令行版本

```bash
python main.py
```

### 方式二：Web版本（推荐）

```bash
python web_app.py
```

然后在浏览器中访问：`http://localhost:5000`

**Web版特点：**
- 🌐 持续运行，无需重复启动
- 🎨 美观的Web界面
- 📊 实时交互式图表
- 💾 智能缓存管理
- 📱 支持远程访问
- 🚀 快速示例按钮

详细使用说明请查看 [WEB_GUIDE.md](WEB_GUIDE.md)

### 2. 输入股票代码

程序会提示输入股票代码，支持以下格式：

```
600519          # 贵州茅台（自动识别为上海）
000001          # 平安银行（自动识别为深圳）
300750          # 宁德时代（自动识别为深圳创业板）
sh600036        # 招商银行（指定上海）
00700           # 腾讯控股（香港）
```

多个股票用逗号分隔：
```
600519,000001,600036
```

### 3. 查看结果

程序会自动生成HTML文件并询问是否在浏览器中打开。

## 配置说明

在 `config.py` 中可以修改以下配置：

```python
CACHE_EXPIRY_HOURS = 24      # 缓存有效期（小时）
DATA_DAYS = 90               # 获取数据天数
HEADLESS_BROWSER = True      # 无头浏览器模式
RETRY_TIMES = 3              # 重试次数
RETRY_DELAY = 2              # 重试延迟（秒）
```

## 模块说明

### code_converter.py
- 股票代码格式转换
- 支持A股、港股、北交所
- 自动识别市场

### scraper.py
- Selenium网页爬虫
- 自动管理ChromeDriver
- 支持重试机制
- 包含模拟数据生成（测试用）

### cache_manager.py
- 本地文件缓存
- JSON格式存储
- 自动过期检查

### data_processor.py
- 数据清洗和验证
- DataFrame转换
- 统计信息计算

### chart_generator.py
- Plotly交互式图表
- K线图 + 成交量图
- 多股票对比图

## 示例输出

### K线图特性
- 红色K线：上涨
- 绿色K线：下跌
- 成交量柱状图
- 时间范围选择
- 悬停显示详情
- 缩放和平移

### 对比图特性
- 归一化涨跌幅
- 多股票曲线对比
- 统一时间轴

## 注意事项

1. **首次运行**：会自动下载ChromeDriver，需要网络连接
2. **数据来源**：MSN网站可能有访问限制，建议使用缓存
3. **模拟数据**：如果爬取失败，会自动生成模拟数据用于测试
4. **浏览器**：需要安装Chrome浏览器

## 故障排除

### 问题1：ChromeDriver下载失败
```bash
# 手动指定ChromeDriver路径
# 在 scraper.py 中修改 Service 配置
```

### 问题2：数据爬取失败
- 检查网络连接
- 尝试关闭无头模式查看浏览器状态
- 使用缓存数据或模拟数据

### 问题3：图表不显示
- 检查output目录是否有HTML文件
- 手动在浏览器中打开HTML文件

## 扩展功能

可以在此基础上添加：
- 技术指标（MA、MACD、RSI等）
- 实时数据更新
- 更多数据源
- Web界面
- 数据导出

## 许可证

MIT License

## 作者

ljq