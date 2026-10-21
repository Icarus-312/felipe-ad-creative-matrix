#!/usr/bin/env python3
"""Render niches.json -> index.html (single file, no deps). Usage: build.py <project_dir>"""
import json, sys, html, pathlib

d = pathlib.Path(sys.argv[1])
data = json.loads((d / "niches.json").read_text())
for n in data["niches"]:
    assert len(n["hooks"]) == 10, f'{n["name"]}: need 10 hooks, got {len(n["hooks"])}'
    assert len(n["bodies"]) == 2, f'{n["name"]}: need 2 bodies, got {len(n["bodies"])}'
blob = json.dumps(data).replace("</", "<\\/")
title = html.escape(data["business"])

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>__TITLE__ Ad Scripts</title>
<style>
:root{--bg:#f6f5f2;--card:#fff;--ink:#17171a;--mute:#6b6b73;--line:#e3e1dc;--acc:#1f3a5f;--acc-ink:#fff}
@media(prefers-color-scheme:dark){:root{--bg:#121214;--card:#1b1b1f;--ink:#f1f0ec;--mute:#9a9aa3;--line:#2c2c32;--acc:#7aa2d6;--acc-ink:#0d1520}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
main{max-width:760px;margin:0 auto;padding:32px 16px 80px}
h1{font-size:28px;margin:0 0 4px}.sub{color:var(--mute);margin:0 0 28px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px;text-align:left;cursor:pointer;color:inherit;font:inherit}
.card:hover{border-color:var(--acc)}.card b{display:block;font-size:18px}.card span{color:var(--mute);font-size:14px}
.back{background:none;border:0;color:var(--acc);cursor:pointer;font:inherit;padding:0;margin-bottom:16px}
details{background:var(--card);border:1px solid var(--line);border-radius:12px;margin-bottom:12px}
summary{padding:16px 18px;font-weight:600;cursor:pointer}
.item{display:flex;gap:12px;align-items:flex-start;padding:12px 18px;border-top:1px solid var(--line)}
.item p{margin:0;flex:1;white-space:pre-wrap}.n{color:var(--mute);min-width:22px}
.cp{background:var(--acc);color:var(--acc-ink);border:0;border-radius:8px;padding:6px 12px;font:inherit;font-size:14px;cursor:pointer}
</style></head><body><main id="app"></main>
<script>
const D=__DATA__;const app=document.getElementById('app');
const esc=s=>s.replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function item(t,i){return `<div class="item">${i?`<span class="n">${i}</span>`:''}<p>${esc(t)}</p><button class="cp" data-t="${esc(t)}">Copy</button></div>`}
function home(){app.innerHTML=`<h1>${esc(D.business)}</h1><p class="sub">Pick a niche. Hooks, bodies and CTA for each.</p><div class="grid">${D.niches.map((n,i)=>`<button class="card" data-i="${i}"><b>${esc(n.name)}</b><span>10 hooks, 2 bodies</span></button>`).join('')}</div>`}
function niche(i){const n=D.niches[i];app.innerHTML=`<button class="back" id="back">Back to niches</button><h1>${esc(n.name)}</h1><p class="sub">${esc(D.offer)}</p>
<details open><summary>10 Hooks</summary>${n.hooks.map((h,k)=>item(h,k+1)).join('')}</details>
<details><summary>2 Bodies</summary>${n.bodies.map((b,k)=>item(b,k+1)).join('')}</details>
<details><summary>CTA</summary>${item(D.cta)}</details>`;document.getElementById('back').onclick=()=>{location.hash=''}}
function route(){const m=location.hash.match(/^#n(\\d+)$/);m&&D.niches[+m[1]]?niche(+m[1]):home();scrollTo(0,0)}
app.addEventListener('click',e=>{const c=e.target.closest('.card');if(c){location.hash='n'+c.dataset.i;return}
const b=e.target.closest('.cp');if(b){navigator.clipboard.writeText(b.dataset.t).then(()=>{b.textContent='Copied';setTimeout(()=>b.textContent='Copy',1200)})}});
addEventListener('hashchange',route);route();
</script></body></html>"""
(d / "index.html").write_text(PAGE.replace("__DATA__", blob).replace("__TITLE__", title))
print(f"built {d/'index.html'} ({len(data['niches'])} niches)")
