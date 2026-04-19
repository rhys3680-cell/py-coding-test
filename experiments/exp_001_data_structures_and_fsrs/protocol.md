# Protocol — exp_001

## 기간
2주 (유연). 성공 기준 달성 시 조기 종료 가능 (exp_000 전례).

## 플랫폼 & 언어
- 프로그래머스
- Python 3

## 문제 선정

### 신규 문제 (Lv.1)
- **자료구조 태그 우선**: 해시 / 스택 / 큐 / 힙 / 정렬 / 완전탐색 / 탐욕법
- exp_000에서 다룬 유형(단순 수학/문자열)은 최소화
- 하루 1~2문제 권장

### 재풀이 문제
- **12931** 자릿수 더하기 (Hard)
- **12932** 자연수 뒤집기 (Hard)
- **12947** 하샤드 수 (Hard)

각 문제 **3일 후 / 7일 후** 2회 재풀이.

## 기록 스키마

### 신규 문제 (기존 스키마 유지)
exp_000 protocol의 스키마와 동일. `stage_attempted`, `patterns_used`, `patterns_missed` 포함.

### 재풀이 문제 (추가 필드)
```json
{
  ...기존 필드...,
  "review_of": "12947",
  "review_round": 1,
  "days_since_previous": 3,
  "grade_previous": "Hard",
  "duration_previous": 9,
  "improvements": "sum(... for ...) 한 번에 사용, 불필요 삼항 제거",
  "remaining_friction": ""
}
```

| 필드 | 설명 |
|---|---|
| `review_of` | 원본 problem_id (예: "12947") |
| `review_round` | 몇 번째 재풀이인지 (1=3일 후, 2=7일 후) |
| `days_since_previous` | 직전 풀이 이후 경과 일수 |
| `grade_previous` / `duration_previous` | 직전 풀이의 등급/시간 |
| `improvements` | 이번에 개선된 점 (자유 메모) |
| `remaining_friction` | 여전히 남은 마찰 |

## 일일 루틴 (권장)

```
1. 복습 큐 확인 (review_queue.md) — 2분
2. 오늘 재풀이 대상 있으면 먼저 수행 — 시간 변동
3. 신규 문제 1~2개 — 시간 변동
4. 기록 업데이트 — 5분
```

### 세션 시작 전 30초 훑기
- `patterns_cheatsheet.md` 훑기 (선택적, 기록은 note에 남기기)

## 종료 기준 (exp_000에서 승계)

### 규칙 A — 시간 역전
동일 적용. "같은 레벨 내 최근 3문제가 V자 반전" 시 종료 신호.

### 최소 달성량 (난이도별)
- Lv.1 신규: 2문제
- 재풀이 only 날: 1건

### 양적/질적 조건 모두 만족 시 실험 종료
- 신규 Lv.1 자료구조 10건 + 재풀이 3건 × 2회 = 총 16건 이상
- 재풀이 중 2건 이상 등급 상승

## 학습 단계 전략 (exp_000 승계)

Stage A/B/C/D 체계 그대로. 자료구조 유형은 **새 도구가 많으므로 초반엔 Stage A로 되돌아갈 수 있음** — 정상이며 관찰 대상.

### FSRS 등급 가이드
exp_000과 동일. Hard를 정직하게 매기기.

## 관찰 포인트

### 재풀이 관련
- 같은 문제에서 **최초 풀이 방식과 재풀이 방식이 달라지는가** (절차적 → 선언적 등)
- **기억 잔존**과 **진짜 학습**의 구분: 2회차 재풀이(7일 후)에서 1회차(3일 후)보다 더 개선되면 진짜 학습

### 자료구조 관련
- **첫 노출**: Counter/defaultdict/deque 본인이 알고 있는지
- **리뷰 후 전이 속도**: exp_000 `sum(... for ...)` 5회 노출보다 빠른가/느린가

## 중단/연장 기준 (exp_000 승계)
- 3일간 로그 0건이면 프로토콜 재검토
- 재풀이 스케줄 하루 이틀 밀려도 OK (간격 오차 큰 실험 아님)
- 2주 후 성공 기준 미달이면 +1주 연장

## 기록 파일

```
experiments/exp_001_data_structures_and_fsrs/
├── hypothesis.md
├── protocol.md               ← 이 파일
├── data.jsonl                ← 신규 + 재풀이 통합
├── review_queue.md           ← 재풀이 일정
├── analysis.md               ← 중간 분석 (필요 시)
└── retrospective.md          ← 종료 후
```