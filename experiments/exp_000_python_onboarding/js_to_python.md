# JS → Python 매핑 (코테 관점)

JS 능숙자가 파이썬으로 코테 풀 때 **자주 걸리는 지점** 위주.

## 1. 기본 문법

| 개념 | JavaScript | Python |
|---|---|---|
| 변수 선언 | `let x = 1;` / `const x = 1;` | `x = 1` (선언 키워드 없음) |
| 문장 끝 | 세미콜론 `;` (선택) | 줄바꿈 (세미콜론 X) |
| 블록 | `{ }` | **들여쓰기 (4칸 권장)** |
| 주석 | `//`, `/* */` | `#`, `""" """` |
| 논리 | `&&`, `\|\|`, `!` | `and`, `or`, `not` |
| 동등 | `===` | `==` (파이썬은 ===  없음) |
| null | `null`, `undefined` | `None` |
| bool | `true` / `false` | `True` / `False` (대문자) |
| 타입 체크 | `typeof x` | `type(x)` / `isinstance(x, int)` |
| 문자열 템플릿 | `` `hello ${name}` `` | `f"hello {name}"` |
| 삼항 | `a ? b : c` | `b if a else c` |
| 거짓값 | `0, "", null, undefined, NaN` | `0, "", None, [], {}, set()` |

## 2. 반복/분기

```javascript
// JS
for (let i = 0; i < n; i++) { ... }
for (const x of arr) { ... }
for (const [i, x] of arr.entries()) { ... }
arr.forEach(x => ...);
```

```python
# Python
for i in range(n): ...
for x in arr: ...
for i, x in enumerate(arr): ...
# forEach는 그냥 for문. 부작용 루프는 컴프리헨션으로 안 씀.
```

while은 거의 동일.

`break`, `continue` 동일. 단 파이썬엔 `for...else`도 있음 (break 안 되고 끝나면 else 실행).

## 3. 배열 ↔ 리스트

| 동작 | JS | Python |
|---|---|---|
| 생성 | `[1,2,3]` | `[1,2,3]` |
| 길이 | `arr.length` | `len(arr)` |
| 추가 | `arr.push(x)` | `arr.append(x)` |
| 뒤에서 빼기 | `arr.pop()` | `arr.pop()` |
| 앞에 추가 | `arr.unshift(x)` | `arr.insert(0, x)` (O(n)) / **`collections.deque` 사용** |
| 앞에서 빼기 | `arr.shift()` | `arr.pop(0)` (O(n)) / deque `popleft()` |
| 슬라이스 | `arr.slice(1, 3)` | `arr[1:3]` |
| 역순 | `arr.slice().reverse()` | `arr[::-1]` (새 리스트) / `arr.reverse()` (in-place) |
| 연결 | `a.concat(b)` / `[...a, ...b]` | `a + b` |
| 포함 | `arr.includes(x)` | `x in arr` |
| 인덱스 | `arr.indexOf(x)` | `arr.index(x)` (없으면 예외) |
| 정렬 | `arr.sort((a,b)=>a-b)` | `arr.sort()` / `sorted(arr)` |
| key 정렬 | `arr.sort((a,b)=>a.x-b.x)` | `sorted(arr, key=lambda v: v.x)` |
| 역정렬 | `.sort((a,b)=>b-a)` | `sorted(arr, reverse=True)` |
| map | `arr.map(x => x*2)` | `[x*2 for x in arr]` / `list(map(lambda x: x*2, arr))` |
| filter | `arr.filter(x => x>0)` | `[x for x in arr if x>0]` |
| reduce | `arr.reduce((a,b)=>a+b, 0)` | `sum(arr)` / `functools.reduce(..., arr, 0)` |
| flat | `arr.flat()` | `[y for x in arr for y in x]` |

**⚠️ 코테 함정**: `arr.pop(0)` / `arr.insert(0, x)`는 **O(n)**. 큐가 필요하면 무조건 `collections.deque`.

## 4. 객체 ↔ 딕셔너리

| 동작 | JS | Python |
|---|---|---|
| 생성 | `{a:1, b:2}` | `{"a":1, "b":2}` |
| 접근 | `obj.a` / `obj["a"]` | `d["a"]` (속성 접근 X) |
| 존재 여부 | `"a" in obj` / `obj.hasOwnProperty("a")` | `"a" in d` |
| 기본값 접근 | `obj.a ?? default` | `d.get("a", default)` |
| 삭제 | `delete obj.a` | `del d["a"]` / `d.pop("a", None)` |
| 키/값/쌍 | `Object.keys/values/entries(obj)` | `d.keys()` / `d.values()` / `d.items()` |
| 병합 | `{...a, ...b}` | `{**a, **b}` / `a \| b` (3.9+) |
| Map | `new Map()` | 그냥 `dict` (key가 해시 가능하면 OK) |

**💡 코테 팁**:
- 카운팅: `collections.Counter(arr)` (JS의 수동 카운트 루프 → 한 줄)
- 기본값 딕셔너리: `collections.defaultdict(list)` (JS에서 `map[k] ??= []; map[k].push(...)` 패턴)

## 5. Set

| 동작 | JS | Python |
|---|---|---|
| 생성 | `new Set([1,2,3])` | `{1,2,3}` / `set([1,2,3])` |
| 빈 Set | `new Set()` | `set()` (⚠️ `{}`는 **빈 dict**) |
| 추가/삭제 | `s.add(x)`, `s.delete(x)` | `s.add(x)`, `s.discard(x)` / `s.remove(x)` |
| 포함 | `s.has(x)` | `x in s` |
| 연산 | (직접 구현) | `a \| b`, `a & b`, `a - b`, `a ^ b` |

## 6. 문자열

| 동작 | JS | Python |
|---|---|---|
| 길이 | `s.length` | `len(s)` |
| 분할 | `s.split(",")` | `s.split(",")` |
| 결합 | `arr.join(",")` | `",".join(arr)` (메서드 주체 반대!) |
| 대소 | `s.toUpperCase()` | `s.upper()` |
| 치환 | `s.replace(a, b)` | `s.replace(a, b)` (파이썬은 **전부** 치환 기본) |
| 포함 | `s.includes(x)` | `x in s` |
| 인덱스 | `s.indexOf(x)` | `s.find(x)` (-1) / `s.index(x)` (예외) |
| 반복 | `s.repeat(3)` | `s * 3` |
| 숫자 변환 | `Number(s)` / `parseInt(s)` | `int(s)` / `float(s)` |
| 문자열 변환 | `String(n)` / `n.toString()` | `str(n)` |
| 문자 → 코드 | `s.charCodeAt(0)` | `ord(s[0])` |
| 코드 → 문자 | `String.fromCharCode(97)` | `chr(97)` |

**⚠️ 코테 함정**: 파이썬 문자열은 **불변**. `s[0] = 'a'` 불가. 바꾸려면 리스트로 변환.

## 7. 숫자 / 수학

| 동작 | JS | Python |
|---|---|---|
| 정수 나눗셈 | `Math.floor(a/b)` / `a/b \| 0` | `a // b` |
| 나머지 | `a % b` (음수 결과 주의) | `a % b` (항상 b와 같은 부호) |
| 거듭제곱 | `Math.pow(a,b)` / `a ** b` | `a ** b` / `pow(a, b)` / `pow(a, b, m)` (모듈러) |
| 절댓값 | `Math.abs(x)` | `abs(x)` |
| 최대/최소 | `Math.max(...arr)` | `max(arr)` |
| 무한대 | `Infinity` | `float('inf')` / `math.inf` |
| 정수 범위 | Number.MAX_SAFE_INTEGER (2^53-1) | **무제한 정수** (코테에서 큰 장점) |

**💡 코테 팁**: 파이썬은 **BigInt 걱정 없음**. `2**100`도 그냥 연산.

## 8. 자주 쓰는 내장함수

| JS | Python |
|---|---|
| (없음, 수동) | `sum(arr)` |
| (없음, 수동) | `any(arr)` / `all(arr)` |
| `arr.sort().reverse()` | `sorted(arr, reverse=True)` |
| (수동) | `zip(a, b)` — 두 리스트 병렬 순회 |
| `arr.entries()` | `enumerate(arr)` |
| `[...Array(n).keys()]` | `range(n)` |
| (수동) | `min(arr, key=...)` / `max(arr, key=...)` |

## 9. 함수 / 고차함수

| 개념 | JS | Python |
|---|---|---|
| 함수 정의 | `function f(x) {...}` / `const f = x => ...` | `def f(x): ...` / `lambda x: ...` |
| 기본 인자 | `function f(x=1)` | `def f(x=1)` |
| 가변 인자 | `function f(...args)` | `def f(*args)` |
| 키워드 가변 | (객체 받기) | `def f(**kwargs)` |
| 스프레드 | `f(...arr)` | `f(*arr)` |
| 구조분해 | `const [a,b] = arr` | `a, b = arr` |
| (없음) | (2개 이상 반환) | `return a, b` → 튜플 |

## 10. 에러 처리

```javascript
try { ... } catch (e) { ... } finally { ... }
throw new Error("msg");
```

```python
try: ...
except ValueError as e: ...
except Exception as e: ...
finally: ...
raise ValueError("msg")
```

## 11. 모듈 / import

| JS | Python |
|---|---|
| `import x from "mod"` | `import mod` / `from mod import x` |
| `require("mod")` | `import mod` |

코테 자주 쓰는 모듈:
```python
from collections import deque, defaultdict, Counter
from heapq import heappush, heappop, heapify
from itertools import permutations, combinations, product, accumulate
from functools import lru_cache, reduce
import math, sys, bisect
```

**⚠️ 재귀 코테 필수**:
```python
import sys
sys.setrecursionlimit(10**6)
```

**⚠️ 큰 입력 빠른 읽기**:
```python
import sys
input = sys.stdin.readline
```

## 12. 코테 관점 요약: JS에 없거나 크게 다른 것

1. **들여쓰기가 문법** — 블록 없음
2. **정수 무제한** — BigInt 안 써도 됨
3. **튜플** — 불변 리스트. 딕셔너리 키로 사용 가능 (JS 객체 키는 문자열만)
4. **리스트 컴프리헨션** — `[x*2 for x in arr if x>0]`이 map/filter보다 파이써닉
5. **슬라이싱** — `arr[::-1]`, `s[1:-1]` 강력
6. **`in` 연산자** — 리스트/딕셔너리/문자열/셋 모두 동작 (단, 리스트는 O(n))
7. **언패킹** — `a, *rest = arr`, `for i, x in enumerate(arr)`
8. **`collections` / `heapq` / `bisect`** — JS보다 기본 제공 자료구조 훨씬 풍부
9. **`sort` key 함수** — `sorted(arr, key=lambda x: (x[0], -x[1]))` 다중키 자연스러움
10. **문자열 불변** — 조작 많으면 list로 변환 후 `"".join(...)`

## 13. 흔한 실수 (JS 습관에서 오는)

- `arr.length` → `len(arr)` (메서드 아님)
- `arr.push` → `arr.append`
- `arr.shift()` 계속 쓰다 TLE → `deque.popleft()`
- `===` 쓰려다 에러 → `==`
- 빈 dict를 `{}`로 만들고 set인 줄 착각 → set은 `set()`
- `i++` 불가 → `i += 1`
- 스위치/case 없음 (3.10+ `match`는 있음, 코테엔 잘 안 씀) → `if/elif`
- `null` → `None` (대문자)
- map/filter 결과가 이터레이터라 `list(...)` 감싸야 출력됨
- 정수 나눗셈 `/` 쓰면 float 반환 → `//` 사용
