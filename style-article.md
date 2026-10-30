# 文章风（推文截图封面 + 文章页内页）

模仿两篇高收藏笔记：捏捏番茄《近期刷到一个含金量非常高的提示词》（封面推文截图）和见山 Jetson《从来没人说过，学AI第一步是Github》（内页文章页）。清爽、可读性高、像真人写的文章。

## 视觉规格
- 推文封面：纯白底，头像 128px + 账号名（粗）+ @handle（灰），右上“···”。正文无衬线 40px，行距 1.7，重点 <b>。可嵌 code 卡（灰色标题栏 + 等宽字 + <mark>黄色高亮</mark>）或图片卡。
- 文章内页：米白底 #F7F6F2，思源宋体。h1 60px + 深青短线；作者行（头像、账号、日期）只放在文章第一页；小标题 h2 42px 左侧竖线；正文 36px 行距 1.9；重点 <b> 为深青色；提示词放 quote（浅灰圆角块）；例子用 example（灰色删除线 → 改后）；tip 是虚线隔开的小提醒；页脚细线 + 标题简称 + “n / 总数”。

## spec 格式（JSON）
```json
{
  "title_short": "页脚左侧的标题简称",
  "date": "2026年 10月 30日",
  "accent": "#1E4D5C",
  "account": {"name": "可选，覆盖 account.json", "handle": "@xxx"},
  "pages": [
    {"type": "tweet", "blocks": [{"p": "..."}, {"code": {"header": "来源栏", "text": "可含 <mark>高亮</mark>"}}, {"card_img": "图片路径"}]},
    {"type": "article", "blocks": [{"h1": "标题<br>第二行"}, {"author": true}, {"p": "..."}]},
    {"type": "article", "blocks": [{"h2": "小标题"}, {"p": "..."}, {"quote": "提示词"}, {"bullets": ["a","b"]}, {"numbered": ["a","b"]}, {"example": ["原句","改成"]}, {"tip": "小提醒"}, {"img": "图片路径"}]}
  ]
}
```
- 文本里可用 <b>、<br>、<s>、<mark>。
- 完整示例：assets/example_article.json

## 渲染与检查
```bash
cd $XHS_WORK   # 默认 /home/claude/xhs_work
python3 render_article.py spec.json 输出名
```
- 脚本会打印每页内容底部位置：>1290 溢出（删字或拆页），<1000 偏空（加例子、小提醒或合并页）。
- 渲染后拼一张缩略图总览，自己看一遍再交付。
