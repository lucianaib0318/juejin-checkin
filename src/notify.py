#!/usr/bin/env python3
"""
读取掘金签到结果并发送通知
支持飞书、Telegram、企业微信等通知方式
"""
import json
import os
import sys
import requests

def send_feishu(webhook_url, report):
    """发送飞书通知"""
    payload = {
        "msg_type": "text",
        "content": {
            "text": f"📊 掘金签到报告\n\n{report}"
        }
    }
    response = requests.post(webhook_url, json=payload)
    return response.status_code == 200

def send_telegram(bot_token, chat_id, report):
    """发送 Telegram 通知"""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": f"📊 掘金签到报告\n\n{report}"
    }
    response = requests.post(url, json=payload)
    return response.status_code == 200

def send_wechat(webhook_url, report):
    """发送企业微信通知"""
    payload = {
        "msgtype": "text",
        "text": {
            "content": f"📊 掘金签到报告\n\n{report}"
        }
    }
    response = requests.post(webhook_url, json=payload)
    return response.status_code == 200

def main():
    result_file = os.path.join(os.path.dirname(__file__), 'src', 'last_result.json')
    
    if not os.path.exists(result_file):
        print("错误：结果文件不存在，请先运行签到脚本")
        sys.exit(1)
    
    with open(result_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    report = data.get('report', '无报告内容')
    
    # 从配置读取通知方式
    try:
        from config import NOTIFY_METHOD, WEBHOOK_URL
    except ImportError:
        print("未配置通知方式，仅输出结果")
        print(report)
        return
    
    # 发送通知
    success = False
    if NOTIFY_METHOD == "feishu":
        success = send_feishu(WEBHOOK_URL, report)
    elif NOTIFY_METHOD == "telegram":
        try:
            from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
            success = send_telegram(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, report)
        except ImportError:
            print("Telegram 配置不完整")
    elif NOTIFY_METHOD == "wechat":
        success = send_wechat(WEBHOOK_URL, report)
    else:
        print(f"不支持的通知方式：{NOTIFY_METHOD}")
        print(report)
        return
    
    if success:
        print("✅ 通知已发送")
    else:
        print("❌ 通知发送失败")

if __name__ == "__main__":
    main()
