# 글꼴 라이선스·상표 점검 (확정 테마 t5.v02, 2026-11-06)

**결론: 4종 모두 SIL Open Font License 1.1이라 웹사이트에 그대로 써도 라이선스·상표 문제가 없다. 교체할 글꼴은 없다.**

| 글꼴 | 쓰는 곳 | 라이선스 | 저작권자(라이선스 원문) | 예약 글꼴 이름(RFN) | 불러오는 방식 |
|---|---|---|---|---|---|
| Playfair Display | 마스트헤드·제목(`--display`) | OFL 1.1 | The Playfair Display Project Authors (2017) | "Playfair Display" | Google Fonts |
| Source Serif 4 | 본문 세리프(`--serif`) | OFL 1.1 | The Source Serif 4 Project Authors (2014) | 없음 | Google Fonts |
| Noto Serif KR | 한글 제목·본문 세리프 | OFL 1.1 | Google Inc. (2012) | 없음 | Google Fonts |
| Pretendard | 메뉴·라벨 고딕(`--sans`) | OFL 1.1 | Kil Hyung-jin (2021), Adobe, The Inter Project Authors, The M+ FONTS Project Authors | "Pretendard", "Source", "Inter", "M PLUS 1" | jsDelivr(작성자 공식 배포본) |

라이선스 원문:
- google/fonts의 `ofl/playfairdisplay/OFL.txt`, `ofl/sourceserif4/OFL.txt`, `ofl/notoserifkr/OFL.txt`
- orioncactus/pretendard의 `LICENSE`

## 판단 근거
- OFL 1.1은 글꼴을 쓰고, 문서·웹사이트에 넣고, 함께 배포하는 것을 상업적 용도까지 허용한다. 글꼴 파일만 따로 파는 것만 금지한다.
- 예약 글꼴 이름(RFN)은 **글꼴을 고친 파생본**에 원래 이름을 쓰지 못하게 하는 조항이다. 이 사이트는 원본을 이름 그대로 불러다 쓰므로 RFN이나 상표 문제가 생기지 않는다.
- 대체 글꼴로 적은 Georgia, Times New Roman, 나눔명조, 시스템 글꼴은 방문자 컴퓨터에 이미 있는 글꼴을 이름으로 부를 뿐이다. 파일을 배포하지 않으므로 해당 사항이 없다.
- 디자인에 "Science"라는 이름이나 다른 잡지의 로고를 쓰지 않았다. "Science Magazine"은 시안 내부 이름이고 CSS 주석과 시안 목록에만 나온다.

## 나중에 글꼴 파일을 사이트에 직접 넣을 때(선택)
지금은 Google Fonts와 jsDelivr에서 불러온다. 외부 의존을 없애려고 파일을 사이트 안에 넣는다면 다음을 지킨다.
1. **공식 배포 파일을 고치지 않고** 넣는다. Pretendard는 작성자가 배포하는 subset·woff2를, Google 글꼴은 google/fonts 저장소 파일을 쓴다.
   - `pyftsubset` 등으로 직접 서브셋하면 OFL상 파생본(Modified Version)이 된다.
   - 그러면 RFN이 있는 Playfair Display와 Pretendard는 이름을 바꿔야 한다.
2. 각 글꼴의 `OFL.txt`를 글꼴 파일과 같은 폴더에 함께 둔다(OFL 재배포 조건).
3. 직접 넣으면 방문자 IP가 Google·jsDelivr로 전송되지 않는다. 개인정보 측면에서도 조금 낫다.
