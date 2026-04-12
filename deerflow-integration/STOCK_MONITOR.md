# DeerFlow 股票监控使用指南

## 🚀 快速开始

### 1. 打开 DeerFlow Web UI
```
http://localhost:3000
```

### 2. 输入监控指令
```
监测腾讯控股、贵州茅台、阿里巴巴的实时行情和买卖信号
```

或者：

```
分析以下股票的投资机会：
- 腾讯控股 00700.HK
- 贵州茅台 600519.SH
- 阿里巴巴 09988.HK
```

### 3. 设置定时监控（可选）

在 DeerFlow 中配置定时任务：

```yaml
# 每个交易日的开盘和收盘时运行
schedule: "0 9:30,15:00 * * 1-5"
task: "分析腾讯、茅台、阿里的最新行情并给出操作建议"
```

---

## 📊 监控命令示例

### 查询实时行情
```
腾讯控股现在多少钱？
```

### 分析买卖时机
```
茅台现在适合买入吗？
```

### 新闻监测
```
搜索阿里巴巴的最新新闻并分析对股价的影响
```

### 综合分析
```
用 GLM-5 全面分析腾讯、茅台、阿里的投资价值
```

### 设置预警
```
当茅台跌破1700元时提醒我
```

---

## 🔧 定时监控脚本

### 手动运行
```bash
~/projects/deer-flow/scripts/quick_monitor.sh
```

### 设置 crontab（每30分钟）
```bash
*/30 * * * * ~/projects/deer-flow/scripts/quick_monitor.sh >> ~/stock_monitor.log 2>&1
```

### 设置 LaunchAgent（macOS）
创建 `~/Library/LaunchAgents/com.stock.monitor.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.stock.monitor</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/sunwenyong/projects/deer-flow/scripts/quick_monitor.sh</string>
    </array>
    <key>StartInterval</key>
    <integer>1800</integer> <!-- 每30分钟 -->
    <key>StandardOutPath</key>
    <string>/tmp/stock_monitor.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/stock_monitor.log</string>
</dict>
</plist>
```

加载：
```bash
launchctl load ~/Library/LaunchAgents/com.stock.monitor.plist
```

---

## 📱 飞书推送（已配置）

监控结果会自动推送到你的飞书账号！

---

## ⚠️ 免责声明

股市有风险，投资需谨慎。以上分析仅供参考，不构成投资建议。
