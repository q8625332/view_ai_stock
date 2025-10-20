"""
测试环境配置
验证.env文件是否正确加载
"""

import config

def test_env_config():
    """测试环境配置"""
    print("=" * 60)
    print("环境配置测试")
    print("=" * 60)
    
    print("\n📁 目录配置:")
    print(f"  基础目录: {config.BASE_DIR}")
    print(f"  缓存目录: {config.CACHE_DIR}")
    print(f"  输出目录: {config.OUTPUT_DIR}")
    
    print("\n⚙️ Web服务器配置:")
    print(f"  主机地址: {config.FLASK_HOST}")
    print(f"  端口号: {config.FLASK_PORT}")
    print(f"  调试模式: {config.FLASK_DEBUG}")
    
    print("\n💾 缓存配置:")
    print(f"  缓存有效期: {config.CACHE_EXPIRY_HOURS} 小时")
    
    print("\n📊 数据配置:")
    print(f"  数据天数: {config.DATA_DAYS} 天")
    
    print("\n🌐 浏览器配置:")
    print(f"  无头模式: {config.HEADLESS_BROWSER}")
    print(f"  重试次数: {config.RETRY_TIMES}")
    print(f"  重试延迟: {config.RETRY_DELAY} 秒")
    
    print("\n📝 日志配置:")
    print(f"  日志级别: {config.LOG_LEVEL}")
    
    print("\n" + "=" * 60)
    print("✅ 环境配置加载成功！")
    print("=" * 60)
    
    # 验证配置
    print("\n🔍 配置验证:")
    issues = []
    
    if config.FLASK_PORT < 1024 or config.FLASK_PORT > 65535:
        issues.append(f"⚠️  端口号 {config.FLASK_PORT} 不在有效范围 (1024-65535)")
    
    if config.CACHE_EXPIRY_HOURS < 1:
        issues.append(f"⚠️  缓存有效期 {config.CACHE_EXPIRY_HOURS} 小时太短")
    
    if config.DATA_DAYS < 1 or config.DATA_DAYS > 365:
        issues.append(f"⚠️  数据天数 {config.DATA_DAYS} 不在建议范围 (1-365)")
    
    if config.RETRY_TIMES < 1:
        issues.append(f"⚠️  重试次数 {config.RETRY_TIMES} 太少")
    
    if issues:
        print("\n发现以下问题:")
        for issue in issues:
            print(f"  {issue}")
    else:
        print("  ✅ 所有配置项都在合理范围内")
    
    print("\n💡 提示:")
    print("  - 修改配置请编辑 .env 文件")
    print("  - 配置说明请查看 ENV_CONFIG.md")
    print("  - 重启服务后配置生效")


if __name__ == '__main__':
    try:
        test_env_config()
    except Exception as e:
        print(f"\n❌ 配置加载失败: {e}")
        print("\n请检查:")
        print("  1. .env 文件是否存在")
        print("  2. .env 文件格式是否正确")
        print("  3. python-dotenv 是否已安装")