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
favicon = (j or {}).get("favicon") or ""
motd = (j or {}).get("motd") or ""

# 头像：接口返回 favicon 用图片，否则用 SVG 占位
if favicon:
    ava = '<img class="ava" src="%s" alt="">' % esc(favicon)
else:
    ava = '<span class="ava ph"></span>'

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

desc_row = '<div class="desc"><span class="rainbow">鲍茶的地盘</span></div>'  # 简介：乌龙茶的地盘

TPL = """<!doctype html><html lang="zh"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>服务器状态</title><style>
html,body{margin:0;height:100%;background:transparent;font-family:system-ui,-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;color:#d9f2e4}
body{min-height:100%;display:flex;overflow:hidden}
.wrap{flex:1;background:linear-gradient(165deg,rgba(15,52,35,.96),rgba(9,30,22,.98));border:1px solid rgba(240,179,92,.45);border-radius:16px;padding:16px 16px 14px;box-sizing:border-box;backdrop-filter:blur(10px);box-shadow:0 12px 34px rgba(0,0,0,.42)}
.h{display:flex;align-items:center;gap:10px;margin-bottom:14px}
.ava{width:46px;height:46px;border-radius:10px;image-rendering:pixelated;background:rgba(255,255,255,.08);border:1px solid rgba(139,199,166,.3);flex:0 0 auto}
.ava.ph{width:46px;height:46px;border-radius:10px;background:linear-gradient(145deg,#3d6b4f,#1f3b2b);display:inline-block;flex:0 0 auto}
.nm{font-size:15px;font-weight:800;line-height:1.3}
.nm .s{display:block;font-size:10px;letter-spacing:.16em;opacity:.5;font-weight:600}
.dot{width:12px;height:12px;border-radius:50%;display:inline-block;vertical-align:-1px}
.on{background:#3ddc84;box-shadow:0 0 12px #3ddc84}
.off{background:#ff5d5d;box-shadow:0 0 12px #ff5d5d}
.unk{background:#93a39a;box-shadow:none}
.row{display:flex;justify-content:space-between;align-items:center;padding:11px 2px;border-bottom:1px solid rgba(255,255,255,.08);font-size:14px}
.row:last-of-type{border-bottom:0}
.k{opacity:.7;font-size:12.5px}
.v{font-weight:700}
.big{font-size:24px;font-weight:800}
.desc{margin-top:12px;padding:10px 12px;background:rgba(240,179,92,.07);border:1px solid rgba(240,179,92,.3);border-radius:10px;font-size:15px;line-height:1.55;text-align:center}
.rainbow{background:linear-gradient(90deg,#ff6b6b,#ffb86b,#ffe66b,#6bff9e,#6bb7ff,#c56bff,#ff6b6b);background-size:200% auto;-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;color:transparent;font-weight:800;animation:rain 3.5s linear infinite}
@keyframes rain{to{background-position:200% center}}
</style></head><body><div class="wrap">
<div class="h">__AVA__<span class="nm"><span class="s">SERVER</span>乌龙茶的地盘</span></div>
__ROWS____DESC__
</div>
<script>setTimeout(function(){location.replace(location.pathname+"?r="+Date.now())},300000);</script>
</body></html>"""

open("status.html", "w", encoding="utf-8").write(
    TPL.replace("__AVA__", ava).replace("__ROWS__", body_rows).replace("__DESC__", desc_row)
)
print("status.html generated, favicon:", bool(favicon), "motd:", motd)
