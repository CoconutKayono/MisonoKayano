"""Build the offline reader: python -m pip install markdown; python build_reader.py."""
from pathlib import Path
import json, re, html
import markdown

ROOT=Path(__file__).resolve().parent
files=[ROOT/'00-系列总计划与目录.md',ROOT/'从零开始学板绘：画出喜欢的洛琪希.md']+sorted(p for p in ROOT.glob('*.md') if re.match(r'(0[1-9]|[1-9][0-9])-',p.name))
mapping={p.name:('plan' if p.name.startswith('00-') else 'lesson-'+p.name[:2] if re.match(r'\d\d-',p.name) else 'guide') for p in files}
lessons=[]
for p in files:
    source=p.read_text(encoding='utf-8'); number=int(p.name[:2]) if re.match(r'\d\d-',p.name) and not p.name.startswith('00-') else None
    markup=markdown.markdown(source,extensions=['tables','fenced_code','toc','sane_lists'])
    for name,id in mapping.items():
        markup=markup.replace('href="'+html.escape(name,quote=True)+'"','href="#'+id+'"')
    markup=re.sub(r'href="index\.html(?:#([^"]+))?"',lambda m:'href="#'+(m[1] or 'home')+'"',markup)
    # Source heading anchors belong to the currently displayed lesson.
    id=mapping[p.name]
    markup=re.sub(r'href="#([^"]+)"',lambda m:m[0] if m[1] in mapping.values() or m[1]=='home' else f'href="#{id}/{m[1]}"',markup)
    short=p.stem[3:] if number else ('系列总计划与目录' if id=='plan' else '板绘入门总指南')
    lessons.append(dict(id=id,number=number,short=short,file=p.name,html=markup,text=source))
payload=json.dumps(lessons,ensure_ascii=False).replace('<','\\u003c').replace('\u2028','\\u2028').replace('\u2029','\\u2029')
shell='''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>从零开始学绘画 · 图文练习册</title><meta name="description" content="面向零基础的二次元板绘图文教程，一课一个小问题。"><link rel="stylesheet" href="reader.css"></head>
<body><a href="#main" class="skip" onclick="document.getElementById('main').focus();return false">跳到正文</a><aside class="sidebar" id="sidebar"><a class="brand" href="#home">绘画小练习</a><p class="tagline">从零开始，画出喜欢的角色。<br>一课一小步，慢慢看见变化。</p><label class="search-label" for="search">查找想学的小问题</label><input id="search" type="search" placeholder="试试：下巴、虹膜、眨眼" autocomplete="off"><p id="search-status" role="status" aria-live="polite"></p><nav id="nav" aria-label="教程目录"></nav><p class="storage-note" id="storage"></p></aside>
<div class="layout"><header class="topbar"><button id="menu" aria-controls="sidebar" aria-expanded="false">目录</button><p>板绘图文练习册 · 24 课已完成编写</p><div class="top-actions"><span id="progress"></span><button class="small-button" id="font" aria-label="切换正文字号">字号 A</button><button class="small-button" id="print">打印</button></div></header><div class="reader-grid"><div><p class="breadcrumb" id="crumb"></p><main id="main" tabindex="-1"></main></div><aside class="aside" id="aside"><h2>这一课的内容</h2><nav id="toc" aria-label="本课小节"></nav><a class="source" id="source"></a></aside></div></div>
<dialog id="lightbox" class="lightbox" aria-labelledby="image-label"><header><span id="image-label"></span><div><button id="zoom">查看原始尺寸</button> <button id="close-image" aria-label="关闭放大图片">关闭 ×</button></div></header><div class="image-scroll"><img id="full-image" alt=""></div></dialog>
<noscript><p>请允许浏览器运行本地 JavaScript 以使用阅读目录。也可以直接打开同文件夹中的 Markdown 源稿。</p></noscript><script type="application/json" id="lesson-data">PAYLOAD</script><script src="reader.js"></script></body></html>'''
(ROOT/'index.html').write_text(shell.replace('PAYLOAD',payload),encoding='utf-8')
print(f'Built offline index.html with {len(lessons)} documents; no fetch or CDN dependencies.')
