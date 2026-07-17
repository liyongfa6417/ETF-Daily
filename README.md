# ETF-Daily 分析决策工具

A股主要ETF品种的自动分析和决策工具，每天下午3点10分生成分析结论和操作建议，通过邮件发送。

## 🎯 核心功能

### 1. 技术面分析
- ✅ 5日/20日/60日均线分析
- ✅ RSI 相对强弱指数
- ✅ MACD 趋势指标
- ✅ 布林带 波动性分析
- ✅ ATR 波动率指标

### 2. 交易决策系统
- ✅ 综合信号评分 (-1 ~ 1)
- ✅ 5档决策建议（强烈买入/买入/持有/卖出/强烈卖出）
- ✅ 置信度评估
- ✅ 详细理由说明

### 3. 🔄 ETF轮动策略 (新增！)
参考 https://www.etfwin.com/etf-rotation/guide

**核心思想：**
- 监测多个资产类别的相对强弱
- 根据动量指标选择表现最好的资产
- 定期轮动调整持仓
- 智能风险管理

**资产类别分组：**
- 股票型：上证50、沪深300、中证500、创业板、科创板50
- 消费医药：消费ETF、医药ETF
- 价值：红利ETF

**轮动指标：**
- 多周期加权动量（5日50%、20日30%、60日20%）
- 相对强弱（相对沪深300的超额收益）
- 年化波动率（风险评估）

### 4. 邮件推送
- ✅ 美观的HTML格式报告
- ✅ 包含技术面决策和轮动策略建议
- ✅ 投资组合结构推荐
- ✅ 实时价格和指标
- ✅ 每日下午3:10分自动发送

## 📊 监控品种

| 代码 | 名称 | 类型 | 资产类别 |
|------|------|------|--------|
| 510050 | 上证50 | 蓝筹 | 股票型 |
| 510300 | 沪深300 | 宽基 | 股票型 |
| 510500 | 中证500 | 中盘 | 股票型 |
| 159915 | 创业板ETF | 成长 | 股票型 |
| 588000 | 科创板50 | 科技 | 股票型 |
| 159928 | 消费ETF | 消费 | 消费医药 |
| 159929 | 医药ETF | 医药 | 消费医药 |
| 510880 | 红利ETF | 价值 | 价值 |

## 📁 项目结构

```
ETF-Daily/
├── data/                  # 数据存储
├── logs/                  # 日志输出
├── src/
│   ├── fetcher.py         # 数据获取（yfinance/akshare）
│   ├── analyzer.py        # 技术分析引擎
│   ├── decision.py        # 交易决策系统
│   ├── rotation.py        # ETF轮动策略 (NEW!)
│   └── mailer.py          # 邮件发送（HTML格式）
├── config.yaml            # 配置文件
├── requirements.txt       # 项目依赖
├── main.py               # 主程序入口
└── .github/
    └── workflows/
        └── etf-daily.yml  # GitHub Actions定时任务
```

## 🚀 快速开始

### 1. 克隆项目
```bash
git clone https://github.com/liyongfa6417/ETF-Daily.git
cd ETF-Daily
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置环境

#### 本地测试
编辑 `config.yaml` 配置参数：
```yaml
email:
  sender: your_email@qq.com
  password: your_auth_code
  receiver: receiver@qq.com
```

#### GitHub Actions 自动运行
在仓库 **Settings → Secrets and variables → Actions** 中添加：
- `EMAIL_SENDER`: 发送邮箱
- `EMAIL_PASSWORD`: 邮箱授权码（QQ邮箱需生成应用专用密码）
- `EMAIL_RECEIVER`: 接收邮箱

### 4. 运行分析

**本地运行：**
```bash
python main.py
```

**自动化运行：**
工作流会每天下午3:10分（北京时间）自动执行 ⏰

## 📧 邮件报告内容

### 个股ETF决策
- 📈 当前价格实时显示
- 🎯 交易决策建议（5档）
- 📊 技术指标详解
- 💡 分析依据说明

### ETF轮动策略
- 🔄 资产类别最强者识别
- ⚡ 动量指标评分
- 📉 波动率风险评估
- 💼 投资组合结构推荐���50%股票型 + 30%消费医药 + 20%价值）

## ⚙️ 配置说明

编辑 `config.yaml` 自定义：

### 邮件配置
```yaml
email:
  sender: 发送邮箱
  password: 邮箱授权码
  receiver: 接收邮箱
  smtp_server: "smtp.qq.com"  # QQ邮箱
  smtp_port: 587
  use_tls: true
```

### 技术指标参数
```yaml
technical:
  ma_short: 5        # 短期均线
  ma_medium: 20      # 中期均线
  ma_long: 60        # 长期均线
  rsi_period: 14     # RSI周期
  macd_fast: 12      # MACD快线
  macd_slow: 26      # MACD慢线
  bb_period: 20      # 布林带周期
```

### 决策阈值
```yaml
decision:
  strong_buy_threshold: 0.8      # 强烈买入
  buy_threshold: 0.6             # 买入
  strong_sell_threshold: -0.8    # 强烈卖出
  sell_threshold: -0.6           # 卖出
```

## 🔧 技术栈

- **Python** 3.8+
- **Data Fetching**: yfinance / akshare
- **Data Processing**: pandas / numpy
- **Technical Analysis**: talib
- **Scheduling**: GitHub Actions
- **Notification**: SMTP Email

## 📈 工作流程

```
1. 数据获取 (akshare/yfinance)
   ↓
2. 技术分析 (MA, RSI, MACD, BB, ATR)
   ↓
3. 交易决策 (综合信号评分)
   ↓
4. 轮动策略 (资产类别轮动 + 动量选择)
   ↓
5. 生成报告 (HTML格式)
   ↓
6. 邮件推送 (SMTP)
```

## 📝 日志

所有运行日志保存在 `logs/etf-daily.log`

查看最新日志：
```bash
tail -f logs/etf-daily.log
```

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

改进方向：
- [ ] 支持更多ETF品种
- [ ] 集成实时数据推送
- [ ] Web 界面展示
- [ ] 历史回测功能
- [ ] 量化指标优化

## ⚠️ 免责声明

本工具仅供学习和参考，**不构成投资建议**。

- 投资有风险，请谨慎决策
- 历史表现不代表未来收益
- 市场瞬息万变，策略需要持续优化

## 📄 许可证

MIT License

---

**最后更新：** 2024-07-17

**版本：** 2.0 (支持ETF轮动策略)

**需要帮助？** 提交 Issue 或联系作者
