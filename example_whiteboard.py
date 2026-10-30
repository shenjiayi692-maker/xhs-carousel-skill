# 白板手绘风示例：在 $XHS_WORK 下运行  python3 example_whiteboard.py
from wb_helpers import *
T=2; P={}
P[1]=('<div style="margin-top:30px;font-size:42px;color:var(--soft);font-weight:300">提示词小技巧</div>'
 '<div style="font-size:96px;line-height:1.2;margin-top:24px">让 AI 少说废话<br><span class="red">3 句就够</span></div>'
 + card('<p style="font-size:30px;color:var(--soft)">✗ 模型只能瞎猜</p><p style="font-size:44px;margin-top:6px" class="rstrike">写得高级一点</p>',520,fill='#FFFFFF')
 + card('<p style="font-size:30px;color:var(--red)">✓ 写清楚要什么</p>'+p('先给结论，再给理由。<br>每段只讲一个意思。<br>不用“总而言之”收尾。',40,mt=10,lh=1.7),760,fill=LY),'')
P[2]=(head('①','改什么、留什么，分开写','最常用的一个写法',2,T)
 + table([['只修改','你要改的那一处'],['必须保留','身份、构图、数字、原文观点'],['允许跟着变','必要的阴影、语气、衔接']],260,[280,650],36,['写法','填什么'])
 + card('<p style="font-size:28px;color:var(--soft)">放进一句话里</p>'+p('本轮只修改标题字号；必须保留其余排版和文字；允许调整标题下方的间距。',36,mt=6,lh=1.6),760,fill=LB)
 + card('<p style="font-size:28px;color:var(--red)">常见翻车</p>'+p('只写“改得好看一点”，它会把整页都重做一遍。<br>要改哪里、别动哪里，都要写出来。',36,mt=6,lh=1.6),1040,fill=LR)
 + src('示例内容'),'')
render(P,'whiteboard_demo')
