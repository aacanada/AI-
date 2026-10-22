"""upload-text.txt for the long-form and the five shorts (chapter times come from timing.json, so re-run after the
recordings arrive and build.py has re-timed everything). Run from project root:
    python3 -I tools/upload_text.py
"""
import json
import os

BLOG = "[블로그 링크]"  # 발행 후 실제 주소로 교체
HOME = "[홈페이지 링크]"

SOURCES = """※ 출처
· REM: rem.info 보도자료 "The REM ready to welcome first passengers" (2023-07-28) · 브로사드–중앙역 16.6km, 18분, 역 5개, 출퇴근 3분 45초 간격(개통 당시), 2023-07-31 운행 시작
· 인구: Statistics Canada 2021 Census (가시적 소수자 집단, 25% 표본) · 아시아계 = 중국·한국·일본·필리핀·동남아계 합계
· 교육청: Riverside School Board 2026-27 브로슈어 (초등 19곳·고등 4곳, 졸업·자격 취득률 88.5%·몬테레지 1위는 브로슈어 기준), 각 학교 홈페이지, Fraser Institute 2025 퀘벡 고교 평가
· 비용·일정: RSB 학생·가족용 학비표 2027-28, RSB 학사일정(2027.02 ~ 2028.06) · 학교 예시 금액(CAQ 포함), 캐나다 달러, 변경될 수 있음
· 학교 영상: Riverside School Board 공식 영상
· 지도: AA Canada 스키매틱(실제 좌표 기준), 캐나다 지도 svg-maps/canada (CC BY 4.0)"""

CHAPTERS = {
    "s01": "몬트리올 = 불어? 강 하나만 건너면",
    "s02": "사우스쇼어는 어디?",
    "s03": "REM, 다운타운까지 18분",
    "s04": "한국 사람이 거의 없는 동네 (2021 인구조사)",
    "s05": "리버사이드 교육청",
    "s06": "고등학교 4곳 (학교 영상)",
    "s07": "초등학교",
    "s08": "비용과 일정 (2027-28)",
    "s09": "제가 사우스쇼어를 권하는 이유",
    "s10": "세 줄 정리",
}

TAGS = "#몬트리올조기유학 #캐나다조기유학 #몬트리올 #사우스쇼어 #REM #리버사이드교육청 #캐나다영어공립학교 #브로사드 #생랑베르 #AACanada"

SHORT_TEXT = {
    "a": ("다운타운 18분, REM 타고 학교 동네로 #shorts",
          "몬트리올 다운타운에서 강 하나 건너면 영어 공립학교 동네, 사우스쇼어.\n새 무인 경전철 REM으로 브로사드역에서 다운타운 중앙역까지 16.6km, 18분입니다.",
          "#REM #몬트리올 #사우스쇼어 #몬트리올조기유학 #캐나다조기유학 #shorts"),
    "b": ("코퀴틀람 한국계 11,900명 vs 생랑베르 50명 #shorts",
          "2021 캐나다 인구조사로 본 한국계 인구.\n코퀴틀람 약 11,900명, 생랑베르 50명, 부셔빌 30명, 생브루노 35명, 롱게일 425명.",
          "#몬트리올조기유학 #코퀴틀람 #생랑베르 #캐나다조기유학 #shorts"),
    "c": ("브로사드 vs 생랑베르, 솔직 비교 #shorts",
          "브로사드는 아시아계가 인구의 약 20%(2021 인구조사), 대신 생활이 편합니다. 한국계는 브로사드도 590명, 1% 미만.\n영어만 쓰는 환경을 원하면 생랑베르·부셔빌, 생활 편의도 본다면 브로사드.",
          "#브로사드 #생랑베르 #몬트리올조기유학 #캐나다조기유학 #shorts"),
    "d": ("몬트리올 영어 공립 고등학교 4곳 #shorts",
          "리버사이드 교육청 고등학교 4곳: 헤리티지(IB·예술·스포츠·IT), 센테니얼(영재반 TaG), 생랑베르 인터내셔널(작은 IB 학교), 세인트 존스(유치원~고등 한 학교).\n영상: Riverside School Board",
          "#헤리티지 #센테니얼 #생랑베르인터내셔널 #세인트존스 #몬트리올조기유학 #shorts"),
    "e": ("캐나다 공립 조기유학 1년, 얼마일까? #shorts",
          "리버사이드 학생·가족용 학비표 2027-28 기준, 학교 예시(CAQ 포함).\n1년 과정 약 CAD 32,000 · 한 학기(5개월) 약 CAD 18,800 · 변경될 수 있음.",
          "#캐나다조기유학 #몬트리올조기유학 #조기유학비용 #리버사이드교육청 #shorts"),
}


def mmss(t):
    t = int(round(t))
    return f"{t // 60:02d}:{t % 60:02d}"


def longform():
    tj = json.load(open("timing.json", encoding="utf-8"))
    ch = "\n".join(f"{mmss(s['start'])} {CHAPTERS[s['id']]}" for s in tj["slots"])
    real = all(s["real"] for s in tj["slots"])
    warn = "" if real else "\n(※ 챕터 시간은 녹음 전 임시 타이밍입니다. 녹음 반영 후 upload_text.py를 다시 실행하세요.)\n"
    return f"""[유튜브 제목]
다운타운 18분인데 한국 사람이 거의 없다? 몬트리올 사우스쇼어, 지도로 보는 영어 공립학교 동네

[유튜브 설명]
몬트리올은 불어 도시라서 조기유학 후보에서 빼셨나요?
몬트리올 다운타운에서 강 하나만 건너면, 수업을 영어로 하는 공립학교들이 모여 있는 동네가 있습니다.
REM 경전철로 다운타운까지 18분, 한국 사람이 거의 없는 몬트리올 남쪽 사우스쇼어를 AA Canada 원장이 지도로 정리했습니다.
{warn}
{ch}

▶ 학교별 자세한 정보(벨타임·프로그램·비용): {BLOG}
▶ 홈페이지 학교 정리: {HOME}
▶ 우리 아이에게 맞는 동네·학교 상담: 카카오톡 canlog · 02-567-4345

{SOURCES}

{TAGS}

[인스타 캡션]
몬트리올 = 불어? 강 하나만 건너면 영어 공립학교 동네 🍁

✔ REM으로 다운타운까지 18분
✔ 한국계 인구 생랑베르 50명 · 부셔빌 30명 (2021 인구조사)
✔ 리버사이드 교육청 초등 19 · 고등 4

아이 학년과 성향을 보내 주시면 동네·학교와 학교 영상을 골라 드려요.
카카오톡 canlog · 📞 02-567-4345

※ 비용·인구·REM 수치 출처는 유튜브 설명란 참고
"""


def short(key):
    t, desc, tags = SHORT_TEXT[key]
    return f"""[유튜브 제목]
{t}

[유튜브 설명]
{desc}

▶ 전체 영상: 관련 동영상 (몬트리올 사우스쇼어, 지도로 보는 영어 공립학교 동네)
▶ 학교별 정리: {BLOG}
▶ 상담: 카카오톡 canlog · 02-567-4345

{tags}

[인스타 캡션]
{desc}

전체 영상은 프로필 링크에서 · 카카오톡 canlog
"""


if __name__ == "__main__":
    open("upload-text.txt", "w", encoding="utf-8").write(longform())
    for k in SHORT_TEXT:
        open(os.path.join("..", "southshore-shorts", f"short-{k}", "upload-text.txt"), "w", encoding="utf-8").write(short(k))
    print("upload-text.txt + 5 shorts")
