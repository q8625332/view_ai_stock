"""
股票代码转换模块
将通用股票代码转换为MSN格式
"""


class StockCodeConverter:
    """股票代码转换器"""
    
    # 市场后缀映射
    MARKET_SUFFIX = {
        'sh': '.SS',  # 上海证券交易所
        'sz': '.SZ',  # 深圳证券交易所
        'hk': '.HK',  # 香港交易所
    }
    
    @staticmethod
    def convert_to_msn_format(code: str) -> str:
        """
        将通用股票代码转换为MSN格式
        
        Args:
            code: 股票代码，如 "600519", "000001", "sh600519"
            
        Returns:
            MSN格式的股票代码，如 "600519.SS", "000001.SZ"
        """
        code = code.strip().lower()
        
        # 如果已经包含后缀，直接返回
        if '.' in code:
            return code.upper()
        
        # 处理带市场前缀的代码
        if code.startswith('sh'):
            return code[2:] + '.SS'
        elif code.startswith('sz'):
            return code[2:] + '.SZ'
        elif code.startswith('hk'):
            return code[2:] + '.HK'
        
        # 根据代码规则判断市场
        if len(code) == 6:
            # 6位数字代码
            if code.startswith('6'):
                # 6开头是上海主板
                return code + '.SS'
            elif code.startswith(('0', '3')):
                # 0开头是深圳主板，3开头是创业板
                return code + '.SZ'
            elif code.startswith('4') or code.startswith('8'):
                # 4和8开头是北交所
                return code + '.BJ'
        elif len(code) == 5:
            # 5位数字代码，香港股票
            return code + '.HK'
        
        # 默认返回原代码
        return code.upper()
    
    @staticmethod
    def convert_batch(codes: list) -> list:
        """
        批量转换股票代码
        
        Args:
            codes: 股票代码列表
            
        Returns:
            转换后的代码列表
        """
        return [StockCodeConverter.convert_to_msn_format(code) for code in codes]
    
    @staticmethod
    def get_market_name(code: str) -> str:
        """
        获取市场名称
        
        Args:
            code: MSN格式的股票代码
            
        Returns:
            市场名称
        """
        if '.SS' in code:
            return '上海证券交易所'
        elif '.SZ' in code:
            return '深圳证券交易所'
        elif '.HK' in code:
            return '香港交易所'
        elif '.BJ' in code:
            return '北京证券交易所'
        else:
            return '未知市场'


if __name__ == '__main__':
    # 测试代码
    converter = StockCodeConverter()
    
    test_codes = [
        '600519',  # 贵州茅台
        '000001',  # 平安银行
        '300750',  # 宁德时代
        'sh600036',  # 招商银行
        '00700',  # 腾讯控股
    ]
    
    print("股票代码转换测试：")
    for code in test_codes:
        msn_code = converter.convert_to_msn_format(code)
        market = converter.get_market_name(msn_code)
        print(f"{code:12} -> {msn_code:12} ({market})")