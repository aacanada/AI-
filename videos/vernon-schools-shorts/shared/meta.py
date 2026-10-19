"""Write <short>/meta.txt (publish-queue metadata, brief section 4).  Re-run after rendering to fill in the video facts.
Usage: python3 shared/meta.py <short-dir> [branch]"""
import json, pathlib, subprocess, sys

ROOT = pathlib.Path(sys.argv[1]).resolve()
BRANCH = sys.argv[2] if len(sys.argv) > 2 else "claude/clever-rubin-cws060"
spec = json.loads((ROOT / "script.json").read_text())
pub = spec["publish"]
mp4 = ROOT / "renders" / "video.mp4"
if mp4.exists():
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp4)]))
    mb = mp4.stat().st_size / 1e6
    vid = f"video.mp4 (1080x1920, {int(d // 60)}:{round(d % 60):02d}, {mb:.0f}MB)"
else:
    vid = "video.mp4 (not rendered yet)"
series = "버논 고등학교 한눈에" if spec["n"] == 6 else f"버논 고등학교 탐방 {spec['n']}/5"
meta = f"""type: shorts
title: {pub['hook']} ({series})
channels: youtube, instagram, threads, clip
visibility: public
publish_order: {spec['n']}
publish_after: {pub['after']}
linked_to: (none)
files: {vid}, thumbnail.jpg (1080x1920 cover), upload-text.txt
source: aacanada/AI- branch {BRANCH}, videos/vernon-schools-shorts/{ROOT.name}/
notes: 유튜브 쇼츠 '관련 동영상'에 기존 버논 롱폼 https://youtu.be/UBTh_AdpNGI 를 연결해 주세요. 블로그·홈페이지는 Aside가 학교별 상세 글로 따로 작성하므로 이 묶음의 channels에서 뺐습니다.
"""
(ROOT / "meta.txt").write_text(meta)
print(meta)
