import os
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

# 基础目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 目录配置
CACHE_DIR = os.path.join(BASE_DIR, os.getenv('CACHE_DIR', 'cache'))
OUTPUT_DIR = os.path.join(BASE_DIR, os.getenv('OUTPUT_DIR', 'output'))

# 缓存配置
CACHE_EXPIRY_HOURS = int(os.getenv('CACHE_EXPIRY_HOURS', '24'))

# 数据配置
DATA_DAYS = int(os.getenv('DATA_DAYS', '90'))

# 浏览器配置
HEADLESS_BROWSER = os.getenv('HEADLESS_BROWSER', 'True').lower() == 'true'
RETRY_TIMES = int(os.getenv('RETRY_TIMES', '3'))
RETRY_DELAY = int(os.getenv('RETRY_DELAY', '2'))

# Web服务器配置
FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
FLASK_PORT = int(os.getenv('FLASK_PORT', '5000'))
FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

# 日志配置
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# 确保目录存在
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)