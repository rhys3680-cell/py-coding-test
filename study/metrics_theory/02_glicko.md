# Glicko / Glicko-2

## 1. 배경 / 왜 나왔나

- **Mark Glickman** (하버드 통계학자)이 1995년 논문 *A Comprehensive Guide to Chess Ratings*에서 ELO의 근본 한계를 지적하며 제안.
- ELO의 핵심 문제: **"레이팅이 얼마나 믿을 만한지"를 표현 못 함.**
  - 3경기 둔 1500과 300경기 둔 1500을 동일 취급.
  - 1년 쉰 사람과 매일 두는 사람을 동일 취급.
- Glicko의 해법: 레이팅을 **점 추정치가 아니라 확률 분포**로 본다. 평균(R)과 함께 **표준편차 RD(Rating Deviation)**를 관리.
- 2012년 Glicko-2로 확장 — **변동성(volatility σ)** 추가, 실력이 불안정한 플레이어를 더 잘 포착.
- **LeetCode Contest Rating이 Glicko 계열**(엄밀히는 Glicko-like 커스텀). 체스닷컴도 Glicko 사용.

## 2. 핵심 아이디어 (직관)

ELO가 "내 실력 = 1600"이라고 말한다면, Glicko는 **"내 실력은 평균 1600, 표준편차 ±80"**라고 말함.

세 가지 추가 개념:

1. **RD (Rating Deviation)**: 레이팅의 불확실성. 크면 "아직 잘 모름", 작으면 "꽤 확신함".
   - 신규 유저 → RD 큼 (보통 350 시작)
   - 자주 두는 고인물 → RD 작음 (50 근처 수렴)
   - **안 두고 쉬면 RD가 다시 커진다** — 실력이 그사이 변했을 수 있으니까.

2. **업데이트가 RD에 따라 달라진다**
   - 내 RD가 크면 → 내 레이팅이 많이 움직임 (자신 없으니 새 정보 많이 반영)
   - 상대 RD가 크면 → 내 레이팅이 **덜** 움직임 (상대 실력이 불확실해서 정보량이 적음)

3. **변동성 σ (Glicko-2)**: "내 실력 자체가 얼마나 요동치는가". 급성장/급하락 플레이어는 σ가 커지고, 그러면 RD 감소 속도가 느려짐.

비유: ELO는 "너 실력은 1600이야"라고 단정. Glicko는 **"너 실력은 1600쯤인 것 같은데 확신은 ±80이야"**라고 말하고, 두면 둘수록 ±가 좁아짐.

## 3. 수식 & 유도

Glicko(1999년 버전)를 먼저, Glicko-2는 뒤에.

### 3.1 Glicko: 기대 승률

플레이어 A가 B를 만났을 때:

```
g(RD_B) = 1 / sqrt(1 + 3q² × RD_B² / π²)
E(A|B) = 1 / (1 + 10^(-g(RD_B) × (R_A - R_B) / 400))
```

- `q = ln(10) / 400 ≈ 0.00575` (ELO와 같은 스케일)
- `g(RD_B)` = **상대 불확실성 감쇠 함수**. RD_B가 크면 g가 작아져 기대 승률이 0.5 쪽으로 끌려감 ("모르는 상대면 예측도 보수적으로").

> `g`의 유도: 로지스틱(실력 차이에 대한 승률)을 **상대 실력이 정규분포로 퍼져있다고 가정**한 상태에서 적분 근사. π²/3이 로지스틱과 정규의 분산 비례 상수. (Glickman 1999, Appendix A)

### 3.2 Glicko: 업데이트

한 rating period 동안 m개 경기(상대 j=1..m, 레이팅 R_j, RD_j, 결과 s_j)를 했다고 가정.

**1. 분산 추정 d²**
```
d² = 1 / (q² × Σ g(RD_j)² × E_j × (1 - E_j))
```
여기서 `E_j = E(A|j)`. d²는 이번 기간 관측에서 얻은 **정보량의 역수** — 분산이 작을수록 정보 많음.

**2. 새 RD**
```
RD' = sqrt(1 / (1/RD² + 1/d²))
```
두 분산을 합치는 정밀도(precision) 방식. **기존 불확실성과 새 정보를 확률적으로 결합**.

**3. 새 레이팅**
```
R' = R + q / (1/RD² + 1/d²) × Σ g(RD_j) × (s_j - E_j)
```
ELO와 같은 "실제 - 기대" 구조인데, **가중치가 1/(1/RD² + 1/d²)로 동적**.

**4. 경기 없는 기간의 RD 증가**
```
RD_new = min(sqrt(RD² + c²), 350)
```
`c`는 "실력이 얼마나 빨리 낡는가" 상수. 경기를 안 두면 RD가 서서히 커지다가 350(초기값)에서 포화.

### 3.3 Glicko-2의 추가점: 변동성 σ

Glicko-2는 "RD가 변하는 속도"도 데이터로 추정. 급성장/급하락 플레이어는 σ가 커짐.

전체 알고리즘은 반복 수치해법(Newton-like)으로 σ를 업데이트 — 여기선 개념만.

핵심 차이:
- 스케일 변환: R을 `μ = (R-1500)/173.7178`, RD를 `φ = RD/173.7178`로 내부 변환 (자연로그 스케일)
- **변동성 업데이트**:
  ```
  σ' = solve for σ in:
     f(x) = (e^x × (Δ² - φ² - v - e^x)) / (2(φ² + v + e^x)²) - (x - ln σ²) / τ² = 0
  ```
  여기서 v = 관측 분산, Δ = 관측 평균 변화, τ = 시스템 상수(0.3~1.2, 대회 성격에 따라).
- 이 σ가 다음 기간의 φ 증가량을 조절: `φ* = sqrt(φ² + σ'²)`

실전 구현은 논문 pseudocode(Glickman 2012)를 그대로 옮기는 게 정석.

## 4. 예제 계산

**상황**: 내 레이팅 R=1500, RD=200. 한 rating period에 1경기만 했음.
- 상대: R_j=1400, RD_j=30, 결과 s_j=1 (내가 이김)

### 4.1 g와 E

```
g(30) = 1 / sqrt(1 + 3 × 0.00575² × 30² / π²)
      = 1 / sqrt(1 + 3 × 3.31e-5 × 900 / 9.87)
      = 1 / sqrt(1 + 0.00905)
      ≈ 0.9955

E = 1 / (1 + 10^(-0.9955 × (1500 - 1400) / 400))
  = 1 / (1 + 10^(-0.2489))
  = 1 / (1 + 0.5638)
  ≈ 0.6395
```
→ 기대 승률 약 64%.

### 4.2 d²
```
d² = 1 / (0.00575² × 0.9955² × 0.6395 × 0.3605)
   = 1 / (3.31e-5 × 0.991 × 0.2306)
   = 1 / 7.57e-6
   ≈ 132,100
d  ≈ 363.5
```

### 4.3 새 RD
```
1/RD² + 1/d² = 1/40000 + 1/132100
             = 2.5e-5 + 7.57e-6
             = 3.257e-5
RD' = sqrt(1 / 3.257e-5) ≈ 175.3
```
RD가 200 → 175로 줄었음. "한 경기 둬서 조금 더 확신 생김."

### 4.4 새 레이팅
```
R' = 1500 + 0.00575 / 3.257e-5 × 0.9955 × (1 - 0.6395)
   = 1500 + 176.6 × 0.9955 × 0.3605
   = 1500 + 63.4
   ≈ 1563.4
```

**관찰**: 같은 상황을 ELO(K=32)로 풀면 변동이 약 +11.5점. Glicko는 **RD가 크니 더 크게 움직였다** (+63). 신규/오랜만에 돌아온 유저의 레이팅이 빨리 수렴하는 이유.

## 5. 파이썬 최소 구현 (Glicko, 단일 rating period)

```python
import math

Q = math.log(10) / 400  # ≈ 0.00575


def g(rd: float) -> float:
    return 1.0 / math.sqrt(1 + 3 * Q**2 * rd**2 / math.pi**2)


def expected(r: float, r_j: float, rd_j: float) -> float:
    return 1.0 / (1 + 10 ** (-g(rd_j) * (r - r_j) / 400))


def update_glicko(
    r: float,
    rd: float,
    opponents: list[tuple[float, float, float]],  # [(r_j, rd_j, s_j), ...]
) -> tuple[float, float]:
    if not opponents:
        return r, min(math.sqrt(rd**2 + 34**2), 350)  # c≈34, 예시값

    d2_inv = 0.0
    delta = 0.0
    for r_j, rd_j, s_j in opponents:
        e_j = expected(r, r_j, rd_j)
        g_j = g(rd_j)
        d2_inv += Q**2 * g_j**2 * e_j * (1 - e_j)
        delta += g_j * (s_j - e_j)

    precision = 1.0 / rd**2 + d2_inv
    r_new = r + Q / precision * delta
    rd_new = math.sqrt(1.0 / precision)
    return r_new, rd_new


if __name__ == "__main__":
    # 예제 4의 상황 재현
    r_new, rd_new = update_glicko(1500, 200, [(1400, 30, 1)])
    print(f"R: 1500 -> {r_new:.1f}")
    print(f"RD: 200 -> {rd_new:.1f}")
    # R: 1500 -> 1563.4
    # RD: 200 -> 175.3
```

Glicko-2 전체 구현은 **Glickman의 2012 pseudocode**를 참고 — 반복 해법 때문에 짧게 못 줄임.

## 6. 한계 / 언제 안 맞나

1. **Rating period 개념의 부담**
   - Glicko는 원래 **일정 기간(주/월)을 묶어** 한 번에 업데이트하는 모델. 실시간 경기마다 업데이트는 근사적.
   - 코딩테스트 플랫폼은 "대회 끝나면 즉시 업데이트"가 자연 → Glicko-2가 그래서 더 잘 맞음.

2. **c 상수와 τ의 임의성**
   - 실력 낡는 속도(c), 시스템 변동성(τ)은 **도메인마다 튜닝** 필요. 이론이 값을 알려주진 않음.

3. **여전히 1대1 모델**
   - 팀전/다인전 → TrueSkill.

4. **문제풀이엔 부적합**
   - ELO와 같은 한계. 상대가 사람일 때만 말이 됨.
   - "나 vs 문제"에 억지로 쓰면 문제 RD를 0에 가깝게 둬야 하는데, 그러면 Glicko의 장점이 사라짐.

5. **계산 복잡도**
   - Glicko-2는 수치 해법 있어서 ELO보다 무거움. 대규모 실시간 시스템에선 캐싱/배치 필요.

## 7. 코딩테스트 학습에 적용 가능한 부분

### 7.1 내 실력 추정에 "신뢰도" 붙이기
- 한 달 쉬었다면 RD 증가 → "지금 내 레이팅은 변했을 수 있음"을 모델이 알려줌.
- 개인 학습 로그에서 **"최근 문제 밀도"**를 RD처럼 쓸 수 있음.

### 7.2 문제 난이도의 불확실성
- solved.ac 티어도 사실 RD가 있음(문제마다 풀이 표본 수가 다름).
- 신규 문제 = 난이도 RD 큼 → 이 문제를 풀거나 틀린 정보는 내 레이팅 업데이트에 **덜** 반영해야 공정.

### 7.3 유형별 RD
- DP는 자주 풀어서 RD 작음, 그래프는 안 풀어서 RD 큼.
- **RD가 큰 유형을 우선 학습**하는 전략 — 정보 이득이 가장 큰 영역을 공략.

### 7.4 언제 Glicko가 ELO보다 명확히 낫나
- 학습 빈도가 **들쭉날쭉**할 때.
- 표본 크기가 **작을 때** (신규 유저).
- 유형별 분리해서 봐야 할 때 (유형마다 표본 차이가 큼).

## 8. 참고자료

- Glickman, M. E. (1995). *A Comprehensive Guide to Chess Ratings*. — 원전, ELO 한계 분석
- Glickman, M. E. (1999). *Parameter estimation in large dynamic paired comparison experiments*. Applied Statistics. — Glicko 공식 논문
- Glickman, M. E. (2012). *Example of the Glicko-2 system*. — 공식 구현 pseudocode, **Glicko-2 구현 시 1순위 참고**
- [Glickman's official page](http://www.glicko.net/glicko.html) — 논문 PDF 직접 다운로드 가능
- [LeetCode Contest Rating 공식 설명](https://leetcode.com/discuss/general-discussion/468851/new-contest-rating-algorithm-coming-soon) — 실제 적용 케이스
- [Wikipedia: Glicko rating system](https://en.wikipedia.org/wiki/Glicko_rating_system)
