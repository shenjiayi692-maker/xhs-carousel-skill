"""白板手绘风渲染库。用法见 references/style-whiteboard.md。"""
import asyncio, os
WORK=os.environ.get('XHS_WORK','/home/claude/xhs_work')
BASE=open(os.path.join(WORK,'whiteboard_base.html'),encoding='utf-8').read()
def head(n, title, sub, pn, total):
    num = f'<span class="n">{n}</span>' if n else ''
    return f'<div class="pn">{pn}/{total}</div><h1>{num}{title}</h1><div class="sub">{sub}</div>'
def src(text):
    return f'<div class="small" style="position:absolute;left:76px;bottom:52px;width:930px;font-size:24px">{text}</div>'
async def _render(P, name):
    from playwright.async_api import async_playwright
    out=os.path.join(WORK,'out_'+name); os.makedirs(out,exist_ok=True)
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1080,'height':1440},device_scale_factor=1.5)
        pg.on('pageerror',lambda e:print('ERR',e))
        for i,(body,js) in P.items():
            html=BASE.replace('%%BODY%%',body).replace('%%JS%%',js)
            path=os.path.join(WORK,f'{name}_{i:02d}.html'); open(path,'w',encoding='utf-8').write(html)
            await pg.goto('file://'+path); await pg.wait_for_function('window.DONE===1')
            await pg.screenshot(path=f'{out}/{i:02d}.png')
        await b.close()
    print('saved to',out)
def render(P,name): asyncio.run(_render(P,name))
