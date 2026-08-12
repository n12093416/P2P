import json
import os
import random
from datetime import datetime, timedelta, timezone

# 한국 시간(KST) 설정
kst = timezone(timedelta(hours=3))
now = datetime.now(kst)
today_date_str = now.strftime("%Y-%m-%d")
today_time_str = now.strftime("%Y년 %m월 %d일 %H:%M:%S")

# 시작일: 2026년 8월 11일 (1일차 기준)
start_date = datetime(2026, 8, 11, tzinfo=kst)
days_passed = (now.date() - start_date.date()).days + 1

# 기록 파일(history.json) 불러오기
history_file = "history.json"
history = []

if os.path.exists(history_file):
    try:
        with open(history_file, "r", encoding="utf-8") as f:
            history = json.load(f)
    except Exception:
        history = []

# 1일차 기록(667)이 없으면 첫 번째에 추가
if not any(item.get("day") == 1 or item.get("date") == "2026-08-11" for item in history):
    history.insert(0, {
        "day": 1,
        "date": "2026-08-11",
        "number": 667
    })

# 오늘 기록 확인 및 추가
today_entry = next((item for item in history if item.get("date") == today_date_str), None)
if not today_entry:
    current_today_num = 415 if today_date_str == "2026-08-12" else random.randint(1, 1000)
    if days_passed > 1:
        history.append({
            "day": days_passed,
            "date": today_date_str,
            "number": current_today_num
        })
else:
    current_today_num = today_entry["number"]

# 파일 영구 저장
with open(history_file, "w", encoding="utf-8") as f:
    json.dump(history, f, ensure_ascii=False, indent=2)

# 리스트 HTML 생성 (최신순)
list_rows_html = ""
for item in reversed(history):
    list_rows_html += f"""
    <div class="list-row">
      <div class="col-day">{item['day']}일차</div>
      <div class="col-date">{item['date']}</div>
      <div class="col-num"><span>🎲 {item['number']}</span></div>
    </div>
    """

# 웹사이트 HTML 생성
html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>일일 난수 아카이브</title>
  <style>
    * {{ box-sizing: border-box; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background-color: #0b0f19;
      color: #f8fafc;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      margin: 0;
      padding: 16px;
    }}
    .container {{
      background: #151d2f;
      border: 1px solid #1e293b;
      padding: 24px 20px;
      border-radius: 20px;
      box-shadow: 0 16px 36px rgba(0, 0, 0, 0.5);
      text-align: center;
      max-width: 440px;
      width: 100%;
    }}
    .title {{ font-size: 1.1rem; color: #94a3b8; font-weight: 600; margin-bottom: 2px; }}
    .days {{ font-size: 1.6rem; font-weight: 800; color: #38bdf8; margin-bottom: 12px; }}
    .today-card {{
      background: linear-gradient(145deg, #1e293b, #0f172a);
      border-radius: 14px;
      padding: 16px;
      border: 1px solid #334155;
      margin-bottom: 18px;
    }}
    .today-label {{ font-size: 0.85rem; color: #94a3b8; }}
    .today-num {{ font-size: 2.6rem; font-weight: 900; color: #fbbf24; margin-top: 4px; }}
    
    .history-box {{
      text-align: left;
      margin-top: 10px;
    }}
    .history-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
      padding: 0 4px;
    }}
    .history-title {{ font-size: 0.95rem; font-weight: 700; color: #e2e8f0; }}
    .total-count {{ font-size: 0.8rem; color: #64748b; }}
    
    .list-wrapper {{
      max-height: 240px;
      overflow-y: auto;
      background: #0d1322;
      border-radius: 12px;
      border: 1px solid #1e293b;
      padding: 6px 10px;
    }}
    .list-wrapper::-webkit-scrollbar {{ width: 6px; }}
    .list-wrapper::-webkit-scrollbar-thumb {{ background: #334155; border-radius: 4px; }}
    
    .list-row {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 10px 4px;
      border-bottom: 1px solid #1a2333;
      font-size: 0.9rem;
    }}
    .list-row:last-child {{ border-bottom: none; }}
    .col-day {{ font-weight: 700; color: #cbd5e1; width: 60px; }}
    .col-date {{ color: #64748b; font-size: 0.82rem; }}
    .col-num span {{
      background: #1e293b;
      color: #38bdf8;
      padding: 3px 8px;
      border-radius: 6px;
      font-weight: 700;
    }}
    .updated {{ margin-top: 16px; font-size: 0.75rem; color: #475569; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="title">🤖 일일 난수 기록 봇</div>
    <div class="days">{days_passed}일차</div>
    
    <div class="today-card">
      <div class="today-label">오늘의 난수 (1 ~ 1000)</div>
      <div class="today-num">{current_today_num}</div>
    </div>
    
    <div class="history-box">
      <div class="history-header">
        <span class="history-title">📜 기록 내역 (최신순)</span>
        <span class="total-count">총 {len(history)}개 누적</span>
      </div>
      <div class="list-wrapper">
        {list_rows_html}
      </div>
    </div>
    
    <div class="updated">마지막 갱신: {today_time_str}</div>
  </div>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
