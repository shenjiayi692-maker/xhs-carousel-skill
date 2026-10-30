# xhs-carousel：小红书图文 Skill

一个给 Claude 用的 Skill：把一篇文章、一份教程或一个选题，做成可以直接发的小红书图文笔记，包括 3:4 轮播图、标题、正文和话题。

![预览](examples/preview.jpg)

## 两种风格

**文章风**：封面做成推文截图（头像、账号名、正文，可嵌一张高亮截图卡），内页像一页书：米白底、宋体、左侧竖线小标题、浅灰引用块放提示词。清爽，可读性高，适合干货和提示词合集。

**白板手绘风**：方格纸底、手写体、手绘框和红笔圈画、荧光笔、胶带贴截图。适合教程、对比、带截图的实测。

## 它会帮你做到
- 封面先给钩子，缩到信息流大小也读得清
- 一页一个单元，每页都有干货，自动提示“溢出”和“偏空”的页面
- 文案去 AI 味：不用“值得注意的是”“不是 A 而是 B”这类套话
- 新闻和数字先核实，别人的图和思路标出处
- 交付时同时给出标题、正文、话题和“发之前注意”

## 安装

**Claude.ai / Claude 桌面版**
1. 下载 `dist/xhs-carousel.zip`
2. 打开 Customize > Skills，点“+”，选“Upload a skill”，上传这个 ZIP

**Claude Code**
```bash
cp -r skills/xhs-carousel ~/.claude/skills/
```

## 使用
对 Claude 说“把这篇改成小红书图文，用文章风”之类的话即可。第一次使用时，它会问你的账号名、@handle 和头像，存进 `account.json`，之后自动套用。

每个新会话第一次出图时，会从 GitHub 下载字体（一百多 MB），需要一两分钟。

## 目录
```
skills/xhs-carousel/
├── SKILL.md                  流程
├── references/               两种风格的规格、内容规则
├── scripts/
│   ├── setup.sh              准备环境、下载字体
│   ├── render_article.py     文章风渲染器（写 JSON 就能出图）
│   ├── wb_lib.py             白板手绘风渲染库
│   └── wb_helpers.py         白板手绘风常用组件
└── assets/                   模板、示例、account.json
```

## 第三方资源
- 思源宋体 / 思源黑体（Noto CJK）：SIL Open Font License 1.1
- 霞鹜文楷（LXGW WenKai）：SIL Open Font License 1.1
- rough.js：MIT License

字体和 rough.js 在运行时从官方仓库下载，不随本仓库分发。

## License
MIT
