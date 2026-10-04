#!/usr/bin/env python3
"""Builds index.html from voice_alignment.json (ElevenLabs char timings).

Scene windows follow the real narration length; captions and reveals are
anchored to substrings of each scene's TTS text.
"""
import json, subprocess

GAP = 0.2      # silence between scenes
TAIL = 1.2     # hold on the CTA after the last word

al = {a["id"]: a for a in json.load(open("voice_alignment.json"))}
tts = {s["id"]: s["tts"] for s in json.load(open("scenes.json"))}
order = [s["id"] for s in json.load(open("scenes.json"))]

start, t = {}, 0.0
for sid in order:
    start[sid] = round(t, 3)
    t += al[sid]["duration"] + GAP
dur = {sid: round(al[sid]["duration"] + GAP, 3) for sid in order}
dur[order[-1]] = round(al[order[-1]]["duration"] + TAIL, 3)
TOTAL = round(start[order[-1]] + dur[order[-1]], 3)


def cue(sid, sub, nth=0):
    """Absolute time where `sub` starts being spoken in scene `sid`."""
    text = tts[sid]
    idx = -1
    for _ in range(nth + 1):
        idx = text.index(sub, idx + 1)
    # alignment chars mirror the input text 1:1
    assert "".join(al[sid]["chars"]) == text, sid
    return round(start[sid] + al[sid]["starts"][idx], 3)


# ── captions: (display, anchor in TTS text) ───────────────────────────────
CAPS = {
    "01-hook": [("몬트리올에서 이제", "몬트리올"), ("자녀 무상교육이 안 된다고요?", "자녀"),
                ("학생비자로 어학연수도", "학생비자"), ("못 한다고요?", "못 한다"), ("아닙니다!", "아닙니다")],
    "02-answer": [("부모가 사설어학원을 다니면서", "부모가"), ("자녀는 무상교육!", "자녀는"),
                  ("몬트리올 실제 송출 중인", "현재"), ("유일한 유학원", "유일한"),
                  ("AA Canada 독점 프로그램", "에이에이")],
    "03-why": [("연 약 $20,000 대학부설 대비", "연간"), ("학비가 저렴하고", "학비가"),
               ("자녀 등하교 케어도 문제없고", "자녀 등하교"), ("학업 부담도 적습니다", "학업 부담")],
    "04-details": [("처음부터 비자 2년 3개월~3년", "처음부터"), ("비자 연장 필요 없음", "비자 연장"),
                   ("영어 or 불어 선택", "영어나"), ("중간에 변경도 가능", "중간에"),
                   ("매주 시작 가능", "매주"), ("월~금 09:00~13:30", "수업은")],
    "05-cost": [("첫 52주 등록 $17,075", "첫 오십이"), ("수업 종료까지 약 1년 3개월", "수업 종료"),
                ("25주 추가 등록 $8,125", "이후"), ("2년 자녀무상교육 부모 학비", "이년 자녀"),
                ("총 $25,200", "총 이만")],
    "06-kids": [("아이는 영어 중심으로", "아이는"), ("또는 영어+불어 함께!", "또는")],
    "07-longterm": [("장기 플랜이라면", "장기"), ("중하급 불어 회화를 만들어", "중하급"),
                    ("LMIA 면제로 지역 이동", "엘엠아이에이"), ("취업비자로 전환", "취업비자로"),
                    ("풀타임 근무 + 자녀 무상교육 계속", "풀타임"), ("대학 진학 때는", "대학 진학"),
                    ("영주권 없이 영주권자 학비", "영주권 없이")],
    "08-fast": [("불어 점수를 만들면", "불어 점수"), ("1년만 공부하고", "일년만"),
                ("추가 등록 없이 취업비자 전환", "어학원 추가"), ("유료 취업 알선·비자까지 지원", "원하시면")],
    "09-cta": [("몬트리올 자녀 무상교육", "몬트리올"), ("지금 AA Canada에 문의하세요!", "지금")],
}

cap_html = []
for sid in order:
    items = CAPS[sid]
    scene_end = start[sid] + al[sid]["ends"][-1] + 0.12
    for i, (txt, anchor) in enumerate(items):
        s = cue(sid, anchor)
        e = cue(sid, items[i + 1][1]) if i + 1 < len(items) else scene_end
        if sid == order[-1] and i + 1 == len(items):
            e = TOTAL
        cid = f"cap-{sid[:2]}-{i}"
        cap_html.append(
            f'<div id="{cid}" class="clip cap" data-start="{s:.3f}" data-duration="{e - s:.3f}" '
            f'data-track-index="20"><span class="cap-pill">{txt}</span></div>')

audio_html = []
for sid in order:
    audio_html.append(
        f'<audio id="vo-{sid}" src="assets/voice/{sid}.mp3" data-start="{start[sid]:.3f}" '
        f'data-duration="{al[sid]["duration"]:.3f}" data-track-index="30" data-volume="1"></audio>')

S = {sid: start[sid] for sid in order}
D = dur
C = {}
for sid, subs in {
    "01-hook": ["자녀", "학생비자", "못 한다", "아닙니다"],
    "02-answer": ["부모가", "자녀는", "현재", "에이에이"],
    "03-why": ["연간", "학비가", "자녀 등하교", "학업 부담"],
    "04-details": ["처음부터", "비자 연장", "영어나", "중간에", "매주", "수업은"],
    "05-cost": ["첫 오십이", "수업 종료", "이후", "이년 자녀", "총 이만"],
    "06-kids": ["아이는", "또는"],
    "07-longterm": ["장기", "중하급", "엘엠아이에이", "취업비자로", "풀타임", "대학 진학"],
    "08-fast": ["불어 점수", "일년만", "어학원 추가", "원하시면"],
    "09-cta": ["몬트리올", "지금"],
}.items():
    for sub in subs:
        C[f"{sid}|{sub}"] = cue(sid, sub)

tpl = open("src/index.template.txt", encoding="utf-8").read()
scene_attrs = {f"%%S_{sid[:2]}%%": f'data-start="{S[sid]:.3f}" data-duration="{D[sid]:.3f}"' for sid in order}
html = tpl
for k, v in scene_attrs.items():
    html = html.replace(k, v)
html = (html.replace("%%TOTAL%%", f"{TOTAL:.3f}")
            .replace("%%CAPTIONS%%", "\n      ".join(cap_html))
            .replace("%%AUDIO%%", "\n      ".join(audio_html))
            .replace("%%CUES%%", json.dumps(C, ensure_ascii=False))
            .replace("%%STARTS%%", json.dumps(S))
            .replace("%%DURS%%", json.dumps(D)))
open("index.html", "w", encoding="utf-8").write(html)

# music bed: trim to the video, gentle fade in/out
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "assets/music/bgm.mp3",
                "-af", f"atrim=0:{TOTAL},afade=t=in:d=0.6,afade=t=out:st={TOTAL - 2.5}:d=2.5",
                "-b:a", "160k", "assets/music/bgm-fit.mp3"], check=True)
print("TOTAL", TOTAL)
for sid in order:
    print(sid, S[sid], D[sid])
