# 몬트리올 개요 상담 영상 (HyperFrames)

원장님 녹음(`plans/montreal-overview/audio/mtl_clean.flac`) + 전 화면 그래픽, 16:9 1920×1080 30fps, 5:04.5.
유튜브 **일부 공개** 전용. 숏폼·publish 큐 없음.

## 구조
- `tools/build.py` → `index.html`, `timing.json`, 폰트 서브셋, `compositions/region.html` 생성
  - `tools/scenes_a.py` 장면 01~14, `tools/scenes_b.py` 장면 15~27, `tools/common.py` 디자인 시스템(메이플 레드)
  - 장면 JS의 시간은 **편집본 음성 기준 시각**이고 `A(t)`가 앞 여백 0.5초를 더한다. 큐는 `TRANSCRIPT_clean.json` 단어 타임스탬프에서 잡았다.
  - 자막: `build.py`의 `CAPS` (SCRIPT.txt 문구, `{...}` = 레드 강조), 타이밍은 단어 타임스탬프로 자동 배분.
  - 셰이더 전환: `@hyperframes/shader-transitions` (`SHADERS` 목록, 장면 경계마다 0.7초).
- `tools/region.py` → `compositions/region.html` (지역 장면, 03:24~03:45) — **별도 서브컴포지션**
- `tools/geo.py` → `assets/geo/geo.json` (Natural Earth에서 캐나다 주 경계·몬트리올 섬 경로)
- `tools/thumb.py` → `thumbnail/thumbnail.png` (1280×720)
- 최종 믹스: 렌더러가 +2.9dB를 더해 -13.3 LUFS로 나와서, 렌더 후 오디오만 -2.9dB 조정(영상 스트림 복사) → -16.2 LUFS, TP -3.9.
- 오디오: `assets/audio/narration.m4a` = mtl_clean.flac에 highpass 70Hz + afftdn(nr 8) + loudnorm I=-16 (v2 편집본 294.98초, 측정 -16.3 LUFS). 말 속도 변경 없음. BGM은 버논 롱폼 bgm-a/b, 내레이션보다 약 22dB 낮게(×0.08), 엔드카드에서 살짝 올림.

```bash
python3 -I tools/build.py      # 재생성 (FONT_SRC=<BlackHanSans.ttf, NotoSansKR.ttf 있는 폴더>)
npx hyperframes check
npx hyperframes render -o renders/video.mp4
```

## 원장님 제공 이미지
`plans/montreal-overview/assets/owner/` → `python3 -I tools/owner_img.py` → `assets/img/owner/` (팝업용 조각 + rects.json).
지역 장면은 원장님 지도로 교체 완료. 아래는 처음 교체 절차(참고용).
## v2 오디오
편집본 v2에서 283.00~286.45초(3.45초)를 잘라냄. 장면 큐는 v1 시각으로 적혀 있고 `A()`(JS)와 `V()`(build.py)가 283초 이후를 3.45초 앞당긴다. 자막은 v2 TRANSCRIPT를 그대로 쓴다.

## 지역 장면 교체 (원장님 A~D 지도가 오면)
지금 지역 장면은 실제 지형(몬트리올 섬 윤곽, 다운타운 위치)만 그리고, A·B·C·D는 지도 위에 놓지 않은 카드로만 보여 준다.
1. 지도 이미지를 `assets/img/region-map.png`로 넣는다.
2. `tools/region.py`의 `#rg-map` 안 `<svg>…</svg>`를 `<img src="assets/img/region-map.png" style="width:1000px">`로 바꾸고, 섬 그리기 트윈(`isl`)을 지운다. A~D 카드를 지도 위 위치로 옮기려면 `.rg-card`의 left/top만 고친다.
3. `python3 -I tools/build.py` → `npx hyperframes render`. 장면 길이(21.5초)와 다른 장면은 그대로다.
