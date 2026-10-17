"""Owner recording → assets/audio/narration.wav + timing.json (see videos/_kit/recording.py).
Cut: the first read of the price line (27.40–32.38 s); the second read is kept."""
import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent / "_kit"))
from recording import process

SCENES = [
    ("s1-hook", "엄마는 한 학기 세 과목 | 아이 학비는 0원? | 사립 컬리지는"),
    ("s2-rule", "자녀무상교육이 안 된다고요? | BC주 기준은 학위 과정이에요 | 사립이라도 학위 과정이면 | 자녀무상교육 대상입니다"),
    ("s3-ac", "알렉산더 컬리지 준학사 | 한 학기 3과목이면 풀타임 | 라이브 온라인 수업도 | 들을 수 있어요"),
    ("s4-eng", "영어는 듀오링고 90점이면 | 조건부 입학으로 바로 시작 | 학비는 한 학기 | 약 5,940 캐나다 달러예요"),
    ("s5-pgwp", "졸업하면 졸업 후 취업비자 | PGWP 최대 3년 | 단, 거주하실 교육청 서류는 | 꼭 미리 확인하세요"),
    ("s6-cta", "밴쿠버 자녀무상교육 | AA캐나다와 상담하세요"),
]
MARKS = {
    "three0": ("s1-hook", "세 과목"), "zero": ("s1-hook", "0원"),
    "priv": ("s1-hook", "사립 컬리지는"), "no": ("s2-rule", "안 된다고요"), "deg": ("s2-rule", "학위 과정이에요"),
    "privdeg": ("s2-rule", "사립이라도"), "free": ("s2-rule", "대상입니다"),
    "ac": ("s3-ac", "알렉산더"), "assoc": ("s3-ac", "준학사"), "three": ("s3-ac", "3과목이면"), "ft": ("s3-ac", "풀타임"), "live": ("s3-ac", "라이브"),
    "duo": ("s4-eng", "듀오링고"), "cond": ("s4-eng", "조건부"), "fee": ("s4-eng", "학비는"), "price": ("s4-eng", "5,940"),
    "grad": ("s5-pgwp", "졸업하면"), "pgwp": ("s5-pgwp", "PGWP"), "check": ("s5-pgwp", "교육청"), "sure": ("s5-pgwp", "꼭 미리"),
    "aa": ("s6-cta", "AA캐나다"),
}
process(ROOT, removes=[(27.40, 32.38)], scenes=SCENES, marks=MARKS, tail=2.6)
