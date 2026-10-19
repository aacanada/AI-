# publish/ — 게시 대기함

Claude Code가 완성한 영상을 올리고, 어사이드가 예약 확인으로 읽어서 게시합니다.
이 폴더는 `publish` 브랜치에서만 관리합니다.

## 폴더 하나 = 게시 묶음 하나

```
publish/YYYY-MM-DD-<이름>/
  video.mp4         최종 영상 (용량이 크면 아래 "큰 영상" 규칙대로 나눠서 올림)
  thumbnail.jpg     썸네일
  upload-text.txt   [유튜브 제목] / [유튜브 설명] / [인스타 캡션]
  meta.txt          채널, 공개 범위, 게시 순서, 연결할 본편 폴더
  READY             Claude Code가 모든 파일을 올린 뒤 마지막 커밋으로 만듦
  published.md      어사이드가 게시 후 채널별 링크를 적음
```

## 규칙

1. `READY` 가 없는 폴더는 아직 준비 중입니다. 게시하지 않습니다.
2. `published.md` 가 있는 폴더는 이미 게시된 것입니다. 건너뜁니다.
3. 게시 전에 각 채널에 같은 글이 이미 있는지 확인합니다 (중복 게시 방지).
4. `meta.txt` 의 `linked_to` 가 있으면, 그 폴더의 `published.md` 에 본편 주소가 생긴 뒤에 게시하고 관련 동영상으로 연결합니다.
5. `visibility: public` 은 바로 공개 게시입니다.
6. `publish_after: YYYY-MM-DD` — 이 날짜(KST) 전에는 게시하지 않음 (예약 게시). `meta.txt` 에 이 줄이 있으면 그 날짜가 될 때까지 건너뜁니다.

## 큰 영상 (90MB 초과)

GitHub는 파일 하나에 100MB까지만 받기 때문에, 큰 영상은 나눠서 올립니다.

```
video.mp4.part-aa, video.mp4.part-ab, ...   90MB 단위 조각
video.mp4.sha256                            합친 뒤 확인용 체크섬
```

- 나누기 (Claude Code): `split -b 90m -d video.mp4 video.mp4.part-` 후 `sha256sum video.mp4 > video.mp4.sha256`
- 합치기 (어사이드): 조각을 이름 순서대로 이어 붙여 `video.mp4` 를 만들고 (`cat video.mp4.part-* > video.mp4`), `sha256sum -c video.mp4.sha256` 이 OK일 때만 게시합니다.
- `meta.txt` 의 `files:` 에 조각 수를 적습니다 (예: `video.mp4 = 3 parts`).
