"""
邮件发送模块增强版 - 支持轮动策略报告
"""
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class EmailSender:
    """邮件发送器"""
    
    def __init__(self, config: Dict):
        """
        初始化邮件发送器
        
        Args:
            config: 邮件配置字典
        """
        self.config = config
    
    def send_analysis_report(self, decisions: List[Dict], etf_list: List[Dict], 
                             rotation_result: Optional[Dict] = None) -> bool:
        """
        发送分析报告（包含轮动策略）
        
        Args:
            decisions: 决策列表
            etf_list: ETF信息列表
            rotation_result: 轮动策略结果（可选）
            
        Returns:
            是否发送成功
        """
        try:
            # 生成邮件内容
            html_content = self._generate_html_report(decisions, etf_list, rotation_result)
            
            # 发送邮件
            return self._send_email(
                subject=f"ETF-Daily 分析报告 {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                html_content=html_content
            )
        except Exception as e:
            logger.error(f"发送分析报告失败: {e}")
            return False
    
    def _generate_html_report(self, decisions: List[Dict], etf_list: List[Dict],
                             rotation_result: Optional[Dict] = None) -> str:
        """生成HTML格式的报告"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        html = f"""
        <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{ font-family: Arial, sans-serif; color: #333; margin: 0; padding: 0; }}
                    .container {{ max-width: 900px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #1e88e5 0%, #1565c0 100%); 
                               color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
                    .timestamp {{ color: #e3f2fd; font-size: 12px; }}
                    .section-title {{ background-color: #0d47a1; color: white; padding: 10px 15px; 
                                     border-radius: 3px; margin-top: 20px; margin-bottom: 10px; 
                                     font-size: 14px; font-weight: bold; }}
                    .etf-card {{ border: 1px solid #ddd; border-radius: 5px; margin: 10px 0; 
                                padding: 15px; background-color: #f9f9f9; }}
                    .decision-strong-buy {{ color: #d32f2f; font-weight: bold; font-size: 16px; }}
                    .decision-buy {{ color: #f57c00; font-weight: bold; font-size: 16px; }}
                    .decision-hold {{ color: #388e3c; font-weight: bold; font-size: 16px; }}
                    .decision-sell {{ color: #1976d2; font-weight: bold; font-size: 16px; }}
                    .decision-strong-sell {{ color: #6a1b9a; font-weight: bold; font-size: 16px; }}
                    .price {{ font-size: 18px; font-weight: bold; color: #d32f2f; }}
                    .indicators {{ background-color: #f5f5f5; padding: 10px; border-radius: 3px; 
                                   margin: 10px 0; font-size: 12px; }}
                    .indicator-item {{ display: inline-block; margin-right: 15px; margin-bottom: 5px; }}
                    .reasons {{ background-color: #fffacd; padding: 10px; border-left: 4px solid #ffeb3b; 
                               margin: 10px 0; font-size: 13px; }}
                    .rotation-card {{ border: 2px solid #ff9800; border-radius: 5px; margin: 10px 0; 
                                    padding: 15px; background-color: #fff3e0; }}
                    .rotation-action {{ font-weight: bold; font-size: 14px; margin: 5px 0; }}
                    .portfolio-table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
                    .portfolio-table th, .portfolio-table td {{ 
                        border: 1px solid #ddd; padding: 10px; text-align: left; }}
                    .portfolio-table th {{ background-color: #f5f5f5; font-weight: bold; }}
                    .footer {{ text-align: center; color: #999; font-size: 11px; 
                              margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; }}
                    .stats {{ display: flex; justify-content: space-around; margin: 10px 0; }}
                    .stat-item {{ text-align: center; padding: 10px; }}
                    .stat-label {{ color: #999; font-size: 12px; }}
                    .stat-value {{ font-weight: bold; font-size: 16px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>📊 ETF-Daily 智能分析报告</h1>
                        <p class="timestamp">生成时间: {timestamp}</p>
                    </div>
        """
        
        # 添加决策统计
        strong_buy = sum(1 for d in decisions if '强烈买入' in d['decision'])
        buy = sum(1 for d in decisions if d['decision'] == '买入')
        sell = sum(1 for d in decisions if d['decision'] == '卖出')
        strong_sell = sum(1 for d in decisions if '强烈卖出' in d['decision'])
        hold = len(decisions) - strong_buy - buy - sell - strong_sell
        
        html += f"""
                    <div class="stats">
                        <div class="stat-item">
                            <div class="stat-label">强烈买入</div>
                            <div class="stat-value" style="color: #d32f2f;">{strong_buy}</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-label">买入</div>
                            <div class="stat-value" style="color: #f57c00;">{buy}</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-label">持有</div>
                            <div class="stat-value" style="color: #388e3c;">{hold}</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-label">卖出</div>
                            <div class="stat-value" style="color: #1976d2;">{sell}</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-label">强烈卖出</div>
                            <div class="stat-value" style="color: #6a1b9a;">{strong_sell}</div>
                        </div>
                    </div>
        """
        
        # 添加ETF决策详情
        html += """
                    <div class="section-title">📈 个股ETF决策详情</div>
        """
        
        for decision in decisions:
            decision_class = self._get_decision_css_class(decision['decision'])
            indicators = decision.get('indicators', {})
            
            html += f"""
                    <div class="etf-card">
                        <h3>{decision['code']} - {self._get_etf_name(decision['code'], etf_list)}</h3>
                        <div class="price">当前价格: ¥{decision['price']:.2f}</div>
                        <div class="decision-{decision_class}">
                            🎯 {decision['decision']}
                        </div>
                        <p>置信度: {decision['confidence']} | 信号评分: {decision['score']}</p>
                        
                        <div class="indicators">
                            <div class="indicator-item">MA: 短{indicators.get('ma', {}).get('short', '-')} | 中{indicators.get('ma', {}).get('medium', '-')} | 长{indicators.get('ma', {}).get('long', '-')}</div>
                            <div class="indicator-item">RSI: {indicators.get('rsi', {}).get('value', '-')}</div>
                            <div class="indicator-item">MACD: {indicators.get('macd', {}).get('macd', '-')}</div>
                        </div>
                        
                        <div class="reasons">
                            <strong>分析依据:</strong><br>
            """
            
            for reason in decision.get('reasons', []):
                html += f"• {reason}<br>"
            
            html += """
                        </div>
                    </div>
            """
        
        # 添加轮动策略建议
        if rotation_result:
            html += """
                    <div class="section-title">🔄 ETF轮动策略建议</div>
            """
            
            for rec in rotation_result.get('recommendations', []):
                action_color = '#d32f2f' if '轮入' in rec['action'] else '#1976d2'
                html += f"""
                    <div class="rotation-card">
                        <h4>{rec['asset_class']} - {rec['name']} ({rec['code']})</h4>
                        <div class="rotation-action" style="color: {action_color};">
                            {rec['action']} ({rec['signal_strength']})
                        </div>
                        <p style="margin: 5px 0;">
                            <strong>动量:</strong> {rec['momentum']:.2f}% | 
                            <strong>波动率:</strong> {rec['volatility']:.2f}%
                        </p>
                        <p style="margin: 5px 0; color: #666; font-size: 12px;">
                            {rec['reason']}
                        </p>
                    </div>
                """
            
            # 添加投资组合结构
            if rotation_result.get('portfolio_structure'):
                html += """
                    <div style="margin-top: 20px;">
                        <h4>💼 建议投资组合结构</h4>
                        <table class="portfolio-table">
                            <tr>
                                <th>ETF代码</th>
                                <th>ETF名称</th>
                                <th>建议配置比例</th>
                            </tr>
                """
                
                for code, info in rotation_result['portfolio_structure'].items():
                    html += f"""
                            <tr>
                                <td>{code}</td>
                                <td>{info['name']}</td>
                                <td style="text-align: center; font-weight: bold; color: #1e88e5;">{info['weight_pct']}</td>
                            </tr>
                    """
                
                html += """
                        </table>
                    </div>
                """
        
        html += """
                    <div class="footer">
                        <p><strong>免责声明:</strong> 本报告仅供参考，不构成投资建议。投资有风险，请谨慎决策。</p>
                        <p style="margin-top: 10px;">© 2024 ETF-Daily 智能分析系统 | 基于技术面分析 + ETF轮动策略</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        return html
    
    def _get_decision_css_class(self, decision: str) -> str:
        """获取决策对应的CSS类名"""
        if '强烈买入' in decision:
            return 'strong-buy'
        elif '买入' in decision:
            return 'buy'
        elif '持有' in decision:
            return 'hold'
        elif '卖出' in decision:
            if '强烈' in decision:
                return 'strong-sell'
            return 'sell'
        return 'hold'
    
    def _get_etf_name(self, code: str, etf_list: List[Dict]) -> str:
        """根据代码获取ETF名称"""
        for etf in etf_list:
            if etf['code'] == code:
                return etf['name']
        return code
    
    def _send_email(self, subject: str, html_content: str) -> bool:
        """通过SMTP发送邮件"""
        try:
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = self.config['sender']
            message['To'] = self.config['receiver']
            
            html_part = MIMEText(html_content, 'html', 'utf-8')
            message.attach(html_part)
            
            with smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port']) as server:
                if self.config.get('use_tls', False):
                    server.starttls()
                
                server.login(self.config['sender'], self.config['password'])
                server.send_message(message)
            
            logger.info(f"✓ 邮件已发送至 {self.config['receiver']}")
            return True
        
        except Exception as e:
            logger.error(f"✗ 邮件发送失败: {e}")
            return False
    
    def send_error_notification(self, error_message: str) -> bool:
        """发送错误通知"""
        try:
            html_content = f"""
            <html>
                <head><meta charset="UTF-8"></head>
                <body>
                    <h2>⚠️ ETF-Daily 运行错误</h2>
                    <p>时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p>错误信息:</p>
                    <pre>{error_message}</pre>
                </body>
            </html>
            """
            
            return self._send_email(
                subject="⚠️ ETF-Daily 错误通知",
                html_content=html_content
            )
        except Exception as e:
            logger.error(f"发送错误通知失败: {e}")
            return False


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("邮件模块已初始化")
