#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# MixMind Video Extraction Pipeline
# =============================================================================
#
# Extracts a precise segment from a YouTube video using yt-dlp + FFmpeg.
# Outputs: clip.mp4, poster.jpg, thumbnail.jpg, metadata.json
#
# Prerequisites:
#   brew install yt-dlp ffmpeg   (macOS)
#   or: scoop install yt-dlp ffmpeg   (Windows)
#   or: apt install yt-dlp ffmpeg   (Linux)
#
# Usage:
#   ./extract-demo.sh --url <youtube-url> --start <seconds> --end <seconds> [--output <dir>]
#
# Example:
#   ./extract-demo.sh \
#     --url "https://youtu.be/GtSCkHk9fLw" \
#     --start 18600 \
#     --end 18764 \
#     --output ../../frontend/public/demo
# =============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log()  { echo -e "${GREEN}[✓]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }
error(){ echo -e "${RED}[✗]${NC} $1"; exit 1; }
info() { echo -e "${CYAN}[i]${NC} $1"; }

# --- Parse arguments ---
URL=""
START=""
END=""
OUTPUT_DIR=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --url)    URL="$2";    shift 2 ;;
    --start)  START="$2";  shift 2 ;;
    --end)    END="$2";    shift 2 ;;
    --output) OUTPUT_DIR="$2"; shift 2 ;;
    *) error "Unknown option: $1. Usage: --url <url> --start <s> --end <s> [--output <dir>]" ;;
  esac
done

[[ -z "$URL" ]]   && error "Missing --url"
[[ -z "$START" ]] && error "Missing --start"
[[ -z "$END" ]]   && error "Missing --end"

OUTPUT_DIR="${OUTPUT_DIR:-./output}"
mkdir -p "$OUTPUT_DIR"

DURATION=$((END - START))
[[ "$DURATION" -le 0 ]] && error "End time must be greater than start time."

# --- Check prerequisites ---
command -v yt-dlp >/dev/null 2>&1 || error "yt-dlp is not installed. Install it first."
command -v ffmpeg  >/dev/null 2>&1 || error "ffmpeg is not installed. Install it first."

info "Pipeline: YouTube → yt-dlp → FFmpeg → optimized MP4"
info "URL:      $URL"
info "Segment:  ${START}s → ${END}s (${DURATION}s total)"
echo ""

# --- Step 1: Fetch video metadata ---
info "Fetching video metadata..."
YT_ID=$(yt-dlp --print id "$URL" 2>/dev/null)
TITLE=$(yt-dlp --print title "$URL" 2>/dev/null)
ARTIST=$(yt-dlp --print uploader "$URL" 2>/dev/null)
log "Video ID: $YT_ID — \"$TITLE\" by $ARTIST"

# --- Step 2: Download best quality video ---
RAW="$OUTPUT_DIR/_raw.mp4"
if [[ ! -f "$RAW" ]]; then
  info "Downloading video (best quality)..."
  yt-dlp \
    -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" \
    --output "$RAW" \
    --no-playlist \
    --quiet \
    "$URL" || error "yt-dlp download failed."
  log "Downloaded to $RAW"
else
  warn "Using cached download: $RAW"
fi

# --- Step 3: Extract segment with FFmpeg ---
CLIP="$OUTPUT_DIR/clip.mp4"
info "Extracting segment ${START}s → ${END}s..."
# Get video info for metadata
FPS=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 "$RAW" 2>/dev/null | head -1)
if command -v bc &>/dev/null; then
  FPS=$(echo "scale=2; $FPS" | bc 2>/dev/null || echo "$FPS")
fi
RES=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "$RAW" 2>/dev/null | head -1 || echo "unknown")

ffmpeg -y \
  -ss "$START" \
  -i "$RAW" \
  -t "$DURATION" \
  -c:v libx264 \
  -preset slow \
  -crf 18 \
  -profile:v high \
  -pix_fmt yuv420p \
  -c:a aac \
  -b:a 192k \
  -movflags +faststart \
  "$CLIP" 2>&1 | tail -1

log "Clip created: $CLIP"

# --- Step 4: Generate poster frame (first frame of clip) ---
POSTER="$OUTPUT_DIR/poster.jpg"
info "Generating poster frame..."
ffmpeg -y -ss 0 -i "$CLIP" -vframes 1 -q:v 3 "$POSTER" 2>&1 | tail -1
log "Poster: $POSTER"

# --- Step 5: Generate thumbnail (midpoint frame, smaller) ---
THUMB="$OUTPUT_DIR/thumbnail.jpg"
info "Generating thumbnail..."
MID=$((DURATION / 2))
ffmpeg -y -ss "$MID" -i "$CLIP" -vframes 1 -vf "scale=640:360" -q:v 5 "$THUMB" 2>&1 | tail -1
log "Thumbnail: $THUMB"

# --- Step 6: Write metadata.json ---
META="$OUTPUT_DIR/metadata.json"
info "Writing metadata.json..."
cat > "$META" << METAEOF
{
  "videoTitle": "$TITLE",
  "artist": "$ARTIST",
  "youtubeId": "$YT_ID",
  "durationOriginal": $(yt-dlp --print duration "$URL" 2>/dev/null || echo 0),
  "clipDuration": $DURATION,
  "startTime": $START,
  "endTime": $END,
  "fps": "$FPS",
  "resolution": "$RES",
  "thumbnail": "thumbnail.jpg",
  "poster": "poster.jpg",
  "src": "clip.mp4",
  "generatedAt": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
METAEOF
log "Metadata: $META"

# --- Cleanup ---
rm -f "$RAW"

echo ""
log "Pipeline complete!"
echo ""
echo "  Output directory: $OUTPUT_DIR"
echo "  Files:"
ls -lh "$OUTPUT_DIR" | tail -n +2
