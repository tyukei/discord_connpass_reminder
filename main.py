import os
import requests
import datetime


url = "https://connpass.com/api/v1/event/"
params = {
    "keyword": "LLMCraft",
    "count": 5
}
resp = requests.get(url, params=params).json()

# 近日開催イベントを抽出
now = datetime.datetime.now()
remind_events = [
    e for e in resp["events"]
    if 0 < (datetime.datetime.strptime(e["started_at"][:19], "%Y-%m-%dT%H:%M:%S") - now).days <= 2
]

if remind_events:
    message = "近日開催のconnpassイベント！\n"
    for e in remind_events:
        message += f'{e["title"]}\n{e["event_url"]}\n{e["started_at"]}\n\n'
    # Discord webhookで通知
    webhook_url = os.environ["DISCORD_WEBHOOK_URL"]
    requests.post(webhook_url, json={"content": message})
