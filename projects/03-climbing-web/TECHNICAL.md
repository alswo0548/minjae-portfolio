# Climbing Web · 구현 포인트

[시연 보기](https://alswo0548.github.io/minjae-portfolio/climbing.html) · [Notion — 기획·화면 설계·개발 과정](https://app.notion.com/p/3de070614e0081cc970cdef56af12c70)

**담당 범위** · 1인 프로젝트로 기획·UI 설계·프론트엔드와 외부 API 연동을 구현한 **웹사이트**입니다.

## 핵심 구현 위치

| 구현 | 원본 프로젝트 파일 · 핵심 처리 |
| --- | --- |
| 클라이밍장 검색·추천 | `js/04_gyms.js` · Kakao Maps·Geocoder 연동, 성향 점수 우선 정렬 및 동점 시 거리 비교 |
| 선수 목록·상세 연결 | `js/05_players.js` · URL의 선수 ID로 해당 페이지 계산 및 강조 표시 |
| 경기 기록 시각화 | `js/06_results.js` · 연도별 메달 집계와 Chart.js 차트 갱신 |
| 장소별 날씨 표현 | `js/04_gyms.js` · OpenWeather 응답에 따른 배경 상태 분기 |

기능 설명·데이터 구조·개발 중 해결한 문제는 위 Notion에 정리했습니다.
