# ETF-Daily 分析决策工具

A股主要ETF品种的自动分析和决策工具，每天下午3点10分生成分析结论和操作建议，通过邮件发送。

## 功能特性

- ✅ 自动获取A股主要ETF实时数据
- ✅ 多维度技术分析（趋势、动量、支撑阻力）
- ✅ 基本面数据整合
- ✅ 智能生成交易决策（买入/持有/卖出）
- ✅ 每日3点10分定时执行
- ✅ 邮件自动推送分析结论

## 监控品种

| 代码 | 名称 | 类型 |
|------|------|------|
| 510050 | 上证50 | 蓝筹 |
| 510300 | 沪深300 | 宽基 |
| 510500 | 中证500 | 中盘 |
| 159915 | 创业板ETF | 成长 |
| 588000 | 科创板50 | 科技 |
| 159928 | 消费ETF | 消费 |
| 159929 | 医药ETF | 医药 |
| 510880 | 红利ETF | 价值 |

## 项目结构

```
ETF-Daily/
├── data/              # 数据存储
├── src/
│   ├── fetcher.py     # 数据获取模块
│   ├── analyzer.py    # 分析引擎
│   ├── decision.py    # 决策系统
│   └── mailer.py      # 邮件发送
├── config.yaml        # 配置文件
├── requirements.txt   # 依赖
├── main.py           # 主程序入口
└── .github/
    └── workflows/
        └── etf-daily.yml  # GitHub Actions定时任务
```

## 快速开始

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
编辑 `config.yaml`，设置邮件和ETF品种参数

### 4. 本地测试
```bash
python main.py
```

### 5. GitHub Actions 自动运行
在仓库 Settings → Secrets 中配置：
- `EMAIL_SENDER`: 发送邮箱
- `EMAIL_PASSWORD`: 邮箱授权码  
- `EMAIL_RECEIVER`: 接收邮箱

工作流将每天下午3点10分自动执行

## 配置说明

编辑 `config.yaml` 自定义：
- ETF品种列表
- 技术指标参数
- 分析周期
- 邮件模板

## 技术栈

- Python 3.8+
- yfinance / akshare (数据获取)
- pandas / numpy (数据处理)
- talib (技术分析)
- GitHub Actions (定时任务)

## 许可证

MIT
