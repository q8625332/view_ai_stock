"""
股票K线图主程序
整合所有模块，实现完整的数据获取和图表生成流程
"""

import os
import webbrowser
from modules.code_converter import StockCodeConverter
from modules.cache_manager import CacheManager
from modules.scraper import MSNStockScraper
from modules.data_processor import DataProcessor
from modules.chart_generator import ChartGenerator


def main():
    """主函数"""
    print("=" * 60)
    print("股票K线图生成系统")
    print("=" * 60)
    
    # 获取用户输入
    user_input = input("\n请输入股票代码（多个代码用逗号分隔，如：600519,000001,600036）：")
    
    if not user_input.strip():
        print("未输入股票代码，使用默认示例：600519,000001,600036")
        user_input = "600519,000001,600036"
    
    # 解析股票代码
    stock_codes = [code.strip() for code in user_input.split(',')]
    print(f"\n将处理 {len(stock_codes)} 只股票")
    
    # 初始化模块
    converter = StockCodeConverter()
    cache_manager = CacheManager()
    scraper = MSNStockScraper()
    processor = DataProcessor()
    
    # 转换股票代码
    print("\n" + "=" * 60)
    print("步骤 1: 转换股票代码格式")
    print("=" * 60)
    msn_codes = converter.convert_batch(stock_codes)
    for original, msn in zip(stock_codes, msn_codes):
        market = converter.get_market_name(msn)
        print(f"{original:12} -> {msn:12} ({market})")
    
    # 获取数据
    print("\n" + "=" * 60)
    print("步骤 2: 获取股票数据")
    print("=" * 60)
    
    all_stock_data = []
    
    try:
        for msn_code in msn_codes:
            print(f"\n处理股票: {msn_code}")
            
            # 检查缓存
            cached_data = cache_manager.get(msn_code)
            
            if cached_data:
                print(f"使用缓存数据: {msn_code}")
                all_stock_data.append(cached_data)
            else:
                # 爬取数据
                print(f"开始爬取数据: {msn_code}")
                stock_data = scraper.fetch_stock_data(msn_code)
                
                if stock_data:
                    # 保存到缓存
                    cache_manager.set(msn_code, stock_data)
                    all_stock_data.append(stock_data)
                else:
                    print(f"获取数据失败: {msn_code}")
    
    finally:
        # 关闭浏览器
        scraper.close()
    
    if not all_stock_data:
        print("\n错误：未能获取任何股票数据")
        return
    
    # 处理数据
    print("\n" + "=" * 60)
    print("步骤 3: 处理和验证数据")
    print("=" * 60)
    
    processed_data = processor.merge_multiple_stocks(all_stock_data)
    
    if not processed_data:
        print("\n错误：数据处理失败")
        return
    
    # 显示统计信息
    print("\n数据统计信息：")
    for stock_code, df in processed_data.items():
        stats = processor.calculate_statistics(df)
        print(f"\n{stock_code}:")
        print(f"  数据天数: {stats['total_days']}")
        print(f"  日期范围: {stats['date_range']['start']} 到 {stats['date_range']['end']}")
        print(f"  当前价格: {stats['price']['current']:.2f}")
        print(f"  涨跌幅: {stats['change']['percent']:.2f}%")
    
    # 生成图表
    print("\n" + "=" * 60)
    print("步骤 4: 生成K线图")
    print("=" * 60)
    
    generator = ChartGenerator()
    output_path = generator.create_combined_chart(processed_data)
    
    if output_path and os.path.exists(output_path):
        print(f"\n✓ 图表生成成功！")
        print(f"文件路径: {output_path}")
        
        # 询问是否打开
        open_browser = input("\n是否在浏览器中打开图表？(y/n): ").strip().lower()
        if open_browser == 'y' or open_browser == '':
            webbrowser.open('file://' + os.path.abspath(output_path))
            print("已在浏览器中打开图表")
    else:
        print("\n错误：图表生成失败")
    
    print("\n" + "=" * 60)
    print("程序执行完成")
    print("=" * 60)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
    except Exception as e:
        print(f"\n程序执行出错: {e}")
        import traceback
        traceback.print_exc()