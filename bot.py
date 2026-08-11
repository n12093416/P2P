from datetime import datetime, timezone, timedelta

# 한국 시간(KST) 설정
kst = timezone(timedelta(hours=9))
now = datetime.now(kst)
today_str = now.strftime("%Y년 %m월 %d일 %H:%M:%S")

# 기준 시작일
start_date = datetime(2026, 1, 1, tzinfo=kst)
days_passed = (now - start_date).days

# 웹사이트용 HTML 생성
html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>무의미한 기록 웹사이트</title>
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background-color: #0f172a;
      color: #f8fafc;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
    }}
    .card {{
      background: #1e293b;
      padding: 30px;
      border-radius: 16px;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
      text-align: center;
      max-width: 400px;
      width: 90%;
    }}
    .counter {{
      font-size: 3rem;
      font-weight: bold;
      color: #38bdf8;
      margin: 20px 0;
    }}
    .status {{
      color: #94a3b8;
      font-size: 0.95rem;
      line-height: 1.6;
    }}
  </style>
</head>
<body>
  <div class="card">
    <h2>🤖 무의미한 기록 봇</h2>
    <div class="counter">{days_passed}일째</div>
    <div class="status">
      아무 일도 일어나지 않고 있습니다.<br>
      <small>마지막 갱신: {today_str}</small>
    </div>
  </div>
</body>
</html>
"""

# index.html 파일로 저장
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"웹페이지 갱신 완료: {today_str}")
