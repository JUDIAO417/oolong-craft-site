/* 站点季节主题：子页跟随主页（读取同一份 sessionStorage / localStorage 记录）
   用法：在 </body> 前 <script src="assets/site-theme.js"></script> */
(function(){
  var KEY = "siteTheme";        // 主页写在 sessionStorage（同标签页共享）
  var PK  = "siteThemePersist"; // 主页额外写 localStorage（跨标签页共享）
  var OK  = {halloween:1, winter:1, girls:1, cyber:1, cosmos:1};

  function norm(v){
    v = (v || "").split("@")[0];
    if(v === "none" || v === "0") v = "";
    return OK[v] ? v : "";
  }

  function pick(){
    var m = location.search.match(/[?&]theme=([A-Za-z0-9_-]*)/);
    if(m) return norm(m[1]);
    var v = "";
    try { v = localStorage.getItem(PK) || ""; } catch(e){}
    if(!v){ try { v = sessionStorage.getItem(KEY) || ""; } catch(e){} }
    return norm(v);
  }

  function apply(t){
    var b = document.body;
    if(!b) return;
    ["halloween","winter","girls","cyber","cosmos"].forEach(function(n){ b.classList.remove(n); });
    if(t) b.classList.add(t);
  }

  var cur = pick();
  apply(cur);

  // 换页时若上一页切过主题，写回 sessionStorage，保证连续浏览一致
  try { if(cur) sessionStorage.setItem(KEY, cur + "@" + (new Date().getMonth() + 1) + "" + (new Date().getDate())); } catch(e){}

  // 特效层
  function aura(){
    if(document.querySelector(".site-aura")) return;
    var d = document.createElement("div");
    d.className = "site-aura";
    d.setAttribute("aria-hidden", "true");
    d.innerHTML = '<div class="milky"></div><div class="grid"></div>' +
                  '<div class="stars"></div><div class="stars b"></div><div class="snow"></div>';
    var b = document.body;
    if(b.firstChild) b.insertBefore(d, b.firstChild); else b.appendChild(d);
  }

  function boot(){
    aura();
    // 其它标签页切换主题时同步
    window.addEventListener("storage", function(e){
      if(e.key === PK || e.key === KEY){
        var t = pick();
        apply(t);
      }
    });
  }

  if(document.readyState === "loading"){
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
