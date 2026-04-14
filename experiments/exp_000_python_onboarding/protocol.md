# Protocol — exp_000

## 기간
- 7일 (유연, 필요 시 +3일 연장)

## 플랫폼 & 범위
- **프로그래머스**
- 난이도: **Lv.0 ~ Lv.1**
- 언어: **Python 3**

## 일일 배분 (하루 2~3시간 기준)
- **30분** — 파이썬 문법/메서드 학습 ([js_to_python.md](js_to_python.md) 참고)
- **60~90분** — Lv.0~1 문제 풀이 (Python으로)
- **10~20분** — 기록 + 간단 회고 (선택: 막힌 지점 메모)

## 기록 방법

매 문제 풀이가 끝나면 `data.jsonl`에 **한 줄 JSON** 추가.

### 스키마

```json
{
  "date": "2026-04-14",
  "problem_id": "12345",
  "title": "짝수와 홀수",
  "level": 1,
  "started_at": "14:00",
  "solved_at": "14:08",
  "duration_min": 8,
  "first_try_correct": true,
  "saw_solution": false,
  "stuck_point": "",
  "grade": "Good",
  "js_equivalent_known": true,
  "python_specific_friction": "",
  "tags": ["기초", "조건문"],
  "note": ""
}
```

### 필드 설명

| 필드 | 설명 |
|---|---|
| `date` | YYYY-MM-DD |
| `problem_id` | 프로그래머스 문제 번호 |
| `title` | 문제 제목 |
| `level` | 0 또는 1 |
| `started_at` / `solved_at` | HH:MM (로컬) |
| `duration_min` | 총 소요 분 (정수) |
| `first_try_correct` | 첫 제출에서 100점? |
| `saw_solution` | 해설 참고 여부 |
| `stuck_point` | 한 줄 메모 (빈 문자열 가능) |
| `grade` | `Again` / `Hard` / `Good` / `Easy` (주관) |
| `js_equivalent_known` | JS로는 바로 떠올릴 수 있었나? |
| `python_specific_friction` | 파이썬이라서 막힌 지점 (예: "딕셔너리 기본값 처리") |
| `tags` | 자유 태그 (예: `["해시", "구현"]`) |
| `note` | 기타 자유 메모 |

### 등급 기준 (Grade)
- **Again**: 풀었지만 거의 손도 못 댈 뻔했다 / 다시 풀면 또 막힐 듯
- **Hard**: 꽤 고생했다
- **Good**: 무난히 풀었다
- **Easy**: 금방 풀었다

이 등급은 나중 FSRS 적용 시 그대로 입력값으로 씀.

## 주간 회고 (7일 후 `retrospective.md` 작성)

- 푼 문제 수, 레벨별 분포
- 평균 소요시간 (레벨별)
- 퍼스트 트라이 정답률
- 해설 본 비율
- **파이썬 특화 마찰점 Top 3** (빈도 기준)
- 등급 분포
- Lv.2 진입 가능 판단
- 다음 실험(exp_001)에 반영할 것

## 중단/연장 기준
- 3일간 로그 0건이면 프로토콜 재검토 (시간 배분/난이도 조정)
- 7일차에 로그 10건 미달이면 +3일 연장
- 연장 후에도 부족하면 문제 난이도 Lv.0으로 통일 후 재시도
