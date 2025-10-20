"""
缓存管理模块
管理股票数据的本地缓存
"""

import os
import json
from datetime import datetime, timedelta
from typing import Optional, Dict
import config


class CacheManager:
    """缓存管理器"""
    
    def __init__(self, cache_dir: str = config.CACHE_DIR):
        """
        初始化缓存管理器
        
        Args:
            cache_dir: 缓存目录路径
        """
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_cache_path(self, stock_code: str) -> str:
        """
        获取缓存文件路径
        
        Args:
            stock_code: 股票代码
            
        Returns:
            缓存文件路径
        """
        safe_code = stock_code.replace('.', '_')
        return os.path.join(self.cache_dir, f"{safe_code}.json")
    
    def get(self, stock_code: str) -> Optional[Dict]:
        """
        获取缓存数据
        
        Args:
            stock_code: 股票代码
            
        Returns:
            缓存的数据字典，如果缓存不存在或已过期则返回None
        """
        cache_path = self._get_cache_path(stock_code)
        
        if not os.path.exists(cache_path):
            return None
        
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            # 检查缓存是否过期
            cache_time = datetime.fromisoformat(cache_data.get('timestamp', ''))
            expiry_time = cache_time + timedelta(hours=config.CACHE_EXPIRY_HOURS)
            
            if datetime.now() > expiry_time:
                print(f"缓存已过期: {stock_code}")
                return None
            
            print(f"使用缓存数据: {stock_code}")
            return cache_data.get('data')
            
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            print(f"缓存读取失败: {stock_code}, 错误: {e}")
            return None
    
    def set(self, stock_code: str, data: Dict) -> bool:
        """
        保存数据到缓存
        
        Args:
            stock_code: 股票代码
            data: 要缓存的数据
            
        Returns:
            是否保存成功
        """
        cache_path = self._get_cache_path(stock_code)
        
        try:
            cache_data = {
                'timestamp': datetime.now().isoformat(),
                'stock_code': stock_code,
                'data': data
            }
            
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            
            print(f"数据已缓存: {stock_code}")
            return True
            
        except Exception as e:
            print(f"缓存保存失败: {stock_code}, 错误: {e}")
            return False
    
    def clear(self, stock_code: Optional[str] = None) -> bool:
        """
        清除缓存
        
        Args:
            stock_code: 股票代码，如果为None则清除所有缓存
            
        Returns:
            是否清除成功
        """
        try:
            if stock_code:
                cache_path = self._get_cache_path(stock_code)
                if os.path.exists(cache_path):
                    os.remove(cache_path)
                    print(f"已清除缓存: {stock_code}")
            else:
                for file in os.listdir(self.cache_dir):
                    if file.endswith('.json'):
                        os.remove(os.path.join(self.cache_dir, file))
                print("已清除所有缓存")
            
            return True
            
        except Exception as e:
            print(f"清除缓存失败: {e}")
            return False
    
    def get_cache_info(self) -> Dict:
        """
        获取缓存信息
        
        Returns:
            缓存信息字典
        """
        cache_files = [f for f in os.listdir(self.cache_dir) if f.endswith('.json')]
        
        info = {
            'total_files': len(cache_files),
            'cache_dir': self.cache_dir,
            'files': []
        }
        
        for file in cache_files:
            file_path = os.path.join(self.cache_dir, file)
            file_stat = os.stat(file_path)
            info['files'].append({
                'name': file,
                'size': file_stat.st_size,
                'modified': datetime.fromtimestamp(file_stat.st_mtime).isoformat()
            })
        
        return info


if __name__ == '__main__':
    # 测试代码
    cache = CacheManager()
    
    # 测试保存和读取
    test_data = {
        'dates': ['2024-01-01', '2024-01-02'],
        'prices': [100, 102]
    }
    
    cache.set('600519.SS', test_data)
    cached = cache.get('600519.SS')
    print(f"缓存测试: {cached}")
    
    # 查看缓存信息
    info = cache.get_cache_info()
    print(f"缓存信息: {info}")