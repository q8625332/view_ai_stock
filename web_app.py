"""
Flask Web应用
提供Web界面查询股票K线图
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
from modules.code_converter import StockCodeConverter
from modules.cache_manager import CacheManager
from modules.scraper import MSNStockScraper
from modules.data_processor import DataProcessor
from modules.chart_generator import ChartGenerator
import plotly.graph_objects as go
from plotly.subplots import make_subplots

app = Flask(__name__)

# 初始化模块
converter = StockCodeConverter()
cache_manager = CacheManager()
processor = DataProcessor()


@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/api/stock', methods=['POST'])
def get_stock_data():
    """获取股票数据API"""
    try:
        data = request.get_json()
        stock_codes = data.get('codes', '').strip()
        
        if not stock_codes:
            return jsonify({'error': '请输入股票代码'}), 400
        
        # 解析股票代码
        codes = [code.strip() for code in stock_codes.split(',')]
        msn_codes = converter.convert_batch(codes)
        
        # 获取数据
        scraper = MSNStockScraper()
        all_stock_data = []
        
        try:
            for msn_code in msn_codes:
                # 检查缓存
                cached_data = cache_manager.get(msn_code)
                
                if cached_data:
                    all_stock_data.append(cached_data)
                else:
                    # 爬取数据
                    stock_data = scraper.fetch_stock_data(msn_code)
                    if stock_data:
                        cache_manager.set(msn_code, stock_data)
                        all_stock_data.append(stock_data)
        finally:
            scraper.close()
        
        if not all_stock_data:
            return jsonify({'error': '未能获取任何股票数据'}), 404
        
        # 处理数据
        processed_data = processor.merge_multiple_stocks(all_stock_data)
        
        if not processed_data:
            return jsonify({'error': '数据处理失败'}), 500
        
        # 生成图表数据
        chart_data = generate_chart_data(processed_data)
        
        # 统计信息
        stats = {}
        for stock_code, df in processed_data.items():
            stats[stock_code] = processor.calculate_statistics(df)
        
        return jsonify({
            'success': True,
            'chart_data': chart_data,
            'stats': stats
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def generate_chart_data(stock_data):
    """生成图表数据，返回JSON格式供前端Plotly渲染"""
    
    # 如果只有一只股票，使用简单布局
    if len(stock_data) == 1:
        stock_code, df = next(iter(stock_data.items()))
        
        traces = []
        
        # K线图 (top plot)
        candlestick_trace = {
            'type': 'candlestick',
            'x': df['Date'].dt.strftime('%Y-%m-%d').tolist(),
            'open': df['Open'].tolist(),
            'high': df['High'].tolist(),
            'low': df['Low'].tolist(),
            'close': df['Close'].tolist(),
            'name': stock_code,
            'increasing': {'line': {'color': 'red'}},
            'decreasing': {'line': {'color': 'green'}},
            'xaxis': 'x2',
            'yaxis': 'y2'
        }
        traces.append(candlestick_trace)
        
        # 成交量 (bottom plot)
        colors = ['red' if close >= open else 'green'
                 for close, open in zip(df['Close'], df['Open'])]
        
        volume_trace = {
            'type': 'bar',
            'x': df['Date'].dt.strftime('%Y-%m-%d').tolist(),
            'y': df['Volume'].tolist(),
            'name': f'{stock_code} 成交量',
            'marker': {'color': colors},
            'showlegend': False,
            'xaxis': 'x',
            'yaxis': 'y'
        }
        traces.append(volume_trace)
        
        layout = {
            'title': f'{stock_code} K线图',
            'height': 600,
            'showlegend': True,
            'hovermode': 'x unified',
            'template': 'plotly_white',
            'xaxis': { # Bottom X axis (for volume)
                'title': '日期',
                'rangeslider': {'visible': False}
            },
            'yaxis': { # Bottom Y axis (for volume)
                'title': '成交量',
                'domain': [0, 0.25]
            },
            'xaxis2': { # Top X axis (for candlestick)
                'matches': 'x',
                'showticklabels': False
            },
            'yaxis2': { # Top Y axis (for candlestick)
                'title': '价格',
                'domain': [0.3, 1]
            }
        }
        
    else:
        # 多股票对比，放在同一个图表中
        traces = []
        
        for stock_code, df in stock_data.items():
            # 只显示K线图，不显示成交量（避免混乱）
            candlestick_trace = {
                'type': 'candlestick',
                'x': df['Date'].dt.strftime('%Y-%m-%d').tolist(),
                'open': df['Open'].tolist(),
                'high': df['High'].tolist(),
                'low': df['Low'].tolist(),
                'close': df['Close'].tolist(),
                'name': stock_code,
                'increasing': {'line': {'color': 'red'}},
                'decreasing': {'line': {'color': 'green'}}
            }
            traces.append(candlestick_trace)
        
        layout = {
            'title': '股票K线对比图',
            'height': 600,
            'showlegend': True,
            'hovermode': 'x unified',
            'template': 'plotly_white',
            'xaxis': {'title': '日期', 'rangeslider': {'visible': False}},
            'yaxis': {'title': '价格'}
        }
    
    return {
        'data': traces,
        'layout': layout
    }


@app.route('/api/cache/clear', methods=['POST'])
def clear_cache():
    """清除缓存API"""
    try:
        data = request.get_json()
        stock_code = data.get('code')
        
        if stock_code:
            cache_manager.clear(stock_code)
            return jsonify({'success': True, 'message': f'已清除 {stock_code} 的缓存'})
        else:
            cache_manager.clear()
            return jsonify({'success': True, 'message': '已清除所有缓存'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/cache/info', methods=['GET'])
def cache_info():
    """获取缓存信息API"""
    try:
        info = cache_manager.get_cache_info()
        return jsonify(info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    import config
    
    # 创建templates目录
    os.makedirs('templates', exist_ok=True)
    
    print("=" * 60)
    print("股票K线图Web服务启动")
    print("=" * 60)
    print(f"访问地址: http://localhost:{config.FLASK_PORT}")
    print(f"主机地址: {config.FLASK_HOST}:{config.FLASK_PORT}")
    print(f"调试模式: {'开启' if config.FLASK_DEBUG else '关闭'}")
    print(f"缓存目录: {config.CACHE_DIR}")
    print(f"输出目录: {config.OUTPUT_DIR}")
    print("按 Ctrl+C 停止服务")
    print("=" * 60)
    
    app.run(host=config.FLASK_HOST, port=config.FLASK_PORT, debug=config.FLASK_DEBUG)