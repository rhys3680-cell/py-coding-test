# FSRS (Free Spaced Repetition Scheduler)

## 1. 배경 / 왜 나왔나

- **Spaced Repetition(분산 반복)**은 에빙하우스(1885) 이래 "학습 간격을 벌리면 장기기억에 유리하다"는 게 반복 검증됨.
- 1980~90년대 **Piotr Woźniak**이 SuperMemo에서 **SM-2** 알고리즘을 만듦 → Anki의 디폴트 스케줄러가 수십 년간 이걸 씀.
- SM-2의 한계:
  - 간격을 **고정된 배수(EF, Ease Factor)**로 늘림. 사람별/카드별 기억 곡선 차이를 반영 못 함.
  - "기억이 얼마나 남아있는가"를 직접 모델링하지 않고 **간격만** 조절.
  - 과학적 근거보다 경험적 규칙.
- **FSRS (Jarrett Ye, 2022~)**: SM-2를 대체하려고 만든 현대 스케줄러.
  - **기억 연구(ACT-R, New Theory of Disuse)**의 **DSR 모델**을 채택.
  - Anki/Mnemosyne의 **대규모 공개 복습 로그**로 파라미터 피팅.
  - 논문: Ye et al. *A Stochastic Shortest Path Algorithm for Optimizing Spaced Repetition Scheduling* (2023, KDD).
  - Anki 23.10부터 내장(FSRS-4.5), 현재(2024~) FSRS-5 기본값.

## 2. 핵심 아이디어 (직관)

### 2.1 기억 상태를 3개 변수로 모델링 (DSR)

- **D (Difficulty, 어려움)**: 이 카드/문제의 본질적 난이도. 0~10 근처.
- **S (Stability, 안정성)**: 기억이 "얼마나 잘 안 잊히는가". **R이 90% → 100 / e⁰·¹ 일 뒤 90%로 떨어지는 시점까지의 일수**로 해석되는 시간 스케일.
- **R (Retrievability, 인출 가능성)**: 지금 이 순간에 맞출 확률(0~1). 시간 t에 따라 **지수적으로 감쇠**.

### 2.2 기억 감쇠 공식

```
R(t) = (1 + t / (9 × S))^(-1)   (FSRS-5)
```

또는 초기 FSRS-4의 지수형:
```
R(t) = exp(-t / S)
```

- t: 마지막 복습 이후 경과 일수
- S가 클수록 R이 천천히 떨어짐
- **S의 정의**: R이 특정 목표치(FSRS에서는 0.9)에 도달할 때까지의 시간.

### 2.3 복습 후 상태 업데이트

복습할 때 사용자가 4단계 등급을 매김:
- **Again(1)**: 완전히 까먹음 → **lapse**
- **Hard(2)**: 어렵게 떠올림
- **Good(3)**: 보통
- **Easy(4)**: 쉽게 떠올림

복습 후:
- 새로운 S'를 계산 (**stability 업데이트 함수**)
- D'를 계산 (**difficulty 업데이트 함수**)
- 다음 복습 일정: **R이 목표값(기본 0.9)로 떨어지는 시점**

### 2.4 스케줄링 목표

**"지금 복습하지 않으면 잊어버릴 시점 직전에 복습 배치"**.
- R = 0.9 (10% 망각 허용) 기본.
- 너무 이르면: 기억이 공고화되기 전에 복습 → 비효율.
- 너무 늦으면: 잊어버려서 재학습 비용 큼.
- FSRS는 이 최적 시점을 **확률 모델 + 파라미터 피팅**으로 계산.

## 3. 수식 & 유도

FSRS-5 기준(2024년 Anki 공식). 파라미터 벡터 `w = (w0 ... w18)` 총 19개, 사전 훈련된 기본값 있음.

### 3.1 Retrievability

```
R(t, S) = (1 + t / (9 × S))^(-1)
```

- `t = 0 → R = 1`
- `t = 9S → R = 0.5`
- 9가 들어가는 이유: `R(S) = 0.9`가 되도록 정규화한 상수(= (1/0.9 - 1)^(-1) = 9).

### 3.2 초기 Stability & Difficulty (첫 복습)

처음 학습 시 등급 `G ∈ {1,2,3,4}`:
```
S_0(G) = w_{G-1}   # w0..w3: 각 등급별 초기 stability
D_0(G) = w_4 - (G - 3) × w_5   # 난이도 초기값, Good(3)이 기준
D_0(G) = clamp(D_0(G), 1, 10)
```

### 3.3 Stability 업데이트 (복습 성공, G ≥ 2)

```
S'(D, S, R, G) = S × (1 + e^{w_8}
                       × (11 - D)
                       × S^{-w_9}
                       × (e^{w_{10}(1-R)} - 1)
                       × factor(G))
```
여기서 `factor(G)`는:
- Hard(2): `w_{15}`
- Good(3): 1
- Easy(4): `w_{16}`

**의미 해석**:
- `(11 - D)`: 쉬운 카드일수록 stability 더 크게 증가.
- `S^{-w_9}`: 이미 stability 큰 카드는 추가 증가가 작음 (포화).
- `(e^{w_{10}(1-R)} - 1)`: **R이 낮을수록(거의 잊을 뻔한 상태에서 복습할수록) 증가량 큼** → "**desirable difficulty**" (Bjork) 원리를 수식에 직접 반영.
- factor(G): Hard면 덜 증가, Easy면 더.

### 3.4 Stability 업데이트 (lapse, G = 1)

```
S'_fail = w_{11}
          × D^{-w_{12}}
          × ((S + 1)^{w_{13}} - 1)
          × e^{w_{14}(1-R)}
```

- 잊어버리면 stability가 **급격히 감소** (보통 직전 S의 몇십 %).

### 3.5 Difficulty 업데이트

```
D_new = D - w_6 × (G - 3)        # 원점 이동: Easy면 D 감소, Again이면 증가
D'    = w_7 × D_init(4) + (1 - w_7) × D_new   # 평균회귀 (mean reversion)
D'    = clamp(D', 1, 10)
```

D가 너무 극단으로 가는 걸 막기 위한 **평균회귀** 항이 핵심.

### 3.6 다음 복습 간격

목표 retrievability `R_target` (기본 0.9)에 도달하는 시간:

```
I = 9 × S × (1/R_target - 1)
```

즉 `R_target = 0.9` → `I = S`. **stability가 곧 "90% 기억 유지 간격"**.

### 3.7 파라미터 피팅

- **입력**: 유저의 복습 로그 `[(카드 id, 시점 t, 등급 G, 이전 간격, ...)]`.
- **우도**: 각 복습에서 예측한 R과 실제 성공/실패의 로지스틱 우도.
- **최적화**: Adam/PyTorch 경사하강, 혹은 L-BFGS. 19차원 파라미터 공간.
- **정규화**: 기본 w를 prior로 두고 L2로 끌어당김(개인 데이터 적을 때 shrinkage).
- Anki는 유저의 누적 로그로 **자동 재피팅** 기능 제공.

## 4. 예제 계산

**상황**: 새 카드를 처음 학습. Good(3)으로 응답.

기본 파라미터(FSRS-5 사전 훈련값 예시):
```
w = [0.40, 0.90, 2.30, 10.9, 4.93, 0.94, 0.86, 0.01, 1.49, 0.14,
     0.94, 2.18, 0.05, 0.34, 1.26, 0.29, 2.61, 0.40, 0.60]
```

### 4.1 첫 복습 (G=3, Good)
```
S_0 = w_2 = 2.30일
D_0 = w_4 - (3 - 3) × w_5 = 4.93
```
→ 다음 복습: `I = 9 × 2.30 × (1/0.9 - 1) = 2.30일` 후 (R=0.9 유지).

### 4.2 2.3일 뒤 복습, 또 Good
현재 R(2.3, 2.30) = (1 + 2.3/(9×2.30))⁻¹ = 1/1.111 = **0.9** (정확히 목표치).

Stability 업데이트 (G=3, factor=1):
```
S' = 2.30 × (1 + e^{1.49} × (11 - 4.93) × 2.30^{-0.14}
             × (e^{0.94 × 0.1} - 1) × 1)
   = 2.30 × (1 + 4.437 × 6.07 × 0.890 × (1.0987 - 1))
   = 2.30 × (1 + 4.437 × 6.07 × 0.890 × 0.0987)
   = 2.30 × (1 + 2.366)
   ≈ 7.74일
```

Difficulty 업데이트:
```
D_new = 4.93 - 0.86 × 0 = 4.93
D'    = 0.01 × 4.93 + 0.99 × 4.93 = 4.93  # 변화 없음 (Good = 기준)
```

→ 다음 복습: 약 **7.7일 후**.

### 4.3 7.7일 뒤, Hard(2)
R은 여전히 0.9에 수렴. Hard라 factor=w_{15}=0.29 적용 → S' 증가폭이 Good 대비 약 1/3.
```
S' ≈ 7.74 × (1 + (기존 항들) × 0.29)
```
대략 S' ≈ 12~13일 수준. Good이었다면 25~30일 갈 수 있었던 것.

**관찰**: 등급 하나 차이가 장기적으로 **누적 간격을 크게 벌리거나 좁힘**. 그래서 Anki 사용자들이 등급 기준을 일관되게 잡는 게 중요.

## 5. 파이썬 최소 구현 (FSRS-5 핵심만)

```python
import math
from dataclasses import dataclass


# 기본 파라미터 (FSRS-5 사전 훈련 예시값)
DEFAULT_W = [
    0.40, 0.90, 2.30, 10.9, 4.93, 0.94, 0.86, 0.01, 1.49, 0.14,
    0.94, 2.18, 0.05, 0.34, 1.26, 0.29, 2.61, 0.40, 0.60,
]

R_TARGET = 0.9


@dataclass
class CardState:
    stability: float
    difficulty: float
    last_review_day: float  # 절대 일수 (t=0 기준)


def retrievability(elapsed_days: float, stability: float) -> float:
    return (1 + elapsed_days / (9 * stability)) ** -1


def init_state(grade: int, w: list[float] = DEFAULT_W) -> CardState:
    """첫 복습 직후 상태."""
    s0 = w[grade - 1]
    d0 = w[4] - (grade - 3) * w[5]
    d0 = max(1.0, min(10.0, d0))
    return CardState(stability=s0, difficulty=d0, last_review_day=0.0)


def next_stability_success(
    d: float, s: float, r: float, grade: int, w: list[float] = DEFAULT_W
) -> float:
    factor = {2: w[15], 3: 1.0, 4: w[16]}[grade]
    hard_penalty = factor
    delta = (
        math.exp(w[8])
        * (11 - d)
        * (s ** -w[9])
        * (math.exp(w[10] * (1 - r)) - 1)
        * hard_penalty
    )
    return s * (1 + delta)


def next_stability_lapse(d: float, s: float, r: float, w: list[float] = DEFAULT_W) -> float:
    return (
        w[11]
        * (d ** -w[12])
        * ((s + 1) ** w[13] - 1)
        * math.exp(w[14] * (1 - r))
    )


def next_difficulty(d: float, grade: int, w: list[float] = DEFAULT_W) -> float:
    d_new = d - w[6] * (grade - 3)
    d_init_easy = w[4] - (4 - 3) * w[5]
    d_prime = w[7] * d_init_easy + (1 - w[7]) * d_new
    return max(1.0, min(10.0, d_prime))


def review(state: CardState, now_day: float, grade: int, w: list[float] = DEFAULT_W) -> CardState:
    elapsed = now_day - state.last_review_day
    r = retrievability(elapsed, state.stability)
    if grade == 1:
        new_s = next_stability_lapse(state.difficulty, state.stability, r, w)
    else:
        new_s = next_stability_success(state.difficulty, state.stability, r, grade, w)
    new_d = next_difficulty(state.difficulty, grade, w)
    return CardState(stability=new_s, difficulty=new_d, last_review_day=now_day)


def next_interval(state: CardState, r_target: float = R_TARGET) -> float:
    return 9 * state.stability * (1 / r_target - 1)


if __name__ == "__main__":
    # 새 카드, Good으로 시작
    s = init_state(grade=3)
    print(f"t=0  S={s.stability:.2f} D={s.difficulty:.2f} → 다음 {next_interval(s):.2f}일")

    # 2.3일 뒤 Good
    s = review(s, now_day=2.3, grade=3)
    print(f"t=2.3 S={s.stability:.2f} D={s.difficulty:.2f} → 다음 {next_interval(s):.2f}일")

    # 그 간격 뒤 Hard
    t2 = s.last_review_day + next_interval(s)
    s = review(s, now_day=t2, grade=2)
    print(f"t={t2:.2f} S={s.stability:.2f} D={s.difficulty:.2f} → 다음 {next_interval(s):.2f}일")
```

실제 공식 구현은 [open-spaced-repetition/py-fsrs](https://github.com/open-spaced-repetition/py-fsrs) 사용 추천. 위 코드는 **이해를 위한 핵심 발췌**.

## 6. 한계 / 언제 안 맞나

1. **DSR 모델 자체의 단순화**
   - 기억을 3개 스칼라로 압축. 실제 기억은 **계층적/연관 네트워크**(한 카드를 보면 다른 카드 기억이 같이 강화되는 **간섭/촉진**)를 모델링 못 함.
2. **등급의 주관성**
   - Good/Hard 기준이 사람마다, 날마다 다름 → 파라미터 피팅 품질이 등급 일관성에 의존.
3. **카드 성격 의존**
   - 간단한 단어 암기엔 잘 맞지만, **풀이 과정이 긴 코테 문제**(개념 이해 vs 구현력이 섞임)에선 "1회 복습 = 1이벤트"로 두는 게 적절한지 자체가 질문.
4. **파라미터 피팅에 로그량 필요**
   - 최소 수백 건의 복습 로그가 있어야 개인 파라미터가 기본값보다 나아짐. 초반엔 default 쓰고 누적되면 재피팅.
5. **목표 R 트레이드오프**
   - R_target을 0.9 → 0.95로 올리면 **복습량 폭증**. 학습 시간 예산과 망각 허용치 사이 튜닝 필요.
6. **"연관 학습"엔 BKT/DKT가 더 적합**
   - "DP 개념 전체의 숙달도"는 카드 단위 FSRS보단 유형 단위 지식 추적이 어울림.

## 7. 코딩테스트 학습에 적용 가능한 부분

### 7.1 오답노트 = FSRS 카드
- 각 **틀린 문제**를 카드로 등록.
- 다시 풀 때 Again/Hard/Good/Easy로 등급.
- FSRS가 재풀이 시점 추천.
- → 전통적인 "1일/3일/1주일" 고정 스케줄보다 훨씬 정교.

### 7.2 개념 카드도 별도 관리
- **"다익스트라 구현"**, **"LIS 점화식"** 같은 **개념 단위 카드**.
- 빈 에디터에서 구현 → 등급. Retrieval practice + FSRS 스케줄.

### 7.3 목표 R을 문제 성격에 맞게 튜닝
- **시험 임박기**: R_target = 0.95 (망각 최소화, 복습량 많음)
- **평소**: 0.9
- **탐색기(새 개념 많이 배우는 중)**: 0.85 (복습 부담 줄이고 신규 우선)

### 7.4 파라미터 피팅은 나중에
- 처음 몇 달은 **기본 w**로 충분. 로그가 1000개쯤 쌓이면 재피팅.
- 재피팅은 py-fsrs의 optimizer 사용 (PyTorch 의존).

### 7.5 자동화 포인트
- **입력**: 문제 id, 복습 시점, 등급
- **출력**: 다음 복습 일자 (CSV/JSON)
- cron + 간단 스크립트로 "오늘 복습할 문제 리스트" 매일 생성 가능.

## 8. 참고자료

- Ye, J., Su, J., Cao, Y. (2023). *A Stochastic Shortest Path Algorithm for Optimizing Spaced Repetition Scheduling*. KDD 2023. — FSRS 공식 논문
- [open-spaced-repetition (GitHub org)](https://github.com/open-spaced-repetition) — py-fsrs, rs-fsrs 등 공식 구현
- [FSRS4Anki Wiki](https://github.com/open-spaced-repetition/fsrs4anki/wiki) — 알고리즘 상세 설명 (FSRS-4.5 / FSRS-5 수식 모두)
- Bjork, R. A. (1994). *Memory and metamemory considerations in the training of human beings*. — "desirable difficulty" 원전
- Settles, B., & Meeder, B. (2016). *A Trainable Spaced Repetition Model for Language Learning*. ACL. — Duolingo의 Half-Life Regression, FSRS와 비교 대상
- Wozniak, P. (1990). *Optimization of learning*. — SM-2 원전, 역사적 맥락
- [Anki FSRS 설명서](https://docs.ankiweb.net/deck-options.html#fsrs) — 실전 사용 레퍼런스
