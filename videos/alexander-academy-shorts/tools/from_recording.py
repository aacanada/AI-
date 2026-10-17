"""Owner recording → assets/audio/narration.wav + timing.json (see videos/_kit/recording.py)."""
import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent / "_kit"))
from recording import process

SCENES = [
    ("s1-hook", "고등학생인데 | 대학 과목을 7개나? | 그것도, 추가 학비 없이요"),
    ("s2-school", "밴쿠버 사립고등학교 | 알렉산더 아카데미 | 같은 건물에 있는 | 알렉산더 컬리지 대학 수업을 | 고등학교 때 미리 들을 수 있어요"),
    ("s3-credits", "최대 7과목, 21학점 | 캐나다 대학 1학년이 | 보통 8~10과목을 들으니까 | 1학년 대부분을 | 고등학교 때 미리 끝내는 셈이죠"),
    ("s4-race", "졸업하고 컬리지에서 | 1년 정도 더 공부하고 | UBC 같은 대학으로 편입하면 | 대학 졸업이 | 약 1년 빨라질 수 있어요"),
    ("s5-transfer", "UBC 직행은 내신 싸움이지만 | 편입은 대학 성적으로 평가받아요 | 그리고 졸업장은 | 똑같은 UBC 학위입니다"),
    ("s6-cta", "수능 앞두고 고민 중이시라면 | 1년 늦어지는 게 아니라 | 1년 앞당기는 방법도 있어요 | 밴쿠버 조기유학, | AA캐나다와 상담하세요"),
]
MARKS = {
    "k7": ("s1-hook", "7개나"), "free": ("s1-hook", "추가"),
    "aca": ("s2-school", "알렉산더 아카데미"), "bldg": ("s2-school", "같은 건물"), "col": ("s2-school", "알렉산더 컬리지"), "early": ("s2-school", "미리"),
    "m7": ("s3-credits", "7과목"), "m21": ("s3-credits", "21학점"), "first": ("s3-credits", "캐나다 대학"), "most": ("s3-credits", "대부분"),
    "grad": ("s4-race", "졸업하고"), "yr1": ("s4-race", "1년 정도"), "ubc": ("s4-race", "UBC"), "fast": ("s4-race", "빨라질"),
    "naesin": ("s5-transfer", "내신"), "gpa": ("s5-transfer", "대학 성적"), "same": ("s5-transfer", "똑같은"),
    "late": ("s6-cta", "늦어지는"), "ahead": ("s6-cta", "앞당기는"), "aa": ("s6-cta", "AA캐나다"),
}
process(ROOT, removes=[], scenes=SCENES, marks=MARKS, tail=2.6)
