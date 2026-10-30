#!/bin/bash
# 准备工作目录：字体、rough.js、模板、头像。每次新会话先跑一次。
set -e
SK="$(cd "$(dirname "$0")/.." && pwd)"
W=${XHS_WORK:-/home/claude/xhs_work}
mkdir -p $W/fonts $W/img
cp "$SK/assets/whiteboard_base.html" $W/
[ -f $W/account.json ] || cp "$SK/assets/account.json" $W/account.json
cp "$SK"/scripts/*.py $W/
cd $W/fonts
get(){ [ -s "$1" ] || curl -sL -o "$1" "$2"; }
N=https://github.com/notofonts/noto-cjk/raw/main
get NotoSerifSC-Regular.otf $N/Serif/OTF/SimplifiedChinese/NotoSerifCJKsc-Regular.otf
get NotoSerifSC-Bold.otf    $N/Serif/OTF/SimplifiedChinese/NotoSerifCJKsc-Bold.otf
get NotoSansSC-Regular.otf  $N/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Regular.otf
get NotoSansSC-Bold.otf     $N/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Bold.otf
get NotoSansSC-Black.otf    $N/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Black.otf
get WK-Medium.ttf https://github.com/lxgw/LxgwWenKai/releases/download/v1.520/LXGWWenKai-Medium.ttf
get WK-Light.ttf  https://github.com/lxgw/LxgwWenKai/releases/download/v1.520/LXGWWenKai-Light.ttf
cd $W && [ -d node_modules/roughjs ] || npm i roughjs >/dev/null 2>&1
python3 -c "import playwright" 2>/dev/null || pip install playwright --break-system-packages -q
echo "ready: $W"; ls -la $W/fonts | tail -n +2
