# GoodDeedQuest · 코드와 구현 근거

[시연 보기](https://alswo0548.github.io/minjae-portfolio/gdq.html) · [Notion — 기획·아키텍처·개발 과정](https://app.notion.com/p/3dc070614e0081428b5ce28f1200007c) · [팀 원본 저장소](https://github.com/QuestismTeam/GoodDeedQuest)

**담당 범위** · 5인 팀의 Community·Team·Admin 백엔드와 AI 팀원 추천 API를 중심으로 구현했습니다.

## 코드에서 확인할 부분

| 구현 | 코드와 변경 이력 |
| --- | --- |
| 개인화 커뮤니티 피드: 관심사·지역·최신성 등의 규칙 점수 계산 | [점수 로직](https://github.com/QuestismTeam/GoodDeedQuest/blob/dev/backend/app/community/scoring.py) · [PR #204](https://github.com/QuestismTeam/GoodDeedQuest/pull/204) |
| 팀원 추천: 후보 점수·순위와 LLM 추천 이유 생성 분리 | [AI 추천 노드](https://github.com/QuestismTeam/GoodDeedQuest/blob/dev/ai/app/challenge_recommend/nodes.py) · [PR #219](https://github.com/QuestismTeam/GoodDeedQuest/pull/219) |
| 관리자 기능: 운영 통계·사용자·신고 처리 | [관리자 서비스](https://github.com/QuestismTeam/GoodDeedQuest/blob/dev/backend/app/admin/service.py) · [PR #249](https://github.com/QuestismTeam/GoodDeedQuest/pull/249) |

> **추천 방식** · 후보 선정·순위는 규칙 기반으로 결정하고, LLM은 설명 문구 생성에 활용합니다. 기능 흐름과 트러블슈팅은 위 Notion에서 확인할 수 있습니다.
