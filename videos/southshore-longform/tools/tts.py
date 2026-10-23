"""Narration with ElevenLabs (voice "일곱번째", eleven_multilingual_v2) instead of the director's recording.
Run from project root (needs ELEVENLABS_API_KEY):
    python3 -I tools/tts.py [--force] [s01 s04 ...]
Per scene:
    ../../plans/southshore-longform/audio/ss_sNN.mp3   the TTS take (committed, same naming as the recording files)
    assets/voice/sNN.align.json                        with-timestamps character alignment of the spoken text
    assets/voice/sNN.wav                               -16 LUFS, untrimmed so the alignment times stay valid
    assets/voice/sNN.words.json                        [{"text","start","end"}] per spoken word -> tools/timing.py
Captions keep the script text; only the spoken text has numbers written out (SAY) so they read naturally.
"""
import base64
import json
import os
import subprocess
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script import SCENES  # noqa: E402

VOICE_NAME = "일곱번째"
VOICE_ID = "vxpRrQegUpenYtez6hz1"  # GET /v1/voices name "일곱번째" (cloned)
MODEL = "eleven_multilingual_v2"
SETTINGS = {"stability": 0.5, "similarity_boost": 0.85, "style": 0.15, "use_speaker_boost": True}
AUD = os.path.join("..", "..", "plans", "southshore-longform", "audio")
OUT = os.path.join("assets", "voice")

# script text -> spoken text (applied in order, per scene)
SAY = {
    "s01": [("AA Canada", "에이에이 캐나다")],
    "s03": [("REM은", "렘은"), ("REM이에요", "렘이에요"), ("2023년 7월 31일", "이천이십삼 년 칠월 삼십일 일"),
            ("16.6킬로미터를 18분에", "십육 점 육 킬로미터를 십팔 분에"), ("3, 4분마다", "삼사 분마다"), ("18분 만에", "십팔 분 만에")],
    "s04": [("2021년", "이천이십일 년"), ("약 1만 1,900명", "약 만 천구백 명"), ("8% 정도", "팔 퍼센트 정도"),
            ("50명", "오십 명"), ("30명", "삼십 명"), ("35명", "삼십오 명"), ("25만 명", "이십오만 명"), ("425명", "사백이십오 명"),
            ("590명", "오백구십 명"), ("1%가", "일 퍼센트가")],
    "s05": [("19곳", "열아홉 곳"), ("4곳", "네 곳"), ("88.5%", "팔십팔 점 오 퍼센트"), ("1위", "일 위"), ("3단계", "삼 단계")],
    "s06": [("1,600명", "천육백 명"), ("IB", "아이비"), ("TaG", "태그"), ("400명", "사백 명")],
    "s07": [("80%", "팔십 퍼센트"), ("영어 70, 불어 30", "영어 칠십, 불어 삼십"), ("IB", "아이비")],
    "s08": [("2027-28학년도", "이천이십칠, 이십팔 학년도"), ("CAQ", "씨에이큐"), ("3만 2천", "삼만 이천"), ("5개월", "오 개월"),
            ("1만 8,800달러", "만 팔천팔백 달러"), ("2027년 2월 2일", "이천이십칠 년 이월 이일"), ("2027년 9월 8일", "이천이십칠 년 구월 팔일")],
    "s09": [("18분", "십팔 분")],
    "s10": [("REM으로 18분", "렘으로 십팔 분"), ("19곳", "열아홉 곳"), ("4곳", "네 곳")],
}


def spoken(sc):
    t = " ".join(sc["rows"])
    for a, b in SAY.get(sc["id"], []):
        assert a in t, (sc["id"], a)
        t = t.replace(a, b)
    return t


def call(text, prev, nxt):
    key = os.environ["ELEVENLABS_API_KEY"]
    body = json.dumps({"text": text, "model_id": MODEL, "voice_settings": SETTINGS,
                       "previous_text": prev, "next_text": nxt}).encode()
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/with-timestamps?output_format=mp3_44100_128",
        data=body, headers={"xi-api-key": key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read())


def words(text, al):
    ch, st, en = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
    assert "".join(ch) == text, "alignment text mismatch"
    out, k = [], 0
    for w in text.split(" "):
        if w:
            out.append({"text": w, "start": round(st[k], 3), "end": round(en[k + len(w) - 1], 3)})
        k += len(w) + 1
    return out


def main():
    force = "--force" in sys.argv
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    os.makedirs(AUD, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    texts = [spoken(sc) for sc in SCENES]
    total = 0
    for i, sc in enumerate(SCENES):
        sid = sc["id"]
        if only and sid not in only:
            continue
        mp3 = os.path.join(AUD, f"ss_{sid}.mp3")
        aj = os.path.join(OUT, f"{sid}.align.json")
        text = texts[i]
        if force or not (os.path.exists(mp3) and os.path.exists(aj)):
            d = call(text, texts[i - 1] if i else "", texts[i + 1] if i + 1 < len(texts) else "")
            open(mp3, "wb").write(base64.b64decode(d["audio_base64"]))
            json.dump({"text": text, "alignment": d["alignment"]}, open(aj, "w", encoding="utf-8"), ensure_ascii=False)
            total += len(text)
        a = json.load(open(aj, encoding="utf-8"))
        json.dump(words(a["text"], a["alignment"]), open(os.path.join(OUT, f"{sid}.words.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=0)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", mp3, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", "-ac", "1",
                        os.path.join(OUT, f"{sid}.wav")], check=True)
        print(sid, len(text), "chars", a["alignment"]["character_end_times_seconds"][-1], "s")
    print("characters sent:", total)


if __name__ == "__main__":
    if "--count" in sys.argv:
        print(sum(len(spoken(sc)) for sc in SCENES), "characters")
    else:
        main()
