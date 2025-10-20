"""
数据处理模块
清洗和格式化股票数据
"""

import pandas as pd
from typing import Dict, List
from datetime import datetime


class DataProcessor:
    """数据处理器"""
    
    @staticmethod
    def process_stock_data(raw_data: Dict) -> pd.DataFrame:
        """
        处理原始股票数据，转换为DataFrame
        
        Args:
            raw_data: 原始数据字典
            
        Returns:
            处理后的DataFrame
        """
        try:
            df = pd.DataFrame({
                'Date': raw_data['dates'],
                'Open': raw_data['open'],
                'High': raw_data['high'],
                'Low': raw_data['low'],
                'Close': raw_data['close'],
                'Volume': raw_data['volume']
            })
            
            # 转换日期格式
            df['Date'] = pd.to_datetime(df['Date'])
            
            # 按日期排序
            df = df.sort_values('Date').reset_index(drop=True)
            
            # 删除重复数据
            df = df.drop_duplicates(subset=['Date'], keep='last')
            
            # 删除缺失值
            df = df.dropna()
            
            # 确保数值类型
            for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # 再次删除转换失败的行
            df = df.dropna()
            
            print(f"数据处理完成，共 {len(df)} 条有效数据")
            return df
            
        except Exception as e:
            print(f"数据处理失败: {e}")
            return pd.DataFrame()
    
    @staticmethod
    def validate_data(df: pd.DataFrame) -> bool:
        """
        验证数据有效性
        
        Args:
            df: DataFrame
            
        Returns:
            数据是否有效
        """
        if df.empty:
            print("数据为空")
            return False
        
        required_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        if not all(col in df.columns for col in required_columns):
            print("缺少必要的列")
            return False
        
        # 检查价格逻辑
        invalid_rows = df[
            (df['High'] < df['Low']) |
            (df['High'] < df['Open']) |
            (df['High'] < df['Close']) |
            (df['Low'] > df['Open']) |
            (df['Low'] > df['Close'])
        ]
        
        if len(invalid_rows) > 0:
            print(f"发现 {len(invalid_rows)} 条价格逻辑错误的数据")
            return False
        
        return True
    
    @staticmethod
    def calculate_statistics(df: pd.DataFrame) -> Dict:
        """
        计算统计信息
        
        Args:
            df: DataFrame
            
        Returns:
            统计信息字典
        """
        if df.empty:
            return {}
        
        stats = {
            'total_days': len(df),
            'date_range': {
                'start': df['Date'].min().strftime('%Y-%m-%d'),
                'end': df['Date'].max().strftime('%Y-%m-%d')
            },
            'price': {
                'current': float(df['Close'].iloc[-1]),
                'max': float(df['High'].max()),
                'min': float(df['Low'].min()),
                'avg': float(df['Close'].mean())
            },
            'volume': {
                'total': int(df['Volume'].sum()),
                'avg': int(df['Volume'].mean()),
                'max': int(df['Volume'].max())
            },
            'change': {
                'value': float(df['Close'].iloc[-1] - df['Close'].iloc[0]),
                'percent': float((df['Close'].iloc[-1] - df['Close'].iloc[0]) / df['Close'].iloc[0] * 100)
            }
        }
        
        return stats
    
    @staticmethod
    def merge_multiple_stocks(stock_data_list: List[Dict]) -> Dict[str, pd.DataFrame]:
        """
        合并多个股票数据
        
        Args:
            stock_data_list: 股票数据列表
            
        Returns:
            股票代码到DataFrame的映射
        """
        result = {}
        
        for data in stock_data_list:
            if data:
                stock_code = data.get('stock_code', 'Unknown')
                df = DataProcessor.process_stock_data(data)
                
                if not df.empty and DataProcessor.validate_data(df):
                    result[stock_code] = df
                    print(f"股票 {stock_code} 数据处理成功")
                else:
                    print(f"股票 {stock_code} 数据无效，已跳过")
        
        return result


if __name__ == '__main__':
    # 测试代码
    test_data = {
        'stock_code': '600519.SS',
        'dates': ['2024-01-01', '2024-01-02', '2024-01-03'],
        'open': [100.0, 102.0, 101.5],
        'high': [103.0, 104.0, 103.5],
        'low': [99.0, 101.0, 100.5],
        'close': [102.0, 103.0, 102.5],
        'volume': [1000000, 1200000, 1100000]
    }
    
    processor = DataProcessor()
    df = processor.process_stock_data(test_data)
    
    print("\n处理后的数据:")
    print(df)
    
    print("\n数据验证:")
    print(processor.validate_data(df))
    
    print("\n统计信息:")
    stats = processor.calculate_statistics(df)
    for key, value in stats.items():
        print(f"{key}: {value}")