"""upload-text.txt for the long-form and the five shorts (chapter times come from timing.json, so re-run after the
recordings arrive and build.py has re-timed everything). Run from project root:
    python3 -I tools/upload_text.py
"""
import json
import os

AI_VOICE = "※ 이 영상의 내레이션은 AI 음성(ElevenLabs)으로 만들었습니다."
INFO = "학교별 벨타임·프로그램·비용 정리는 AA Canada 네이버 블로그와 홈페이지에 있습니다."

# one line per number shown or spoken, with its source and reference date
SRC = {
    "rem": "· 18분·16.6km·역 5개·출퇴근 3분 45초 간격: REM 보도자료 \"The REM ready to welcome first passengers\" (rem.info, 2023-07-28 발표 / 개통 2023-07-31 당시 기준)",
    "coq": "· 코퀴틀람 한국계 약 11,900명(시 인구의 8.1%): Statistics Canada 2021 Census, Focus on Geography Series – Coquitlam (인구조사 기준일 2021-05-11)",
    "south": "· 한국계 생랑베르 50명·부셔빌 30명·생브루노 35명·롱게일 425명·브로사드 590명(1% 미만), 롱게일 인구 약 25만 명: Statistics Canada 2021 Census Profile, 25% 표본 (기준일 2021-05-11)",
    "rsb": "· 초등학교 19곳·고등학교 4곳, 졸업·자격 취득률 88.5%·몬테레지 지역 1위: Riverside School Board 2026-27 국제학생 브로슈어 기재값",
    "hs": "· 헤리티지 학생 1,600명 이상·센테니얼 약 1,100명·생랑베르 인터내셔널 약 400명: 각 학교 홈페이지 (2026-10 확인) · 센테니얼 점수: Fraser Institute 2025 퀘벡 고교 평가",
    "el": "· 굿셰퍼드 수업 80% 이상 영어·생랑베르 초등 영어 70 : 불어 30·수업 시작 7:50 / 9:05: 각 학교 교육계획·벨타임 (2026-27학년도)",
    "cost": "· 1년 과정 약 CAD 32,000·한 학기(5개월) 약 CAD 18,800: RSB 학생·가족용 학비표 2027-28, 학교 예시 금액(CAQ 포함), 변경될 수 있음",
    "date": "· 2027-02-02 겨울 학기·2027-09-08 1년 과정 시작: RSB 학사일정 2027-28",
    "map": "· 지도: AA Canada 스키매틱(실제 좌표 기준), 캐나다 지도 svg-maps/canada (CC BY 4.0) · 학교 영상: Riverside School Board 공식 영상",
}


def sources(*keys):
    return "※ 출처·기준일\n" + "\n".join(SRC[k] for k in keys)


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
          "#REM #몬트리올 #사우스쇼어 #몬트리올조기유학 #캐나다조기유학 #shorts", ("rem", "map")),
    "b": ("코퀴틀람 한국계 11,900명 vs 생랑베르 50명 #shorts",
          "2021 캐나다 인구조사로 본 한국계 인구.\n코퀴틀람 약 11,900명, 생랑베르 50명, 부셔빌 30명, 생브루노 35명, 롱게일 425명.",
          "#몬트리올조기유학 #코퀴틀람 #생랑베르 #캐나다조기유학 #shorts", ("coq", "south")),
    "c": ("브로사드 vs 생랑베르, 솔직 비교 #shorts",
          "브로사드는 중국계 커뮤니티가 커서 아시아계 주민이 꽤 많고, 대신 생활이 편합니다. 한국계는 브로사드도 590명, 1% 미만.\n영어만 쓰는 환경을 원하면 생랑베르·부셔빌, 생활 편의도 본다면 브로사드.",
          "#브로사드 #생랑베르 #몬트리올조기유학 #캐나다조기유학 #shorts", ("south",)),
    "d": ("몬트리올 영어 공립 고등학교 4곳 #shorts",
          "리버사이드 교육청 고등학교 4곳: 헤리티지(IB·예술·스포츠·IT), 센테니얼(영재반 TaG), 생랑베르 인터내셔널(작은 IB 학교), 세인트 존스(유치원~고등 한 학교).",
          "#헤리티지 #센테니얼 #생랑베르인터내셔널 #세인트존스 #몬트리올조기유학 #shorts", ("rsb", "hs", "map")),
    "e": ("캐나다 공립 조기유학 1년, 얼마일까? #shorts",
          "리버사이드 학생·가족용 학비표 2027-28 기준, 학교 예시(CAQ 포함).\n1년 과정 약 CAD 32,000 · 한 학기(5개월) 약 CAD 18,800 · 변경될 수 있음.",
          "#캐나다조기유학 #몬트리올조기유학 #조기유학비용 #리버사이드교육청 #shorts", ("cost",)),
}


def mmss(t):
    t = int(round(t))
    return f"{t // 60:02d}:{t % 60:02d}"


def longform():
    tj = json.load(open("timing.json", encoding="utf-8"))
    ch = "\n".join(f"{mmss(s['start'])} {CHAPTERS[s['id']]}" for s in tj["slots"])
    assert all(s["real"] for s in tj["slots"]), "voice missing: chapter times would be provisional"
    src = sources("rem", "coq", "south", "rsb", "hs", "el", "cost", "date", "map")
    return f"""[유튜브 제목]
다운타운 18분인데 한국 사람이 거의 없다? 몬트리올 사우스쇼어, 지도로 보는 영어 공립학교 동네

[유튜브 설명]
몬트리올은 불어 도시라서 조기유학 후보에서 빼셨나요?
몬트리올 다운타운에서 강 하나만 건너면, 수업을 영어로 하는 공립학교들이 모여 있는 동네가 있습니다.
REM 경전철로 다운타운까지 18분, 한국 사람이 거의 없는 몬트리올 남쪽 사우스쇼어를 AA Canada가 지도로 정리했습니다.

{ch}

▶ {INFO}
▶ 우리 아이에게 맞는 동네·학교 상담: 카카오톡 canlog · 02-567-4345

{src}

{AI_VOICE}

{TAGS}

[인스타 캡션]
몬트리올 = 불어? 강 하나만 건너면 영어 공립학교 동네 🍁

✔ REM으로 다운타운까지 18분 (REM 보도자료 2023-07-28)
✔ 한국계 인구 생랑베르 50명 · 부셔빌 30명 (2021 캐나다 인구조사)
✔ 리버사이드 교육청 초등 19 · 고등 4 (교육청 2026-27 브로슈어)

아이 학년과 성향을 보내 주시면 동네·학교와 학교 영상을 골라 드려요.
카카오톡 canlog · 📞 02-567-4345

{AI_VOICE}

[Threads]
몬트리올은 불어 도시라 조기유학 후보에서 빼셨다면, 강 건너 남쪽 사우스쇼어를 한 번 보세요.
REM으로 다운타운 중앙역까지 18분(REM 보도자료 2023-07-28), 한국계 인구는 생랑베르 50명·부셔빌 30명(2021 캐나다 인구조사).
리버사이드 교육청 영어 공립학교 초등 19곳·고등 4곳(교육청 2026-27 브로슈어)을 지도로 정리했습니다.
상담: 카카오톡 canlog
{AI_VOICE}
"""


def short(key):
    t, desc, tags, keys = SHORT_TEXT[key]
    src = sources(*keys)
    return f"""[유튜브 제목]
{t}

[유튜브 설명]
{desc}

▶ 전체 영상: 관련 동영상 (몬트리올 사우스쇼어, 지도로 보는 영어 공립학교 동네)
▶ {INFO}
▶ 상담: 카카오톡 canlog · 02-567-4345

{src}

{AI_VOICE}

{tags}

[인스타 캡션]
{desc}

전체 영상은 프로필 링크에서 · 카카오톡 canlog

{src}

{AI_VOICE}
"""


if __name__ == "__main__":
    open("upload-text.txt", "w", encoding="utf-8").write(longform())
    for k in SHORT_TEXT:
        open(os.path.join("..", "southshore-shorts", f"short-{k}", "upload-text.txt"), "w", encoding="utf-8").write(short(k))
    print("upload-text.txt + 5 shorts")
