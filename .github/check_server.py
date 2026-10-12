#!/usr/bin/env python3
# 定时查询 MC 服务器状态并写入 server-status.json（由 GitHub Actions 运行，美国节点网络）
import json, time, urllib.request

HOST = "play2.mx16.com"
PORT = 10058
APIS = [
    "https://api.mcsrvstat.us/3/" + HOST + ":" + str(PORT),
    "https://api.mcstatus.io/v2/status/java/" + HOST + ":" + str(PORT),
    "https://mcapi.us/server/status?ip=" + HOST + "&port=" + str(PORT),
]

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "oolong-status-bot"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8", "ignore"))

result = None
for api in APIS:
    try:
        d = fetch(api)
        if not isinstance(d, dict):
            continue
        if "now" in (d.get("players") or {}):  # mcapi.us
            online = bool(d.get("online"))
            cur = (d.get("players") or {}).get("now", 0)
            mx = (d.get("players") or {}).get("max", 0)
            ver = ((d.get("server") or {}).get("name") or "") or ((d.get("version") or {}).get("name") or "")
        else:
            online = bool(d.get("online"))
            cur = (d.get("players") or {}).get("online", 0)
            mx = (d.get("players") or {}).get("max", 0)
            ver = (d.get("version") or {}).get("name_raw") or (d.get("version") or {}).get("name") or ""
        result = {"online": online, "cur": cur, "max": mx, "version": ver, "source": api}
        break
    except Exception:
        continue

out = {"ts": int(time.time()), "java": result, "bedrock": None}
with open("server-status.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(out, ensure_ascii=False))
print(json.dumps(out, ensure_ascii=False))
