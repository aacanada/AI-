"""학교 정본 마크다운을 홈페이지에 붙여 넣을 HTML로 바꾼다.

사용: PYTHONPATH=<markdown 설치 경로> python3 tools/md2html.py <입력.md> <출력.html> [대표이미지 경로]
- 출력은 <div class="aac-school">...</div> 조각과 스타일을 담은 독립 HTML.
  홈페이지 편집기에는 <body> 안의 내용만 복사해 넣으면 된다.
- .md 링크는 .html 링크로 바꾼다.
"""
import re
import sys
from pathlib import Path

import markdown

STYLE = """
.aac-school{max-width:860px;margin:0 auto;padding:24px 16px;font-family:Pretendard,'Apple SD Gothic Neo','Malgun Gothic',sans-serif;color:#1d2733;line-height:1.7;word-break:keep-all}
.aac-school h1{font-size:30px;line-height:1.3;margin:0 0 12px}
.aac-school h2{font-size:23px;margin:36px 0 12px;padding-bottom:6px;border-bottom:3px solid #c8102e}
.aac-school h3{font-size:19px;margin:24px 0 8px}
.aac-school blockquote{margin:12px 0;padding:10px 16px;background:#f6f1e7;border-left:4px solid #e8b931;color:#5f6b78;font-size:15px}
.aac-school table{width:100%;border-collapse:collapse;margin:12px 0;font-size:15px}
.aac-school th,.aac-school td{border:1px solid #d9d2c3;padding:8px 10px;text-align:left;vertical-align:top}
.aac-school th{background:#0f2a44;color:#fff}
.aac-school tr:nth-child(even) td{background:#faf8f3}
.aac-school img.hero{width:100%;max-width:540px;display:block;margin:8px auto 20px;border-radius:12px}
.aac-school a{color:#c8102e}
.aac-school code{background:#f2f2f2;padding:1px 5px;border-radius:4px}
@media (max-width:600px){.aac-school table{font-size:13px}.aac-school th,.aac-school td{padding:6px}}
"""


def convert(src: Path, dst: Path, hero: str | None) -> None:
    text = src.read_text(encoding="utf-8")
    text = re.sub(r"\]\(([^)]+?)\.md\)", r"](\1.html)", text)
    body = markdown.markdown(text, extensions=["tables", "sane_lists"])
    if hero:
        body = re.sub(r"(</h1>)", rf'\1\n<img class="hero" src="{hero}" alt="">', body, count=1)
    title = re.search(r"<h1>(.*?)</h1>", body)
    title_text = re.sub(r"<[^>]+>", "", title.group(1)) if title else src.stem
    html = (
        "<!doctype html>\n<html lang=\"ko\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n"
        f"<title>{title_text} | AA Canada</title>\n<style>{STYLE}</style>\n</head>\n<body>\n"
        f"<div class=\"aac-school\">\n{body}\n</div>\n</body>\n</html>\n"
    )
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(html, encoding="utf-8")
    print("wrote", dst)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    convert(Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3] if len(sys.argv) > 3 else None)
