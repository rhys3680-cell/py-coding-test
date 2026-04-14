# BKT (Bayesian Knowledge Tracing)

## 1. 배경 / 왜 나왔나

- **Albert Corbett & John Anderson** (1995, CMU)이 지능형 튜터링 시스템 **ACT-R 기반 Cognitive Tutor**에서 제안.
- 문제: "학생이 **개념(skill)**을 숙달했는지" 단순 정답률으로는 못 잼. 운 좋게 맞을 수도, 알면서 실수할 수도 있음.
- 해법: 개념 숙달을 **숨겨진 이진 상태(모름/앎)**로 두고, 관측(정답/오답)에서 **베이즈 추론**으로 숙달 확률 추정.
- 구조적으로는 **2-state Hidden Markov Model**.
- Khan Academy, DuoLingo 초기, 여러 MOOC 튜터에 30년간 표준으로 사용. 이후 **DKT(Deep KT, 2015)** 등 딥러닝 버전이 SOTA지만, **해석 가능성/단순성** 때문에 BKT는 여전히 살아있음.

## 2. 핵심 아이디어 (직관)

각 **개념(skill)**마다 HMM 하나:

```
숨김 상태: L ∈ {아직 못 배움(0), 숙달(1)}
관측: 정답 또는 오답

            P(T)
      ┌────────────┐
      │            ↓
[L=0 Not Learned]  [L=1 Learned]
      │                ↑
      └ 한 번 숙달하면 복귀 X (BKT 기본 가정)
```

**4개 파라미터**만으로 모든 걸 설명:

| 파라미터 | 의미 | 범위 |
|---|---|---|
| `P(L₀)` | 처음부터 알고 있을 확률 (사전 숙달) | [0, 1] |
| `P(T)` | 한 번 연습하면 **Not Learned → Learned**로 **전이**할 확률 | [0, 1] |
| `P(G)` | 모르는데 **Guess**로 맞출 확률 | [0, 0.5] 권장 (너무 크면 이상) |
| `P(S)` | 아는데 **Slip**으로 틀릴 확률 | [0, 0.5] |

각 문제를 풀 때마다:
1. **정답/오답 관측** → 숙달 확률 `P(L_n)`을 베이즈로 업데이트
2. **연습 효과** → `P(T)`만큼 추가로 숙달 확률 증가

## 3. 수식 & 유도

### 3.1 한 문제 풀이 후 업데이트

n번째 문제에서 정답/오답을 봤을 때:

**관측이 정답(correct)**:
```
P(L_n | correct) = P(L_n) × (1 - P(S))
                  ÷ [P(L_n) × (1 - P(S)) + (1 - P(L_n)) × P(G)]
```

**관측이 오답(incorrect)**:
```
P(L_n | incorrect) = P(L_n) × P(S)
                    ÷ [P(L_n) × P(S) + (1 - P(L_n)) × (1 - P(G))]
```

이건 그냥 **베이즈 정리**:
```
P(L | 관측) = P(관측 | L) × P(L) / P(관측)
```

- `P(correct | L=1) = 1 - P(S)` (아는데 안 미끄러질 확률)
- `P(correct | L=0) = P(G)` (모르는데 찍어서 맞을 확률)

### 3.2 연습에 의한 전이

관측 반영 후 **연습으로 숙달이 진행**되는 효과:
```
P(L_{n+1}) = P(L_n | 관측) + (1 - P(L_n | 관측)) × P(T)
```

즉 "이미 숙달했거나, 아직 숙달 못했지만 이번 연습으로 전이될 확률".

### 3.3 다음 문제의 정답 예측

```
P(correct_{n+1}) = P(L_{n+1}) × (1 - P(S)) + (1 - P(L_{n+1})) × P(G)
```

→ 학습 시스템이 **"이 학생이 이 개념 문제를 맞출 확률"**을 예측할 때 사용.

### 3.4 파라미터 추정

**입력**: 여러 학생의 [개념 k에 대한 정/오답 시퀀스] 데이터.

방법 1: **EM 알고리즘** (표준).
- E-step: 현재 파라미터로 각 시점의 P(L_n) 계산
- M-step: 로그우도 최대화하도록 4개 파라미터 갱신
- 반복 수렴까지

방법 2: **그리드/경사하강** — 차원이 4개뿐이라 의외로 grid search도 가능.

**제약**:
- 식별성(identifiability) 문제로 `P(G) + P(S) < 1` 같은 조건 부과해야 수렴 안정.
- Beck & Chang (2007): `P(G) ≤ 0.3, P(S) ≤ 0.1` 클램핑이 경험적으로 잘 동작.

### 3.5 확장: Individualized BKT

기본 BKT는 **개념별 파라미터는 있지만 학생별 파라미터는 없음**. 확장:
- **P(L₀)를 학생별로** 분리 → 사전 지식 차이 반영
- **P(T)를 학생별로** → 학습 속도 차이 반영
- Yudelson et al. (2013): 학생별 P(L₀) + P(T) 조합이 가장 좋은 적합도

### 3.6 DKT와의 차이

- BKT: 개념별 독립 HMM. 4개 파라미터.
- DKT (Piech 2015): **LSTM**이 모든 개념 간 상관까지 학습. 수천~수만 파라미터.
- DKT가 예측 정확도는 더 높지만 **해석 불가** ("숙달도가 몇 %야?"에 답 못 함).
- 소규모/해석 필요하면 BKT, 대규모/예측 우선이면 DKT.

## 4. 예제 계산

**설정**: 한 개념에 대해
- P(L₀) = 0.1 (초반 10%만 알 것)
- P(T) = 0.3 (연습당 30% 숙달 전이)
- P(G) = 0.2, P(S) = 0.1

학생이 문제 4개를 풂: **오, 정, 정, 정**.

### Step 1: 문제 1, 오답
```
P(L_1) = 0.1
P(L_1 | incorrect) = 0.1 × 0.1 / (0.1 × 0.1 + 0.9 × 0.8)
                   = 0.01 / 0.73
                   ≈ 0.0137
P(L_2) = 0.0137 + (1 - 0.0137) × 0.3
       = 0.0137 + 0.296
       ≈ 0.3097
```
→ 틀렸지만 연습 효과로 숙달확률이 오히려 올라감 (0.1 → 0.31).

### Step 2: 문제 2, 정답
```
P(L_2 | correct) = 0.3097 × 0.9 / (0.3097 × 0.9 + 0.6903 × 0.2)
                 = 0.2787 / (0.2787 + 0.1381)
                 = 0.2787 / 0.4168
                 ≈ 0.669
P(L_3) = 0.669 + 0.331 × 0.3 ≈ 0.768
```

### Step 3: 문제 3, 정답
```
P(L_3 | correct) = 0.768 × 0.9 / (0.768 × 0.9 + 0.232 × 0.2)
                 = 0.6912 / 0.7376
                 ≈ 0.937
P(L_4) = 0.937 + 0.063 × 0.3 ≈ 0.956
```

### Step 4: 문제 4, 정답
```
P(L_4 | correct) = 0.956 × 0.9 / (0.956 × 0.9 + 0.044 × 0.2)
                 ≈ 0.9898
P(L_5) ≈ 0.9898 + 0.01 × 0.3 ≈ 0.993
```

**해석**: 4문제 만에 숙달 확률 **0.1 → 0.99**. 틀린 첫 문제가 오히려 정보 많이 제공 → 이후 정답 연속으로 빠르게 수렴.

## 5. 파이썬 최소 구현

```python
from dataclasses import dataclass


@dataclass
class BKTParams:
    p_L0: float = 0.1
    p_T: float = 0.3
    p_G: float = 0.2
    p_S: float = 0.1


def update_after_response(p_L: float, correct: bool, params: BKTParams) -> float:
    """관측(정/오답)을 본 뒤의 숙달 확률 (전이 적용 전)."""
    if correct:
        num = p_L * (1 - params.p_S)
        den = p_L * (1 - params.p_S) + (1 - p_L) * params.p_G
    else:
        num = p_L * params.p_S
        den = p_L * params.p_S + (1 - p_L) * (1 - params.p_G)
    return num / den


def apply_transition(p_L_posterior: float, params: BKTParams) -> float:
    """연습에 의한 Not Learned → Learned 전이."""
    return p_L_posterior + (1 - p_L_posterior) * params.p_T


def predict_correct(p_L: float, params: BKTParams) -> float:
    """다음 문제 정답 확률."""
    return p_L * (1 - params.p_S) + (1 - p_L) * params.p_G


def trace(responses: list[bool], params: BKTParams) -> list[float]:
    """각 문제 직전의 숙달 확률 P(L_n) 시퀀스."""
    p_L = params.p_L0
    history = [p_L]
    for r in responses:
        p_L_post = update_after_response(p_L, r, params)
        p_L = apply_transition(p_L_post, params)
        history.append(p_L)
    return history


if __name__ == "__main__":
    params = BKTParams()
    responses = [False, True, True, True]
    hist = trace(responses, params)
    for i, p in enumerate(hist):
        print(f"문제 {i}번 직전 P(L) = {p:.4f}")
    print(f"다음 정답 예측 확률 = {predict_correct(hist[-1], params):.4f}")
```

파라미터 피팅은 **pyBKT** (github.com/CAHLR/pyBKT, UC Berkeley) 라이브러리가 표준.

## 6. 한계 / 언제 안 맞나

1. **이진 숙달 가정**
   - "모름(0) vs 숙달(1)" 둘뿐. 실제로는 **부분 이해**가 존재.
   - 3-state BKT 확장 있지만 식별성 더 나빠짐.

2. **Forgetting 없음 (기본 모델)**
   - 한 번 숙달하면 안 잊는다고 가정 → 현실과 불일치.
   - **BKT with forgetting**: 전이를 양방향으로 + P(F) 추가. 그러나 식별성·해석 복잡해짐.
   - → **FSRS와 결합**하면 자연스럽게 해결: BKT로 개념 숙달, FSRS로 망각 관리.

3. **개념별 독립 가정**
   - 다익스트라를 알면 BFS도 잘하는 식의 **개념 간 전이**를 못 잡음.
   - → DKT, DKVMN 같은 신경망 KT가 해결.

4. **P(G), P(S) 과적합**
   - 자유 방임하면 "아는데 항상 틀리고, 모르는데 항상 맞춘다" 같은 **degenerate 해**로 수렴.
   - 실전에선 제약/정규화 필수.

5. **개별 학생 특성 반영 약함**
   - 기본 BKT는 모든 학생이 같은 P(L₀), P(T) 가정. 개별화 확장 필요.

6. **"문제 난이도"가 없음**
   - 같은 개념의 쉬운 문제와 어려운 문제를 구분 못 함.
   - → KT + IRT 결합 모델(IKT) 연구 다수.

## 7. 코딩테스트 학습에 적용 가능한 부분

### 7.1 개념 단위 숙달도 추적
- 코테 **알고리즘 유형 각각을 "개념"**으로 취급:
  - DP, 그래프 기본, 다익스트라, 이분탐색, 백트래킹, 세그먼트트리 등.
- 유형별로 BKT 인스턴스 하나씩.
- "DP 숙달도 85%, 세그먼트트리 20%" 같은 해석 가능한 지표가 나옴.

### 7.2 "다음에 뭘 풀지" 추천
- `P(correct_{n+1})`을 유형별로 계산.
- 너무 쉬운 것(>0.9), 너무 어려운 것(<0.3)은 제외, 중간 난이도(0.5~0.8) 추천.
- CAT의 Fisher 정보 기준과 유사한 직관.

### 7.3 FSRS와 역할 분담
| | BKT | FSRS |
|---|---|---|
| 단위 | 개념(skill) | 카드(card) |
| 추적 | 숙달도 (0~1) | 기억 강도 (S, D) |
| 질문 | "이 개념 알아?" | "이 카드 언제 다시 볼까?" |
| 시간 | 기본 없음 | 핵심 변수 |

→ **개념 숙달은 BKT, 문제 복습은 FSRS**로 같이 돌리면 보완적.

### 7.4 파라미터 초기값 제안 (감각)
코테 학습 맥락에서 시작값 예시:
- P(L₀) = 0.05 (새 유형은 대부분 모름)
- P(T) = 0.15 (한 문제 푼다고 금방 숙달은 아님, 코테는 느림)
- P(G) = 0.1 (코테는 찍어 맞추기 어려움. 객관식 아니니 낮게)
- P(S) = 0.15 (실수·시간부족으로 틀리는 비율)

유저 로그 쌓이면 pyBKT로 재피팅.

### 7.5 언제 BKT가 과할까
- 개념 수가 너무 적으면(5개 미만) 그냥 **유형별 정답률**만으로 충분.
- 데이터 규모가 아주 작으면(유형당 풀이 10회 미만) 파라미터 추정 불안정 → 기본값 고정.

## 8. 참고자료

- Corbett, A. T., & Anderson, J. R. (1995). *Knowledge Tracing: Modeling the Acquisition of Procedural Knowledge*. User Modeling and User-Adapted Interaction. — **원전**
- Yudelson, M. V., Koedinger, K. R., Gordon, G. J. (2013). *Individualized Bayesian Knowledge Tracing Models*. AIED. — 학생별 파라미터 확장
- Beck, J. E., & Chang, K. (2007). *Identifiability: A Fundamental Problem of Student Modeling*. UMAP. — P(G)/P(S) 제약 논의
- Piech, C. et al. (2015). *Deep Knowledge Tracing*. NeurIPS. — DKT 원전, BKT 비교
- Pardos, Z. A., & Heffernan, N. T. (2011). *KT-IDEM: Introducing Item Difficulty to the Knowledge Tracing Model*. UMAP. — KT+문제난이도 결합
- [pyBKT (UC Berkeley CAHLR)](https://github.com/CAHLR/pyBKT) — 파이썬 표준 구현
- Khan, S. et al. (2016). *Cognitive Modeling of Learning Using Bayesian Knowledge Tracing*. — Khan Academy 적용 리뷰
