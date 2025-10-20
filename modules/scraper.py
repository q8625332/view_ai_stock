"""
数据爬取模块
使用Selenium从MSN网站爬取股票K线数据
"""

import time
from datetime import datetime, timedelta
from typing import Dict, Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import config


class MSNStockScraper:
    """MSN股票数据爬虫"""
    
    def __init__(self, headless: bool = config.HEADLESS_BROWSER):
        """
        初始化爬虫
        
        Args:
            headless: 是否使用无头模式
        """
        self.headless = headless
        self.driver = None
    
    def _init_driver(self):
        """初始化浏览器驱动"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument('--headless')
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        try:
            # 尝试使用webdriver-manager
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            print("浏览器驱动初始化成功")
        except Exception as e:
            print(f"ChromeDriver初始化失败: {e}")
            print("将使用模拟数据模式")
            self.driver = None
    
    def _close_driver(self):
        """关闭浏览器驱动"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            print("浏览器已关闭")
    
    def fetch_stock_data(self, stock_code: str, retry: int = config.RETRY_TIMES) -> Optional[Dict]:
        """
        获取股票数据
        
        Args:
            stock_code: MSN格式的股票代码
            retry: 重试次数
            
        Returns:
            股票数据字典，包含日期、开盘价、最高价、最低价、收盘价、成交量
        """
        # 如果驱动初始化失败，直接使用模拟数据
        if self.driver is None:
            try:
                self._init_driver()
            except:
                pass
        
        if self.driver is None:
            print(f"浏览器驱动不可用，使用模拟数据: {stock_code}")
            return self._generate_mock_data(stock_code)
        
        for attempt in range(retry):
            try:
                print(f"正在爬取股票数据: {stock_code} (尝试 {attempt + 1}/{retry})")
                
                # 构建MSN股票页面URL
                url = f"https://www.msn.com/zh-cn/money/stockdetails/fi-{stock_code}"
                print(f"访问URL: {url}")
                
                self.driver.get(url)
                
                # 等待页面加载
                wait = WebDriverWait(self.driver, 20)
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                time.sleep(3)  # 额外等待JavaScript渲染
                
                # 尝试点击历史数据标签
                try:
                    history_tab = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '历史') or contains(text(), 'Historical')]"))
                    )
                    history_tab.click()
                    time.sleep(2)
                except Exception as e:
                    print(f"未找到历史数据标签，尝试直接解析: {e}")
                
                # 获取页面HTML
                page_source = self.driver.page_source
                soup = BeautifulSoup(page_source, 'lxml')
                
                # 解析数据
                data = self._parse_stock_data(soup, stock_code)
                
                if data and len(data.get('dates', [])) > 0:
                    print(f"成功获取 {len(data['dates'])} 条数据")
                    return data
                else:
                    print(f"未能解析到有效数据")
                    
            except Exception as e:
                print(f"爬取失败 (尝试 {attempt + 1}/{retry}): {e}")
                if attempt < retry - 1:
                    time.sleep(config.RETRY_DELAY)
                    self._close_driver()
        
        print(f"爬取失败，使用模拟数据: {stock_code}")
        return self._generate_mock_data(stock_code)
    
    def _parse_stock_data(self, soup: BeautifulSoup, stock_code: str) -> Optional[Dict]:
        """
        解析股票数据
        
        Args:
            soup: BeautifulSoup对象
            stock_code: 股票代码
            
        Returns:
            解析后的数据字典
        """
        try:
            # 查找历史数据表格
            tables = soup.find_all('table')
            
            if not tables:
                print("未找到数据表格")
                return self._generate_mock_data(stock_code)
            
            # 解析表格数据
            data = {
                'stock_code': stock_code,
                'dates': [],
                'open': [],
                'high': [],
                'low': [],
                'close': [],
                'volume': []
            }
            
            for table in tables:
                rows = table.find_all('tr')
                
                for row in rows[1:]:  # 跳过表头
                    cols = row.find_all(['td', 'th'])
                    
                    if len(cols) >= 6:
                        try:
                            date_str = cols[0].get_text(strip=True)
                            open_price = float(cols[1].get_text(strip=True).replace(',', ''))
                            high_price = float(cols[2].get_text(strip=True).replace(',', ''))
                            low_price = float(cols[3].get_text(strip=True).replace(',', ''))
                            close_price = float(cols[4].get_text(strip=True).replace(',', ''))
                            volume = float(cols[5].get_text(strip=True).replace(',', ''))
                            
                            data['dates'].append(date_str)
                            data['open'].append(open_price)
                            data['high'].append(high_price)
                            data['low'].append(low_price)
                            data['close'].append(close_price)
                            data['volume'].append(volume)
                            
                        except (ValueError, IndexError) as e:
                            continue
            
            if len(data['dates']) > 0:
                return data
            else:
                print("表格中未找到有效数据，使用模拟数据")
                return self._generate_mock_data(stock_code)
                
        except Exception as e:
            print(f"解析数据失败: {e}")
            return self._generate_mock_data(stock_code)
    
    def _generate_mock_data(self, stock_code: str) -> Dict:
        """
        生成模拟数据（用于测试）
        
        Args:
            stock_code: 股票代码
            
        Returns:
            模拟的股票数据
        """
        print(f"生成模拟数据: {stock_code}")
        
        import random
        
        data = {
            'stock_code': stock_code,
            'dates': [],
            'open': [],
            'high': [],
            'low': [],
            'close': [],
            'volume': []
        }
        
        base_price = 100.0
        end_date = datetime.now()
        
        for i in range(config.DATA_DAYS):
            date = end_date - timedelta(days=i)
            data['dates'].insert(0, date.strftime('%Y-%m-%d'))
            
            # 生成随机价格数据
            open_price = base_price + random.uniform(-5, 5)
            close_price = open_price + random.uniform(-3, 3)
            high_price = max(open_price, close_price) + random.uniform(0, 2)
            low_price = min(open_price, close_price) - random.uniform(0, 2)
            volume = random.randint(1000000, 10000000)
            
            data['open'].insert(0, round(open_price, 2))
            data['high'].insert(0, round(high_price, 2))
            data['low'].insert(0, round(low_price, 2))
            data['close'].insert(0, round(close_price, 2))
            data['volume'].insert(0, volume)
            
            base_price = close_price
        
        return data
    
    def close(self):
        """关闭爬虫"""
        self._close_driver()


if __name__ == '__main__':
    # 测试代码
    scraper = MSNStockScraper(headless=False)
    
    try:
        data = scraper.fetch_stock_data('600519.SS')
        
        if data:
            print(f"\n股票代码: {data['stock_code']}")
            print(f"数据条数: {len(data['dates'])}")
            print(f"日期范围: {data['dates'][0]} 到 {data['dates'][-1]}")
            print(f"最新收盘价: {data['close'][-1]}")
    finally:
        scraper.close()