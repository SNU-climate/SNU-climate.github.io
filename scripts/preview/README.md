# claude.ai 미리보기(artifact) 빌드 도구

artifact 한 개에는 파일을 511개까지만 넣을 수 있다. 그래서 공지·앨범은 최근 글만 넣고, 테마마다 복사되는 `static/`과 `assets/shared/`를 루트 한 곳에 모은다. 여러 테마를 넣으면 페이지 아래쪽에 시안 전환 막대를 넣는다.
결과물은 `site/`가 아닌 스크래치 폴더에 만들고, 원본 데이터는 바꾸지 않는다. 다른 작업과 섞이지 않게 `git archive HEAD`로 뽑은 스냅숏에서 빌드한다.
**게시 전에 반드시 `git pull`로 GitHub 최신본을 받고, 커밋하지 않은 변경이 없는 상태에서 스냅숏을 뜬다.** 아티팩트는 하나라서, 오래된 복사본으로 게시하면 다른 사람이 반영한 페이지를 옛 내용으로 덮어쓴다. 게시 담당은 관리자 한 명으로 정한다(`HANDOVER.md` 미리보기 관리). 확정 시안 1개 모드는 화면 캡처(`site/_shots`)가 필요 없다.

| 스크립트 | 용도 | 게시한 artifact |
|---|---|---|
| `preview_family.py <스냅숏> <출력> <공지 수> <앨범 수> <전체 목록 URL> <계열 이름> <테마...>` | 계열 하나의 v01·v02(첫 화면 포함) | 계열별 9개(아래) |
| `preview_family.py <스냅숏> <출력> 99 9 <전체 목록 URL> 'Science Magazine v02' t5.v02` | 확정 시안 1개(테마 1개 모드: 전환 막대·카드 없이 artifact 첫 화면이 곧 사이트 홈). 공지는 전부, 앨범은 파일 505개 이하가 되게 | 확정 시안 https://claude.ai/artifact/DY6yy4sVdjhcwagM9XHjQD |
| `linkcheck.py <출력>` | 출력 폴더 안 상대 링크 검사 | — |
| `diff_preview.py <이전 출력> <새 출력> [--json]` | 두 미리보기를 비교해 다시 게시할 파일(changed·added·removed) 목록. 날짜 표시만 다른 HTML은 제외 | — |

이전 시안 artifact(2026-11-04, 테마 폴더는 2026-11-11에 삭제, 공지 10편·앨범 8개): Basic 42dn4KBdXePsxkrdcWen1h · Classic B2dq9P7exJx691zUrLXbqX · Minimal RbsU8RYiPNsZwezBfxUopf · Ocean LZe2TmNi6oTgCMm2HaJYvG · Dashboard 93S7w5j1y4zuhnfTpGKAuh · Magazine N3Mt1GmAi58tNBquYJFx5S · Sidebar 2ERDxAyQX6M1pWszKojSTE · One-page 5zz8DYr4xhK6twHQAeKMRD · Globe 71xFcCrVjmSvTGZt2CqUaK (모두 `https://claude.ai/artifact/<ID>`).
미리보기는 페이지마다 `window.CSL_NO_EMBED=true`를 넣어, artifact가 막는 유튜브 iframe 대신 재생 버튼이 YouTube 새 탭 링크가 되게 한다.
확정 시안 미리보기에는 버튼이 두 개 있다.
둘 다 미리보기의 `shared/shared.js` 끝에 붙는 조각이라, 버튼만 고칠 때는 `index.html`과 `shared/shared.js`만 다시 게시하면 된다.
- **의견 남기기**(`FEEDBACK_HTML`, `FEEDBACK_JS`): 누르면 고르기 상태(빨간 커서, 마우스가 올라간 부분에 빨간 테두리)가 되고, 그 상태에서 누른 부분이나 드래그한 글자에 claude.ai 댓글 창을 연다. Esc나 버튼을 다시 누르면 취소. 댓글 창이 닫히면(Esc·게시) claude.ai의 댓글 모드도 함께 끝낸다(`customAnchors`의 `exitMode`. 쓰던 글이 남아 있으면 claude.ai가 모드를 유지한다).
- **사진 보내기**(`UPLOAD_HTML`, `UPLOAD_JS`): 사진을 artifact 자산으로 올리고 db `uploads`에 `{assetId, filename, note, page, title, uploader, time, sizeBytes, contentType, done}`을 남긴다.
- 게시할 때 capabilities는 `{"comments": {"composer_only": true, "customAnchors": true}, "assets": {"upload": "interact"}, "db": {}, "user": {}}`. capabilities를 넘기면 전체가 바뀌므로 넷을 모두 적는다(생략하면 이전 선언 유지).
- 올라온 사진은 `Artifact list`(scope `assets`)와 `ArtifactData list`(collection `uploads`)로 확인하고 `Artifact read`(path에 자산 id)로 내려받는다. 반영한 행은 `done: true`로 바꾼다.

테마가 자체 호스팅하는 글꼴(`assets/fonts`, 140여 개)은 미리보기에서 빼고 Google Fonts 링크로 바꾼다(파일 수 한도).
게시는 한 번에 255개 항목까지라 두 번에 나눠 올린다. 내용이 안 바뀐 파일은 다시 올리지 않아도 된다(보낸 파일만 바뀌고 나머지는 유지). 같은 URL을 다시 올릴 때는 이전에만 있던 경로를 `null`로 지워야 한다.

**바뀐 페이지만 다시 게시하기**(매일 자동 갱신과 "미리보기 갱신해 줘"가 쓰는 순서)
1. 마지막 게시 커밋(비공개 리뷰 기록 저장소 `SNU-climate/homepage-reviews`의 `preview_state.json`)과 `origin/main`을 각각 `git archive`로 풀어 `preview_family.py`로 두 벌을 만든다.
2. `linkcheck.py <새 출력>`이 0인지 확인한다.
3. `diff_preview.py <이전> <새>`로 고른 파일만 같은 주소에 게시한다(없어진 파일은 `null`). capabilities는 넘기지 않는다.
4. `preview_state.json`의 `published_commit`과 `artifact_version`을 갱신한다.
