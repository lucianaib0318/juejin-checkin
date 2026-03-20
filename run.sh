#!/bin/bash
# 掘金签到运行脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🚀 开始执行掘金签到..."
python3 src/main.py

echo ""
echo "📬 发送通知..."
python3 src/notify.py
