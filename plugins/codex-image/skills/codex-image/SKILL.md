---
name: codex-image
description: >
  Generate raster images (illustrations, photorealistic scenes, concept art,
  mockups, character scenes) by invoking the local Codex CLI's imagegen skill
  and copying the PNG into the current workspace. Use when the user asks to
  "generate an image", "draw", "畫一張圖", "產圖", "生圖", or describes a
  visual scene to produce. Default output: cwd with timestamp filename.
  Do NOT use for flowcharts/architecture diagrams (use Mermaid), precision
  alignment graphics (use SVG), or images with heavy text (use SVG overlay).
---

呼叫本機 codex exec 生圖，從 stdout 抓 session id，
把 PNG 從 `~/.codex/generated_images/{session_id}/` 複製到目標位置。
預設目標位置是當前工作目錄，檔名 `codex-image-YYYYMMDD-HHMMSS.png`。

## 何時用

- 插畫、寫實風、概念示意圖、人物場景、產品 mockup
- 不適合：流程圖／架構圖（用 Mermaid）、精確對齊對照圖（用 SVG）、
  圖內大量文字（用 SVG 疊文字）

## Prompt 撰寫

中文 prompt 即可。建議結構：主體與動作 + 場景／環境 + 光線／氛圍 + 風格。
風格詞彙範例：溫暖插畫風、日系動畫風、水彩風、電影感寫實風、
等角視圖（isometric）、賽博龐克風、編輯雜誌風。

## 工作流

### 1. 跟使用者確認目標路徑

如果使用者沒指定，預設用 cwd。如果在專案內，問一下要不要放到 `assets/`、`public/images/` 之類的位置。

### 2. 執行 codex exec 並抓 session id

關鍵 flags（缺一不可）：
- `--skip-git-repo-check` — 允許在非 git 目錄跑
- `--sandbox workspace-write` — 預設 read-only sandbox 寫不了檔
- `< /dev/null` — 避免 codex 卡在等 stdin

```bash
LOG=$(mktemp -t codex-image.XXXXXX.log)
codex exec --skip-git-repo-check --sandbox workspace-write \
  "<完整 prompt>" < /dev/null > "$LOG" 2>&1
SID=$(sed -n 's/^session id: //p' "$LOG" | head -1)
[ -z "$SID" ] && { echo "找不到 session id，log: $LOG"; exit 1; }
SRC_DIR="$HOME/.codex/generated_images/$SID"
```

### 3. 複製到目標路徑

```bash
DEST="<目標目錄>"
mkdir -p "$DEST"
TS=$(date +%Y%m%d-%H%M%S)
i=0
for src in "$SRC_DIR"/ig_*.png; do
  i=$((i+1))
  if [ "$i" = "1" ]; then
    DST="$DEST/codex-image-$TS.png"
  else
    DST="$DEST/codex-image-$TS-$i.png"
  fi
  cp "$src" "$DST"
  echo "✓ $DST"
done
```

### 4. 驗證

用 Read 工具開複製出來的 PNG，確認構圖、文字、風格符合需求。
不滿意就改 prompt 重生 — 每次 codex exec 都是新 session，不會覆蓋舊圖。

## 反例

- 不抓 session id 直接 `ls ~/.codex/generated_images/`：會抓到別任務的舊圖
- 把 `~/.codex/generated_images/{sid}/` 當資產引用：那是 codex 私有目錄，
  要先複製到專案內
- prompt 塞「圖中有 5 行文字寫 X、Y、Z」：codex 文字渲染穩定度不夠，
  需要文字疊圖用 SVG 後製
- 忘記 `--sandbox workspace-write`：codex 預設 read-only 寫不了檔，靜默失敗
