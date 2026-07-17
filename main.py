"""
ETF-Daily 主程序（增强版 - 支持轮动策略）
每天下午3点10分自动运行分析和邮件发送
"""
import os
import sys
import yaml
import logging
from datetime import datetime
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from fetcher import ETFDataFetcher
from analyzer import TechnicalAnalyzer
from decision import DecisionEngine
from rotation import ETFRotationStrategy
from mailer import EmailSender

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/etf-daily.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def load_config():
    """加载配置文件"""
    config_path = Path(__file__).parent / 'config.yaml'
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # 用环境变量替换配置中的占位符
    config['email']['sender'] = os.getenv('EMAIL_SENDER', config['email']['sender'])
    config['email']['password'] = os.getenv('EMAIL_PASSWORD', config['email']['password'])
    config['email']['receiver'] = os.getenv('EMAIL_RECEIVER', config['email']['receiver'])
    
    return config


def main():
    """主函数"""
    try:
        logger.info("=" * 60)
        logger.info("开始ETF分析 - {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        logger.info("=" * 60)
        
        # 加载配置
        config = load_config()
        logger.info("✓ 配置已加载")
        
        # 创建日志目录
        Path('logs').mkdir(exist_ok=True)
        Path('data').mkdir(exist_ok=True)
        
        # 1. 获取数据
        logger.info("\n[1/6] 获取ETF数据...")
        fetcher = ETFDataFetcher(history_days=config['analysis']['history_days'])
        etf_data = fetcher.fetch_multiple_etfs(config['etf_list'])
        
        if not etf_data:
            logger.error("✗ 未能获取任何ETF数据")
            return False
        
        logger.info(f"✓ 成功获取 {len(etf_data)} 个ETF的数据")
        
        # 2. 技术分析
        logger.info("\n[2/6] 执行技术分析...")
        analyzer = TechnicalAnalyzer(config['technical'])
        analysis_results = []
        
        for code, data in etf_data.items():
            result = analyzer.analyze(data, code)
            if result:
                analysis_results.append(result)
        
        logger.info(f"✓ 完成 {len(analysis_results)} 个ETF的分析")
        
        # 3. 生成交易决策
        logger.info("\n[3/6] 生成交易决策...")
        decision_engine = DecisionEngine(config['decision'])
        decisions = []
        
        for analysis in analysis_results:
            # 查找对应的ETF信息
            etf_info = next(
                (e for e in config['etf_list'] if e['code'] == analysis['code']),
                {'code': analysis['code'], 'name': analysis['code']}
            )
            
            decision = decision_engine.make_decision(analysis)
            decision['code'] = analysis['code']
            decision['price'] = analysis['price']
            decisions.append(decision)
            
            # 输出决策摘要
            summary = decision_engine.generate_summary(etf_info, decision)
            logger.info(summary)
        
        logger.info(f"✓ 生成了 {len(decisions)} 个决策")
        
        # 4. 执行ETF轮动策略分析
        logger.info("\n[4/6] 执行ETF轮动策略分析...")
        rotation_strategy = ETFRotationStrategy(config)
        
        # 只对成功获取数据的ETF进行轮动分析
        valid_etf_data = {code: data for code, data in etf_data.items() if data is not None}
        rotation_result = rotation_strategy.generate_rotation_strategy(
            valid_etf_data,
            config['etf_list']
        )
        
        logger.info("✓ 轮动策略分析完成")
        logger.info("\n【轮动策略建议】")
        for rec in rotation_result['recommendations']:
            logger.info(f"""
  {rec['asset_class']}：{rec['name']}({rec['code']})
  建议：{rec['action']} ({rec['signal_strength']})
  动量：{rec['momentum']:.2f}% | 波动率：{rec['volatility']:.2f}%
  原因：{rec['reason']}
            """)
        
        # 5. 生成报告统计
        logger.info("\n[5/6] 生成报告...")
        strong_buy_count = sum(1 for d in decisions if '强烈买入' in d['decision'])
        buy_count = sum(1 for d in decisions if d['decision'] == '买入')
        sell_count = sum(1 for d in decisions if d['decision'] == '卖出')
        strong_sell_count = sum(1 for d in decisions if '强烈卖出' in d['decision'])
        
        logger.info(f"""
        决策统计:
        - 强烈买入: {strong_buy_count}
        - 买入: {buy_count}
        - 持有: {len(decisions) - strong_buy_count - buy_count - sell_count - strong_sell_count}
        - 卖出: {sell_count}
        - 强烈卖出: {strong_sell_count}
        """)
        
        # 6. 发送邮件
        logger.info("\n[6/6] 发送邮件...")
        mailer = EmailSender(config['email'])
        
        # 检查邮箱配置
        if config['email']['sender'] and config['email']['password'] and config['email']['receiver']:
            if mailer.send_analysis_report(decisions, config['etf_list'], rotation_result):
                logger.info("✓ 报告已发送")
            else:
                logger.warning("✗ 邮件发送失败")
        else:
            logger.warning("⚠ 邮箱配置不完整，跳过发送")
        
        logger.info("\n" + "=" * 60)
        logger.info("分析完成 - {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        logger.info("=" * 60)
        
        return True
    
    except Exception as e:
        logger.error(f"\n✗ 发生错误: {e}", exc_info=True)
        
        # 尝试发送错误通知
        try:
            config = load_config()
            mailer = EmailSender(config['email'])
            mailer.send_error_notification(str(e))
        except:
            pass
        
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
