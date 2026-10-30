# 白板手绘风（方格纸 + 手绘红笔）

方格纸底、霞鹜文楷、rough.js 手绘框/圈/箭头、黄色荧光笔、胶带贴截图。适合教程、对比、清单、带截图的实测。

## 用法
在 $XHS_WORK 下新建一个 python 文件：
```python
from wb_helpers import *     # 含 head/src/render, card, table, chip, at, p, shot, box, LB/LR/LG/LY 等
T=6; P={}
P[1]=(head('①','标题','副标题',1,T) + card(p('正文 <span class="hl">荧光笔</span>',36),300,fill=LY), '')
render(P,'输出名')
```
- 每页是 (HTML, JS) 二元组；JS 用于自定义手绘图（rough.js 的 R、RED、INK、rel()、add()、arrow()）。
- 页面内可用的 class：.rbx（手绘框，data-fill 填色、data-c="red" 红框）、.mark（截图上的红圈，data-k="ellipse|box"）、.hl（荧光笔）、.rstrike（红笔划掉）、.rund（红笔下划线）、.note（红色批注）、.shot（胶带截图）、h1 .n（红圈序号）。
- 多张卡片纵向排列用 flow 布局（一个容器里依次放 .rbx 块），避免绝对定位重叠。
- 截图先放进 $XHS_WORK/img/，用 shot('文件名',x,y,宽,旋转角)。

## 规格
- 画布 1080×1440，渲染 1.5 倍。标题 66px，正文 33–38px。
- 颜色：墨蓝 #1F2A44、红 #D8352A、荧光黄 #FFE14A；卡片底色 LB/LR/LG/LY 四种浅色，一页别超过三种。
- 每页底部用 src() 标来源。
