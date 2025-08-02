import os
import requests
from datetime import datetime, timezone

series_id = 16032  # グループID

url = "https://api.connpass.com/v2/event/"
params = {
    "series_id": series_id,
    "limit": 100
}

resp = requests.get(url, params=params)
data = resp.json()

events = data.get("data", []) if "data" in data else data.get("events", [])

# 今日の日付（タイムゾーン対応：JSTなら+09:00にする）
today_str = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d")

today_events = []
for e in events:
    # v2 APIのフィールド名: "starts_at"（ISO 8601文字列: "2025-08-02T19:00:00+09:00" など）
    start = e.get("starts_at")
    if start and start.startswith(today_str):
        today_events.append(e)

if today_events:
    message = f"**connpassグループID {series_id} の本日開催イベント**\n\n"
    for e in today_events:
        title = e.get("title")
        url = e.get("event_url")
        start = e.get("starts_at")
        place = e.get("place")
        message += f"- [{title}]({url})\n  開始: {start}\n"
        if place:
            message += f"  場所: {place}\n"
        message += "\n"
else:
    message = f"グループID {series_id} の本日開催イベントはありません！"

webhook_url = os.environ["DISCORD_WEBHOOK_URL"]
requests.post(webhook_url, json={"content": message})
