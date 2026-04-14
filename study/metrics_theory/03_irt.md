# IRT (Item Response Theory, 문항반응이론)

## 1. 배경 / 왜 나왔나

- 1950~60년대 **심리측정학(psychometrics)** 분야에서 고전검사이론(CTT, Classical Test Theory)의 한계를 넘으려고 개발.
- CTT의 문제:
  - 시험 점수 = **이 시험에 한정된** 숫자. 다른 시험과 직접 비교 불가.
  - 문제 난이도도 "정답률"로만 측정 → 누가 풀었느냐에 따라 값이 흔들림.
- IRT의 핵심 전환: **사람 실력 θ와 문제 난이도 b를 동시에, 표본과 독립적으로 추정**.
- 대표 개발자: **Georg Rasch**(1960, 덴마크 수학자 — Rasch 모델 = 1PL), **Frederic Lord & Allan Birnbaum**(1960~70s, 2PL/3PL 일반화).
- 현재 적용:
  - **TOEFL, SAT, GRE, TOEIC** — 대부분 2PL/3PL IRT 기반 (CAT = Computer Adaptive Testing).
  - **solved.ac 티어 산정** — 공식 블로그에 "IRT 기반" 명시.
  - **교육용 AI 튜터** — Knowledge Tracing의 이론적 뿌리.

## 2. 핵심 아이디어 (직관)

ELO가 **사람 vs 사람**이라면 IRT는 **사람 vs 문제**.

- 사람마다 실력 파라미터 `θ` (theta, 보통 평균 0 표준편차 1의 표준정규 스케일).
- 문제마다 난이도 파라미터 `b`.
- **어떤 사람이 어떤 문제를 맞출 확률은 (θ - b)의 함수**.
- 실력이 난이도보다 딱 같으면 50%, 크게 높으면 100%에 가까이, 낮으면 0%에 가까이.

이 관계를 그린 곡선을 **ICC (Item Characteristic Curve, 문항특성곡선)**이라고 함 — S자 로지스틱.

추가로:
- **변별도 a** — "이 문제가 실력 차이를 얼마나 잘 가르는가". 급한 S자면 a 큼.
- **추측도 c** — "찍어도 맞을 확률". 객관식 5지선다면 c ≈ 0.2.

## 3. 수식 & 유도

### 3.1 1PL 모델 (Rasch)

```
P(정답 | θ, b) = σ(θ - b) = 1 / (1 + e^(-(θ - b)))
```

- 파라미터: θ(사람), b(문제) 각각 하나씩.
- 모든 문제가 같은 변별도를 가진다는 강한 가정.
- **장점**: 극도로 단순, 파라미터 추정 안정적, 해석 쉬움.
- ELO와의 관계:
  - ELO는 `1/(1 + 10^((R_B-R_A)/400))`.
  - 1PL은 `1/(1 + e^(-(θ-b)))`.
  - 스케일만 다름. R = 400θ/ln10 + 1500 같은 선형 변환으로 맞출 수 있음.
  - **ELO는 사실상 1PL의 동적 온라인 업데이트 버전**.

### 3.2 2PL 모델

```
P(정답 | θ, b, a) = σ(a × (θ - b))
```

- 변별도 `a` 추가.
- `a`가 크면 ICC가 가파름 → θ가 b 근처에서 급격히 승률이 변함 → "실력 경계를 잘 가르는 문제".
- `a`가 작으면 ICC가 완만 → 실력 상관없이 엇비슷한 승률 → "구분력 낮은 문제".
- **a ≤ 0인 문제는 폐기** (실력이 높을수록 더 틀리는 문제 = 망한 문제).

### 3.3 3PL 모델

```
P(정답) = c + (1 - c) × σ(a × (θ - b))
```

- 추측도 `c` 추가.
- θ → -∞일 때 P → c (하한). 즉 "아무리 못해도 c 확률로는 맞음".
- **객관식 시험**에 적합. 코딩테스트처럼 풀이를 써야 하는 시험엔 c ≈ 0이라 2PL이면 충분.

### 3.4 파라미터 추정 (MLE 개요)

N명의 사람, M개의 문제, 응답 행렬 `U (N×M)` = {0, 1}. 추정 대상: `θ_1..θ_N, a_1..a_M, b_1..b_M`.

**로그 우도**:
```
L(θ, a, b) = Σ_i Σ_j [u_ij × log(P_ij) + (1 - u_ij) × log(1 - P_ij)]
```
여기서 `P_ij = σ(a_j × (θ_i - b_j))` (2PL).

풀이 방법:
1. **JMLE (Joint MLE)**: θ와 (a,b)를 번갈아 고정하며 최적화. 단순하지만 편향 존재.
2. **MMLE (Marginal MLE)**: θ를 사전분포 N(0,1)로 주고 적분해 소거, (a,b)만 MLE → EM 알고리즘. 가장 표준적.
3. **Bayesian (MCMC, Variational)**: 사전분포 명시, 사후분포 샘플링. 현대적 대규모에 유리.

solved.ac 같은 실제 시스템은 문제 수/유저 수가 수만 단위라 **MMLE 또는 근사 Bayesian**으로 돌림.

### 3.5 CAT (Computer Adaptive Testing)

IRT의 실전 응용. 시험 도중 **다음 문제를 동적 선택**:
- 현재까지의 응답으로 θ 추정치 갱신.
- 다음 문제는 **Fisher 정보량**(I(θ) = a² × P × (1-P))이 최대인 문제 = 지금 실력에서 가장 구분력 있는 문제.
- 기대 θ의 표준오차가 임계값 이하로 내려가면 종료.

→ TOEFL/GRE가 이렇게 동작. 학습 시스템에도 직접 응용 가능: **"지금 나한테 가장 정보 많은 다음 문제"를 추천**.

## 4. 예제 계산

### 4.1 ICC 감 잡기 (2PL)

b=0, a=1 문제를 가정:
- θ = -2 → σ(1×(-2 - 0)) = σ(-2) ≈ 0.119
- θ = 0 → σ(0) = 0.5
- θ = 1 → σ(1) ≈ 0.731
- θ = 2 → σ(2) ≈ 0.881

b=0, a=2 (더 가파른 문제):
- θ = -1 → σ(-2) ≈ 0.119
- θ = 0 → 0.5
- θ = 1 → σ(2) ≈ 0.881

→ a가 크면 θ가 b 근처에서 승률이 **훨씬 빨리 변함**.

### 4.2 θ 추정 (수동)

내가 3개 문제를 풂:
- 문제1: b=-1, a=1, **정답**
- 문제2: b=0, a=1, **정답**
- 문제3: b=1, a=1, **오답**

θ 후보들의 로그우도:
```
L(θ) = log σ(θ+1) + log σ(θ) + log(1 - σ(θ-1))
```

| θ | σ(θ+1) | σ(θ) | 1-σ(θ-1) | L(θ) |
|---|---|---|---|---|
| -1 | 0.5 | 0.269 | 0.881 | -2.155 |
| 0 | 0.731 | 0.5 | 0.731 | -1.326 |
| 0.5 | 0.818 | 0.622 | 0.622 | -1.156 |
| 1 | 0.881 | 0.731 | 0.5 | -1.134 |
| 1.5 | 0.924 | 0.818 | 0.378 | -1.257 |

→ θ ≈ **1** 근처가 최대. 직관적 — "b=1 근처 문제에서 막힘".

### 4.3 CAT 예시

현재 θ 추정 = 0.5, RD(표준오차) 큼. 다음 문제 후보:
- Q_easy: b=-1, a=1 → I(0.5) = 1² × 0.818 × 0.182 ≈ **0.149**
- Q_mid: b=0.5, a=1 → I(0.5) = 1² × 0.5 × 0.5 = **0.25**
- Q_hard: b=2, a=1 → I(0.5) = 1² × 0.182 × 0.818 ≈ **0.149**

→ **b = 현재 θ와 같은 문제가 정보량 최대**. "딱 내 수준 문제"가 가장 유익하다는 직관의 수학적 근거.

## 5. 파이썬 최소 구현 (2PL, 단일 사용자 θ 추정)

```python
import math


def p_correct(theta: float, b: float, a: float = 1.0) -> float:
    return 1.0 / (1.0 + math.exp(-a * (theta - b)))


def log_likelihood(theta: float, items: list[tuple[float, float, int]]) -> float:
    """items: [(b, a, u), ...] where u in {0,1}."""
    ll = 0.0
    for b, a, u in items:
        p = p_correct(theta, b, a)
        ll += u * math.log(p) + (1 - u) * math.log(1 - p)
    return ll


def estimate_theta(
    items: list[tuple[float, float, int]],
    lo: float = -4.0,
    hi: float = 4.0,
    iters: int = 40,
) -> float:
    """그리드 + 이분탐색으로 θ MLE 근사."""
    # 격자 탐색으로 대충 위치 잡기
    best, best_ll = 0.0, -math.inf
    for i in range(101):
        t = lo + (hi - lo) * i / 100
        ll = log_likelihood(t, items)
        if ll > best_ll:
            best, best_ll = t, ll
    # 주변 세밀 탐색
    step = (hi - lo) / 100
    for _ in range(iters):
        step /= 2
        for t in (best - step, best + step):
            ll = log_likelihood(t, items)
            if ll > best_ll:
                best, best_ll = t, ll
    return best


def fisher_info(theta: float, b: float, a: float = 1.0) -> float:
    p = p_correct(theta, b, a)
    return a**2 * p * (1 - p)


def next_item_cat(theta_hat: float, pool: list[tuple[float, float]]) -> tuple[float, float]:
    """현재 θ 추정에서 정보량 최대 문제 반환. pool: [(b, a), ...]."""
    return max(pool, key=lambda ba: fisher_info(theta_hat, ba[0], ba[1]))


if __name__ == "__main__":
    items = [(-1, 1, 1), (0, 1, 1), (1, 1, 0)]
    theta = estimate_theta(items)
    print(f"θ 추정: {theta:.3f}")  # ≈ 1.0

    pool = [(-1, 1), (0.5, 1), (2, 1)]
    b, a = next_item_cat(theta_hat=0.5, pool=pool)
    print(f"다음 문제: b={b}, a={a}")  # b=0.5
```

전체 IRT (문제 파라미터까지 동시 추정)는 `pyirt`, `girth` 같은 라이브러리 사용이 현실적.

## 6. 한계 / 언제 안 맞나

1. **IID 가정 (independence)**
   - 문제끼리 독립이라는 가정. 실제로는 **같은 주제 문제끼리 상관** 있음 — DP 하나 풀면 비슷한 DP 줄줄이 풀리는 현상.
   - → 다차원 IRT(MIRT), Knowledge Tracing으로 보완.

2. **단일 차원(unidimensional) 가정**
   - θ 하나로 모든 문제를 설명. "DP는 잘하는데 그래프는 약한 사람"을 잘 표현 못 함.
   - → MIRT(여러 θ) 혹은 유형별 별도 모델.

3. **파라미터 추정에 대량 데이터 필요**
   - 2PL은 문제당 보통 **수백 명 이상** 풀이 기록 필요. 신규 문제는 추정 불안정.
   - → 베이지안 prior로 완화 가능.

4. **실력이 시간에 따라 변한다는 걸 못 반영**
   - IRT는 기본적으로 정적(snapshot) 모델. 학습 효과를 반영하려면 **Knowledge Tracing**이나 **Dynamic IRT** 필요.

5. **변별도/추측도 해석 주의**
   - a가 음수로 추정되면 문제 설계 이상 (실력 높을수록 더 틀림) — 데이터 클리닝 필요.
   - c는 객관식에만 의미. 코딩테스트엔 거의 0.

## 7. 코딩테스트 학습에 적용 가능한 부분

### 7.1 solved.ac 티어를 이해하는 프레임
- 문제의 티어(b)는 수많은 유저 풀이 데이터로 IRT 추정된 값.
- 내 티어(θ)는 어떤 b의 문제를 얼마나 맞추냐로 역산.
- **"내 티어 = 50% 정답률 근처 b"**가 직관적 해석 (Rasch 기준).

### 7.2 "내 수준 문제"를 정확히 고르기
- CAT 아이디어: **b ≈ θ_hat** 문제가 정보량 최대.
- "너무 쉽거나 너무 어려운 문제는 실력 측정/성장에 덜 유용"의 수학적 근거.
- **약점 유형**을 찾으려면 그 유형의 문제만으로 서브 θ를 추정해 전체 θ와 비교.

### 7.3 내 풀이 로그로 2PL 돌리기
- 플랫폼 난이도 b를 고정값으로 신뢰하면, 내 풀이만 가지고 θ 추정이 단순 로지스틱 회귀가 됨.
- `scikit-learn`의 `LogisticRegression`으로 몇 줄로 구현 가능:
  ```python
  # X = 문제 특성(b만 쓴다면 (θ - b) 꼴로), y = 정/오답
  # 절편 = θ로 해석
  ```

### 7.4 한계도 기억하기
- 학습 효과 있는 상황이라 **정적 IRT는 부정확**. 시간에 따른 θ 변화를 보려면 **기간별로 쪼개서** 추정하거나 Knowledge Tracing.
- 유형 편향 있으니 **전체 θ 하나로 만족하지 말고 유형별 θ** 병행 추천.

## 8. 참고자료

- Rasch, G. (1960). *Probabilistic Models for Some Intelligence and Attainment Tests*. — 1PL 원전
- Birnbaum, A. (1968). *Some Latent Trait Models and Their Use in Inferring an Examinee's Ability*. In Lord & Novick, *Statistical Theories of Mental Test Scores*. — 2PL/3PL 기초
- Embretson, S. E., & Reise, S. P. (2000). *Item Response Theory for Psychologists*. — 입문 교재 추천
- [solved.ac 티어 산정 공식 문서](https://solvedac.github.io/unofficial-documentation/rating.html) — IRT 적용 실제 사례
- [pyirt GitHub](https://github.com/17zuoye/pyirt) — 파이썬 IRT 라이브러리
- [girth GitHub](https://eribean.github.io/girth/) — 현대적 파이썬 IRT (MMLE, Bayesian)
- Baker, F. B., & Kim, S.-H. (2004). *Item Response Theory: Parameter Estimation Techniques*. — 추정 알고리즘 레퍼런스
