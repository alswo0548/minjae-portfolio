# OCTV · 코드와 구현 근거

[시연 보기](https://alswo0548.github.io/minjae-portfolio/octv.html) · [Notion — 기획·아키텍처·개발 과정](https://app.notion.com/p/99ac34c55d37838bae8f81588467f52f) · [원본 저장소](https://github.com/alswo0548/octv)

**담당 범위** · 2인 팀에서 사건 저장·조회와 판단·대응 백엔드, 외부 정보 연동, 위험도·기관·경로 추천, 비동기 알림과 통합·배포를 담당했습니다. CCTV 환경 적응학습에도 참여했으며, **YOLO 탐지·시간 검증·사건화의 주요 구현은 팀원 담당**입니다.

## 코드에서 확인할 부분

| 구현 | 코드와 변경 이력 |
| --- | --- |
| 사건 저장·조회: 중복 사건 관리와 최신 탐지 시각 갱신 | [사건 서비스](https://github.com/alswo0548/octv/blob/main/backend/app/incidents/service.py) · [PR #12](https://github.com/alswo0548/octv/pull/12) |
| 사건 분석: 외부 맥락 → 위험도·우선순위 → 기관·경로 → 저장 | [LangGraph 파이프라인](https://github.com/alswo0548/octv/blob/main/ai/orchestration/pipeline.py) · [PR #19](https://github.com/alswo0548/octv/pull/19) |
| 기관 추천: 역할·지역·경로 접근성 반영 | [추천 로직](https://github.com/alswo0548/octv/blob/main/ai/agency_recommendation/recommender.py) · [PR #30](https://github.com/alswo0548/octv/pull/30) |
| 비동기 분석·알림: 작업 큐, 재시도 및 실패 대상 처리 | [Celery 워커](https://github.com/alswo0548/octv/blob/main/backend/app/workers.py) · [알림 서비스](https://github.com/alswo0548/octv/blob/main/backend/app/notifications/service.py) · [PR #23](https://github.com/alswo0548/octv/pull/23) |

> **구현 범위** · 관제 담당자의 대응 판단과 기관 전달을 지원하는 서비스이며, 실제 출동 지령·현장 조치 완료까지 자동화하지는 않습니다. 설계와 문제 해결의 상세 설명은 위 Notion에 정리했습니다.
