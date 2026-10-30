"""文章风渲染器。用法：python3 render_article.py spec.json 输出目录名
spec 格式见 references/style-article.md。每页会打印内容底部位置，>1290 说明溢出，要删字或拆页。"""
import asyncio, json, os, sys, html as H
WORK=os.environ.get('XHS_WORK','/home/claude/xhs_work')
F=f'file://{WORK}/fonts'
FONTS=f'''@font-face{{font-family:SR;src:url({F}/NotoSerifSC-Regular.otf)}}@font-face{{font-family:SB;src:url({F}/NotoSerifSC-Bold.otf)}}
@font-face{{font-family:NR;src:url({F}/NotoSansSC-Regular.otf)}}@font-face{{font-family:NBd;src:url({F}/NotoSansSC-Bold.otf)}}@font-face{{font-family:NB;src:url({F}/NotoSansSC-Black.otf)}}'''
ART_CSS='''*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1440px;overflow:hidden;background:#F7F6F2;color:#222;font-family:SR}
.pg{position:absolute;left:92px;right:92px;top:96px}
h1{font-family:SB;font-size:60px;line-height:1.36;color:#1a1a1a}
.ul{width:72px;height:6px;background:var(--acc);margin:26px 0 34px}
.au{display:flex;align-items:center;gap:22px;margin-bottom:44px}.au .n{font-size:34px;color:#333}.au .d{font-size:25px;color:#999;margin-top:2px}
p{font-size:36px;line-height:1.9;margin-bottom:30px}
b{font-family:SB;color:var(--acc);font-weight:normal}
.h2{border-left:9px solid var(--acc);padding-left:22px;font-family:SB;font-size:42px;line-height:1.35;color:var(--acc);margin-bottom:34px}
.q{font-family:SB;font-size:33px;line-height:1.85;color:#1a1a1a;background:#EFEDE6;padding:28px 34px;border-radius:12px;margin-bottom:34px}
.dot{font-family:SB;color:var(--acc)}
s{color:#999;text-decoration-color:#B5483A;text-decoration-thickness:3px}
.tip{font-size:30px;color:#7A7468;border-top:1.5px dashed #DDD9CF;padding-top:22px}
.im{border-radius:14px;overflow:hidden;margin-bottom:34px;border:1.5px solid #E6E2D8}.im img{display:block;width:100%}
.foot{position:absolute;left:92px;right:92px;bottom:72px;border-top:1.5px solid #DDD9CF;padding-top:22px;display:flex;justify-content:space-between;align-items:center}
.foot .l{font-size:24px;color:#A08F70}.foot .r{font-family:NBd;font-size:30px;color:var(--acc)}'''
TW_CSS='''*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1440px;overflow:hidden;background:#FFFFFF;color:#111;font-family:NR}
.pg{position:absolute;left:60px;right:60px;top:56px}
.hd{display:flex;align-items:center;gap:26px;margin-bottom:46px}.hd .n{font-family:NBd;font-size:46px}.hd .h{font-size:34px;color:#8B98A5;margin-top:4px}
.more{position:absolute;right:0;top:20px;font-size:40px;color:#8B98A5;letter-spacing:4px}
p{font-size:40px;line-height:1.7;margin-bottom:36px}
b{font-family:NBd;font-weight:normal}
.card{border-radius:22px;overflow:hidden;border:1.5px solid #E6E8EB;margin-bottom:42px}
.card .ch{background:#F4F5F7;padding:22px 32px;font-size:28px;color:#8B98A5;border-bottom:1.5px solid #E6E8EB}
.card .cb{padding:30px 32px;font-family:Menlo,monospace;font-size:31px;line-height:1.7;color:#24292F;background:#FAFBFC}
.card img{display:block;width:100%}
mark{background:#FFF1A8;color:inherit}'''
def doc(css,body,acc):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}:root{{--acc:{acc}}}{css}</style></head><body>{body}</body></html>'
def av(src,s,name='?'):
    if src and os.path.exists(src):
        return f'<img src="file://{src}" style="width:{s}px;height:{s}px;border-radius:50%;object-fit:cover;flex:none">'
    ini=H.escape((name or '?').strip()[:1])  # 没有头像时，用名字首字做圆形占位
    return f'<div style="width:{s}px;height:{s}px;border-radius:50%;background:#1E4D5C;color:#fff;display:flex;align-items:center;justify-content:center;font-family:NBd;font-size:{int(s*0.42)}px;flex:none">{ini}</div>'
def block(b,S):
    k,v=next(iter(b.items()))
    if k=='h1': return f'<h1>{v}</h1><div class="ul"></div>'
    if k=='author': return f'<div class="au">{av(S["avatar"],84,S["name"])}<div><div class="n">{S["name"]}</div><div class="d">{S["date"]}</div></div></div>'
    if k=='h2': return f'<div class="h2">{v}</div>'
    if k=='p': return f'<p>{v}</p>'
    if k=='quote': return f'<div class="q">“{v}”</div>'
    if k=='bullets': return '<p>'+'<br>'.join(f'<span class="dot">•</span> {x}' for x in v)+'</p>'
    if k=='numbered': return '<p>'+'<br>'.join(f'<span class="dot">{i+1}.</span> {x}' for i,x in enumerate(v))+'</p>'
    if k=='example': return f'<p style="margin-bottom:8px"><s>{v[0]}</s></p><p><span class="dot">→</span> {v[1]}</p>'
    if k=='tip': return f'<p class="tip">小提醒：{v}</p>'
    if k=='img': return f'<div class="im"><img src="file://{os.path.abspath(v)}"></div>'
    if k=='code': return f'<div class="card"><div class="ch">{v.get("header","")}</div><div class="cb">{v["text"]}</div></div>'
    if k=='card_img': return f'<div class="card"><img src="file://{os.path.abspath(v)}"></div>'
    if k=='html': return v
    raise ValueError('unknown block '+k)
def page(pg,n,total,S):
    acc=S.get('accent','#1E4D5C')
    if pg['type']=='tweet':
        body=f'<div class="pg"><div class="hd">{av(S["avatar"],128,S["name"])}<div><div class="n">{S["name"]}</div><div class="h">{S["handle"]}</div></div></div><div class="more">···</div>'+''.join(block(b,S) for b in pg['blocks'])+'</div>'
        return doc(TW_CSS,body,acc)
    body='<div class="pg">'+''.join(block(b,S) for b in pg['blocks'])+f'</div><div class="foot"><span class="l">{S["title_short"]}</span><span class="r">{n} / {total}</span></div>'
    return doc(ART_CSS,body,acc)
async def main(spec_path,name):
    from playwright.async_api import async_playwright
    spec=json.load(open(spec_path,encoding='utf-8'))
    cfg_path=os.path.join(WORK,'account.json')
    cfg=json.load(open(cfg_path,encoding='utf-8')) if os.path.exists(cfg_path) else {}
    acct={**cfg,**spec.get('account',{})}
    av_path=acct.get('avatar') or ''
    S={'name':acct.get('name','你的账号名'),'handle':acct.get('handle','@your_handle'),'avatar':os.path.abspath(av_path) if av_path else '',
       'date':spec.get('date',''),'title_short':spec.get('title_short',''),'accent':spec.get('accent',acct.get('accent','#1E4D5C'))}
    out=os.path.join(WORK,'out_'+name); os.makedirs(out,exist_ok=True); tmp=os.path.join(WORK,'pages_'+name); os.makedirs(tmp,exist_ok=True)
    pages=spec['pages']; total=len(pages)
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1080,'height':1440},device_scale_factor=1.5)
        for i,pgspec in enumerate(pages,1):
            f=os.path.join(tmp,f'{i:02d}.html'); open(f,'w',encoding='utf-8').write(page(pgspec,i,total,S))
            await pg.goto('file://'+f); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
            h=await pg.evaluate("(()=>{const e=[...document.querySelectorAll('.pg > *')];return e.length?Math.max(...e.map(x=>x.getBoundingClientRect().bottom)):0})()")
            flag='  <-- 溢出，删字或拆页' if h>1290 else ('  <-- 偏空，可加内容' if 0<h<1000 and pgspec['type']=='article' else '')
            print(f'{i:02d} {pgspec["type"]:8s} 内容底部 {int(h)}{flag}')
            await pg.screenshot(path=os.path.join(out,f'{i:02d}.png'))
        await b.close()
    print('saved to',out)
if __name__=='__main__':
    asyncio.run(main(sys.argv[1],sys.argv[2] if len(sys.argv)>2 else 'post'))
