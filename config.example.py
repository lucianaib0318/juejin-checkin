# 掘金签到配置文件
# 复制此文件为 config.py 并填写你的真实信息

# ============= 必填配置 =============

# Cookie 信息（从浏览器开发者工具获取）
# 获取方法：
# 1. 打开 https://juejin.cn/ 并登录
# 2. 按 F12 打开开发者工具
# 3. 刷新页面，找到任意请求
# 4. 复制 Request Headers 中的 Cookie 字段
COOKIE = ""

# 请求参数（一般不需要修改）
AID = "2608"
UUID = "YOUR_UUID_HERE"  # 从浏览器请求中获取
SPIDER = "0"
MS_TOKEN = "YOUR_MS_TOKEN_HERE"  # 从浏览器请求中获取
A_BOGUS = "YOUR_A_BOGUS_HERE"  # 从浏览器请求中获取

# ============= 可选配置 =============

# 通知方式（后续可扩展）
# - feishu: 飞书 webhook
# - telegram: Telegram Bot
# - wechat: 企业微信
NOTIFY_METHOD = "feishu"

# Webhook URL（如使用飞书/钉钉通知）
WEBHOOK_URL = "YOUR_WEBHOOK_URL_HERE"
