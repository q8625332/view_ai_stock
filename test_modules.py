"""
模块测试脚本
快速验证各个模块的功能
"""

def test_code_converter():
    """测试代码转换模块"""
    print("\n" + "=" * 60)
    print("测试 1: 股票代码转换模块")
    print("=" * 60)
    
    from modules.code_converter import StockCodeConverter
    
    converter = StockCodeConverter()
    test_codes = ['600519', '000001', '300750', 'sh600036', '00700']
    
    for code in test_codes:
        msn_code = converter.convert_to_msn_format(code)
        market = converter.get_market_name(msn_code)
        print(f"  {code:12} -> {msn_code:12} ({market})")
    
    print("✓ 代码转换模块测试通过")


def test_cache_manager():
    """测试缓存管理模块"""
    print("\n" + "=" * 60)
    print("测试 2: 缓存管理模块")
    print("=" * 60)
    
    from modules.cache_manager import CacheManager
    
    cache = CacheManager()
    
    # 测试数据
    test_data = {
        'dates': ['2024-01-01', '2024-01-02'],
        'open': [100, 102],
        'close': [102, 103]
    }
    
    # 保存缓存
    cache.set('TEST.SS', test_data)
    
    # 读取缓存
    cached = cache.get('TEST.SS')
    
    if cached and cached['dates'] == test_data['dates']:
        print("  ✓ 缓存保存和读取正常")
    else:
        print("  ✗ 缓存测试失败")
    
    # 清除测试缓存
    cache.clear('TEST.SS')
    print("✓ 缓存管理模块测试通过")


def test_data_processor():
    """测试数据处理模块"""
    print("\n" + "=" * 60)
    print("测试 3: 数据处理模块")
    print("=" * 60)
    
    from modules.data_processor import DataProcessor
    
    processor = DataProcessor()
    
    test_data = {
        'stock_code': '600519.SS',
        'dates': ['2024-01-01', '2024-01-02', '2024-01-03'],
        'open': [100.0, 102.0, 101.5],
        'high': [103.0, 104.0, 103.5],
        'low': [99.0, 101.0, 100.5],
        'close': [102.0, 103.0, 102.5],
        'volume': [1000000, 1200000, 1100000]
    }
    
    df = processor.process_stock_data(test_data)
    
    if not df.empty and len(df) == 3:
        print(f"  ✓ 数据处理成功，共 {len(df)} 条记录")
        
        if processor.validate_data(df):
            print("  ✓ 数据验证通过")
        else:
            print("  ✗ 数据验证失败")
        
        stats = processor.calculate_statistics(df)
        print(f"  ✓ 统计信息计算成功")
        print(f"    - 价格范围: {stats['price']['min']:.2f} - {stats['price']['max']:.2f}")
        print(f"    - 涨跌幅: {stats['change']['percent']:.2f}%")
    else:
        print("  ✗ 数据处理失败")
    
    print("✓ 数据处理模块测试通过")


def test_chart_generator():
    """测试图表生成模块"""
    print("\n" + "=" * 60)
    print("测试 4: 图表生成模块")
    print("=" * 60)
    
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta
    from modules.chart_generator import ChartGenerator
    
    # 生成测试数据
    dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
    
    test_data = {}
    for code in ['600519.SS', '000001.SZ']:
        base_price = 100 if code == '600519.SS' else 50
        
        df = pd.DataFrame({
            'Date': dates,
            'Open': base_price + np.random.randn(30) * 2,
            'High': base_price + np.random.randn(30) * 2 + 2,
            'Low': base_price + np.random.randn(30) * 2 - 2,
            'Close': base_price + np.random.randn(30) * 2,
            'Volume': np.random.randint(1000000, 10000000, 30)
        })
        
        test_data[code] = df
    
    generator = ChartGenerator()
    output_path = generator.create_combined_chart(test_data)
    
    if output_path:
        print(f"  ✓ 图表生成成功")
        print(f"  文件路径: {output_path}")
    else:
        print("  ✗ 图表生成失败")
    
    print("✓ 图表生成模块测试通过")


def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("股票K线图系统 - 模块测试")
    print("=" * 60)
    
    try:
        test_code_converter()
        test_cache_manager()
        test_data_processor()
        test_chart_generator()
        
        print("\n" + "=" * 60)
        print("所有模块测试完成！")
        print("=" * 60)
        print("\n提示：可以运行 'python main.py' 来使用完整系统")
        
    except Exception as e:
        print(f"\n测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()