#!/usr/bin/env python3
# 读取 server-status.json，生成渲染好的 status.html（iframe 直接显示，零 JS 数据请求）
import json, datetime, html

try:
    d = json.load(open("server-status.json"))
except Exception:
    d = {}

def esc(x):
    return html.escape(str(x))

j = d.get("java") if isinstance(d, dict) else None
ts_raw = d.get("ts", 0) if isinstance(d, dict) else 0
try:
    ts_str = datetime.datetime.fromtimestamp(ts_raw).strftime("%Y-%m-%d %H:%M:%S")
except Exception:
    ts_str = ""

if j is None:
    body_rows = '<div class="row"><span class="k">状态</span><span class="v">未配置服务器地址</span></div>'
else:
    if j.get("online") is True:
        body_rows = (
            '<div class="row"><span class="k">状态</span><span class="v"><span class="dot on"></span> 在线</span></div>'
            + '<div class="row"><span class="k">在线人数</span><span class="v big">%s / %s</span></div>' % (esc(j.get("cur", 0)), esc(j.get("max", 0)))
        )
        if j.get("version"):
            body_rows += '<div class="row"><span class="k">版本</span><span class="v">%s</span></div>' % esc(j["version"])
    elif j.get("online") is False:
        body_rows = '<div class="row"><span class="k">状态</span><span class="v"><span class="dot off"></span> 离线</span></div>'
    else:
        body_rows = '<div class="row"><span class="k">状态</span><span class="v"><span class="dot unk"></span> 获取失败</span></div>'

foot = ("更新于 " + ts_str + " · 每 5 分钟自动刷新") if ts_str else "状态数据由后台每 5 分钟代查"

TPL = """<!doctype html><html lang="zh"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>服务器状态</title><style>
html,body{margin:0;height:100%;background:transparent;font-family:system-ui,-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;color:#d9f2e4}
body{min-height:100%;display:flex}
.wrap{flex:1;background:linear-gradient(165deg,rgba(15,52,35,.96),rgba(9,30,22,.98));border:1px solid rgba(139,199,166,.28);border-radius:16px;padding:18px 16px 14px;box-sizing:border-box;backdrop-filter:blur(10px);box-shadow:0 12px 34px rgba(0,0,0,.42)}
.h{display:flex;align-items:baseline;gap:8px;font-size:15px;font-weight:800;margin-bottom:15px}
.h .s{font-size:11px;letter-spacing:.14em;opacity:.55}
.dot{width:12px;height:12px;border-radius:50%;display:inline-block;vertical-align:-1px}
.on{background:#3ddc84;box-shadow:0 0 12px #3ddc84}
.off{background:#ff5d5d;box-shadow:0 0 12px #ff5d5d}
.unk{background:#93a39a;box-shadow:none}
.row{display:flex;justify-content:space-between;align-items:center;padding:11px 2px;border-bottom:1px solid rgba(255,255,255,.08);font-size:14px}
.row:last-of-type{border-bottom:0}
.k{opacity:.7;font-size:12.5px}
.v{font-weight:700}
.big{font-size:24px;font-weight:800}
.foot{margin-top:13px;font-size:11px;opacity:.55;text-align:center}
</style></head><body><div class="wrap">
<div class="h"><span class="s">SERVER</span>乌龙茶的地盘</div>
__ROWS__
<div class="foot">__FOOT__</div>
</div>
<script>setTimeout(function(){location.replace(location.pathname+"?r="+Date.now())},300000);</script>
</body></html>"""

open("status.html", "w", encoding="utf-8").write(TPL.replace("__ROWS__", body_rows).replace("__FOOT__", foot))
print("status.html generated:", j)
