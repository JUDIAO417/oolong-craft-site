#!/usr/bin/env python3
# 定时查询 MC 服务器状态并写入 server-status.json（由 GitHub Actions 运行，美国节点网络）
# 策略：多接口交叉验证，取"在线且人数最大"的结果，避免接口缓存把有人误报成 0
import json, time, urllib.request

HOST = "play2.mx16.com"
PORT = 10058
APIS = [
    "https://api.mcstatus.io/v2/status/java/" + HOST + ":" + str(PORT),
    "https://mcapi.us/server/status?ip=" + HOST + "&port=" + str(PORT),
    "https://api.mcsrvstat.us/3/" + HOST + ":" + str(PORT),
]

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "oolong-status-bot"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read().decode("utf-8", "ignore"))

def parse(d, api):
    if not isinstance(d, dict):
        return None
    players = d.get("players") or {}
    favicon = d.get("favicon") or ""
    motd = ""
    if "now" in players:  # mcapi.us
        motd = str(d.get("motd") or "")
        ver = ((d.get("server") or {}).get("name") or "") or ((d.get("version") or {}).get("name") or "")
    else:  # mcstatus.io / mcsrvstat.us
        md = d.get("motd") or {}
        if isinstance(md, dict):
            clean = md.get("clean") or []
            motd = " ".join(clean) if isinstance(clean, list) else str(clean)
        elif isinstance(md, str):
            motd = md
        ver = (d.get("version") or {}).get("name_raw") or (d.get("version") or {}).get("name") or ""
    return {
        "online": bool(d.get("online")),
        "cur": int(players.get("now", players.get("online", 0)) or 0),
        "max": int(players.get("max") or 0),
        "ver": ver,
        "favicon": favicon,
        "motd": motd,
    }

best = None
for api in APIS:
    try:
        p = parse(fetch(api), api)
    except Exception:
        continue
    if p is None:
        continue
    # 取在线且人数最大的结果（接口缓存可能滞后，避免"有人显示没人"）
    if best is None or (p["online"] and (p["cur"] > best["cur"] or not best["online"])):
        best = {"online": p["online"], "cur": p["cur"], "max": p["max"], "version": p["ver"], "favicon": p["favicon"], "motd": p["motd"], "source": api}

# 单接口缺字段时从其他接口补充：mcstatus.io 无 favicon；motd 个别情况下为空
if best:
    for k in ("favicon", "motd"):
        if best.get(k):
            continue
        for api2 in APIS:
            try:
                d2 = fetch(api2)
                if isinstance(d2, dict) and d2.get(k):
                    best[k] = d2[k]
                    break
            except Exception:
                continue

out = {"ts": int(time.time()), "java": best, "bedrock": None}
with open("server-status.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(out, ensure_ascii=False))
print(json.dumps(out, ensure_ascii=False))
