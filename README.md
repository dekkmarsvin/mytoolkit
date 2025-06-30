# smtp_client

本專案為 Python 3.12 非同步 SMTP client，具備以下功能：
- 支援單一或多收件人寄信
- 提供寄送 log 訊息功能，根據 log level（dev, info, warn, error, critical）變更信件底色或顏色提示緊急程度
- dev 等級時，信件內容需格式化 stack trace

## 使用方式
1. 安裝相依套件：`pip install -r requirements.txt`
2. 參考 `main.py` 撰寫寄信邏輯

## 目標
- 提供簡單易用的非同步 SMTP 寄信 API
- 方便整合於自動化、監控、通知等場景
