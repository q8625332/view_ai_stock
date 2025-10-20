"""
图表生成模块
使用Plotly生成交互式K线图
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict
import os
import config


class ChartGenerator:
    """图表生成器"""
    
    @staticmethod
    def create_candlestick_chart(stock_data: Dict[str, pd.DataFrame], output_path: str = None) -> str:
        """
        创建K线图
        
        Args:
            stock_data: 股票代码到DataFrame的映射
            output_path: 输出文件路径
            
        Returns:
            生成的HTML文件路径
        """
        if not stock_data:
            print("没有可用的股票数据")
            return None
        
        # 计算子图数量（每个股票2行：K线图+成交量）
        num_stocks = len(stock_data)
        
        # 创建子图
        fig = make_subplots(
            rows=num_stocks * 2,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            row_heights=[0.7, 0.3] * num_stocks,
            subplot_titles=[f"{code} K线图" for code in stock_data.keys()] + 
                          [f"{code} 成交量" for code in stock_data.keys()]
        )
        
        # 为每个股票添加K线图和成交量图
        for idx, (stock_code, df) in enumerate(stock_data.items()):
            row_candlestick = idx * 2 + 1
            row_volume = idx * 2 + 2
            
            # 添加K线图
            fig.add_trace(
                go.Candlestick(
                    x=df['Date'],
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'],
                    name=stock_code,
                    increasing_line_color='red',
                    decreasing_line_color='green'
                ),
                row=row_candlestick,
                col=1
            )
            
            # 添加成交量柱状图
            colors = ['red' if close >= open else 'green' 
                     for close, open in zip(df['Close'], df['Open'])]
            
            fig.add_trace(
                go.Bar(
                    x=df['Date'],
                    y=df['Volume'],
                    name=f'{stock_code} 成交量',
                    marker_color=colors,
                    showlegend=False
                ),
                row=row_volume,
                col=1
            )
            
            # 更新Y轴标签
            fig.update_yaxes(title_text="价格", row=row_candlestick, col=1)
            fig.update_yaxes(title_text="成交量", row=row_volume, col=1)
        
        # 更新布局
        fig.update_layout(
            title={
                'text': '股票K线图对比',
                'x': 0.5,
                'xanchor': 'center'
            },
            xaxis_rangeslider_visible=False,
            height=400 * num_stocks,
            showlegend=True,
            hovermode='x unified',
            template='plotly_white'
        )
        
        # 更新X轴
        fig.update_xaxes(title_text="日期", row=num_stocks * 2, col=1)
        
        # 保存HTML文件
        if output_path is None:
            output_path = os.path.join(config.OUTPUT_DIR, 'stock_chart.html')
        
        fig.write_html(output_path)
        print(f"图表已保存到: {output_path}")
        
        return output_path
    
    @staticmethod
    def create_comparison_chart(stock_data: Dict[str, pd.DataFrame], output_path: str = None) -> str:
        """
        创建多股票对比图（归一化）
        
        Args:
            stock_data: 股票代码到DataFrame的映射
            output_path: 输出文件路径
            
        Returns:
            生成的HTML文件路径
        """
        if not stock_data:
            print("没有可用的股票数据")
            return None
        
        fig = go.Figure()
        
        # 为每个股票添加归一化的收盘价曲线
        for stock_code, df in stock_data.items():
            # 归一化：以第一天的收盘价为基准
            normalized_close = (df['Close'] / df['Close'].iloc[0] - 1) * 100
            
            fig.add_trace(
                go.Scatter(
                    x=df['Date'],
                    y=normalized_close,
                    mode='lines',
                    name=stock_code,
                    hovertemplate='%{y:.2f}%<extra></extra>'
                )
            )
        
        fig.update_layout(
            title='股票涨跌幅对比（归一化）',
            xaxis_title='日期',
            yaxis_title='涨跌幅 (%)',
            hovermode='x unified',
            template='plotly_white',
            height=600
        )
        
        if output_path is None:
            output_path = os.path.join(config.OUTPUT_DIR, 'stock_comparison.html')
        
        fig.write_html(output_path)
        print(f"对比图已保存到: {output_path}")
        
        return output_path
    
    @staticmethod
    def create_combined_chart(stock_data: Dict[str, pd.DataFrame]) -> str:
        """
        创建组合图表（K线图 + 对比图）
        
        Args:
            stock_data: 股票代码到DataFrame的映射
            
        Returns:
            生成的HTML文件路径
        """
        # 生成K线图
        candlestick_path = ChartGenerator.create_candlestick_chart(stock_data)
        
        # 如果有多个股票，生成对比图
        if len(stock_data) > 1:
            comparison_path = ChartGenerator.create_comparison_chart(stock_data)
            print(f"已生成对比图: {comparison_path}")
        
        return candlestick_path


if __name__ == '__main__':
    # 测试代码
    import numpy as np
    from datetime import datetime, timedelta
    
    # 生成测试数据
    dates = pd.date_range(start='2024-01-01', periods=90, freq='D')
    
    test_data = {}
    for code in ['600519.SS', '000001.SZ']:
        base_price = 100 if code == '600519.SS' else 50
        
        df = pd.DataFrame({
            'Date': dates,
            'Open': base_price + np.random.randn(90) * 2,
            'High': base_price + np.random.randn(90) * 2 + 2,
            'Low': base_price + np.random.randn(90) * 2 - 2,
            'Close': base_price + np.random.randn(90) * 2,
            'Volume': np.random.randint(1000000, 10000000, 90)
        })
        
        test_data[code] = df
    
    # 生成图表
    generator = ChartGenerator()
    output_path = generator.create_combined_chart(test_data)
    print(f"测试图表已生成: {output_path}")