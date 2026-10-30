from wb_lib import head, src, render
def shot(f,x,y,w,rot=0):
    return (f'<figure class="shot" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg)"><img src="img/{f}">'
            f'<i class="tape" style="left:{w*0.1}px;top:-18px;transform:rotate(-5deg)"></i><i class="tape" style="right:12px;bottom:-18px;transform:rotate(6deg)"></i></figure>')
def box(lines,top,label='',fill=True,left=76,width=928,size=33):
    f='data-fill="#FFF3A8" data-fs="solid"' if fill else ''
    lab=f'<p style="font-size:26px;color:var(--soft)">{label}</p>' if label else ''
    return (f'<div style="position:absolute;left:{left}px;top:{top}px;width:{width}px"><div class="rbx" {f} style="padding:22px 32px">{lab}'
            + ''.join(f'<p style="font-size:{size}px;line-height:1.55;margin-top:6px">{l}</p>' for l in lines) + '</div></div>')
def at(top,html,left=76,width=930):
    return f'<div style="position:absolute;left:{left}px;top:{top}px;width:{width}px">{html}</div>'
def p(t,size=38,cls='',mt=0,lh=1.6): return f'<p class="{cls}" style="font-size:{size}px;line-height:{lh};margin-top:{mt}px">{t}</p>'
def cover(series,title,sub):
    return (f'<div style="margin-top:30px;font-size:40px;color:var(--soft);font-weight:300">{series}</div>'
            f'<div style="font-size:96px;line-height:1.2;margin-top:24px">{title}</div><div style="font-size:42px;margin-top:30px;line-height:1.5">{sub}</div>')
def end(n,T,lines,q):
    return (f'<div class="pn">{n}/{T}</div>'+at(160,p(lines,56,lh=1.5))+at(900,p(q,44,lh=1.5)))
SER=''

def card(html,top,left=76,width=928,fill='#FFF3A8',c='',pad='22px 30px'):
    cc=f'data-c="{c}"' if c else ''
    return f'<div style="position:absolute;left:{left}px;top:{top}px;width:{width}px"><div class="rbx" {cc} data-fill="{fill}" data-fs="solid" style="padding:{pad}">{html}</div></div>'
def chip(t,color='var(--red)'):
    return f'<span style="display:inline-block;font-size:26px;color:#fff;background:{color};padding:2px 12px;margin-right:14px;transform:rotate(-2deg)">{t}</span>'
def table(rows,top,cols,size=30,head_=None):
    h=''
    if head_: h='<div style="display:flex;padding:10px 0;border-bottom:3px solid var(--ink)">'+''.join(f'<div style="width:{w}px;font-size:{size-4}px;color:var(--soft)">{t}</div>' for t,w in zip(head_,cols))+'</div>'
    body=''.join('<div style="display:flex;padding:12px 0;border-bottom:2px dashed #C9D2DF">'+''.join(f'<div style="width:{w}px;font-size:{size}px;line-height:1.45;{"color:var(--red);" if i==0 else ""}padding-right:12px">{t}</div>' for i,(t,w) in enumerate(zip(r,cols)))+'</div>' for r in rows)
    return at(top,h+body)
LB='#E3EAF5';LR='#FBE1DC';LG='#E6EFD8';LY='#FFF3A8'
