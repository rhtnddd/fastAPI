from typing import List, Tuple, Dict, Optional, Union, Literal, Callable, TypeVar, Generic

from typing import NewType

# --- 의미 있는 별칭 타입 ---

UserId = NewType("UserId", int)


# --- 1. 기본 연산: add ---

def add(a: int, b: int) -> int:
    """정수 두 개를 더한 값을 반환한다."""

    return a + b


# --- 2. 리스트 처리: double_all ---

def double_all(numbers: List[int]) -> List[int]:
    """

    정수 리스트의 각 원소를 두 배로 만들어 반환한다.

    - 빈 리스트면 그대로 빈 리스트 반환

    """


    return [i * 2 for i in numbers]


# --- 3. 튜플 생성: person_info ---

def person_info(name: str, age: int) -> Tuple[str, int]:
    """

    이름과 나이를 튜플로 반환한다. (name, age)

    - age는 0 이상이어야 한다. 아니라면 ValueError

    """

    # TODO: 검증 추가

    if age < 0:
        raise ValueError("age는 0 이상이어야 합니다.")

    return name, age

# --- 4. 딕셔너리 가공: normalize_scores ---

def normalize_scores(raw: Dict[str, float]) -> Dict[str, float]:
    """

    학생 점수 딕셔너리를 0~1 범위로 정규화하여 반환한다.

    - 최대값이 0이면 모든 값을 0.0으로 반환

    - 빈 딕셔너리면 빈 딕셔너리 반환

    """

    if not raw:
        return {}

    max_score = max(raw.values()) if raw else 0.0

    if max_score <= 0:
        return {k: 0.0 for k in raw}

        # TODO: 딕셔너리 컴프리헨션으로 0~1 스케일링

    return {name: score / max_score for name, score in raw.items()}


# --- 5. Optional 처리: find_user_name ---

def find_user_name(users: Dict[UserId, str], user_id: UserId) -> Optional[str]:
    """

    주어진 user_id에 해당하는 이름을 반환한다.

    - 없으면 None 반환

    """

    # TODO: dict.get 사용

    return users.get(user_id)


# --- 6. Union 처리: square_or_length ---

def square_or_length(value: Union[int, str]) -> int:
    """TODO:

    - int -> 제곱값 반환

    - str -> 문자열 길이 반환

    """
    if isinstance(value, int):
        return value ** 2

    if isinstance(value, str):
        return len(value)


# --- 7. Literal 인자: sort_numbers ---

def sort_numbers(numbers: List[int], order: Literal["asc", "desc"] = "asc") -> List[int]:
    """

    order가 'asc'면 오름차순, 'desc'면 내림차순으로 정렬하여 반환.

    """

    # TODO: order 값에 따라 reverse 플래그 설정

    reverse = (order == "desc")

    return sorted(numbers, reverse=reverse)


# --- 8. Callable 사용: apply_op ---

def apply_op(a: int, b: int, op: Callable[[int, int], int]) -> int:
    """

    전달받은 op 함수(시그니처: (int, int) -> int)를 a, b에 적용하여 결과 반환.

    예: op=add -> add(a, b)

    """

    # TODO: op 호출
    return op(a, b)

# --- 9. 제네릭 함수: first_or_default ---

T = TypeVar("T")


def first_or_default(items: List[T], default: T) -> T:
    """

    리스트가 비어있지 않으면 첫 요소를, 비어있으면 default를 반환.

    제네릭으로 어떤 타입 리스트에도 동작.

    """

    # TODO: 빈 리스트 처리
    if len(items) == 0:
        return default
    return items[0]


# --- 10. 에러/경계값 핸들링: safe_div ---

def safe_div(a: float, b: float) -> Optional[float]:
    """

    0으로 나누면 None, 그렇지 않으면 a / b 결과를 반환.

    """

    # TODO: ZeroDivision 보호
    if b == 0:
        return None
    return a / b

# --- 11. 간단한 비즈니스 규칙: compute_grade ---

def compute_grade(score: float) -> Literal["A", "B", "C", "D", "F"]:
    """

    점수(0~100)에 대해 등급 리터럴을 반환.

    - 유효 범위가 아니면 ValueError

    규칙(예시):

        90~100 -> "A"

        80~89  -> "B"

        70~79  -> "C"

        60~69  -> "D"

        0~59   -> "F"

    """

    # TODO: 범위 검사 및 등급 판정
    if 100 < score < 0:
        raise ValueError("에러다잇!!")
    elif score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"

# --- 메인: 간단 실행/검증 예시 ---

if __name__ == "__main__":

    # 1) add

    print("add:", add(1, 2))  # 3

    # print(add("1", "2"))  # 타입 힌트 위반 예시(정적 검사에서 잡힘)

    # 2) double_all

    print("double_all:", double_all([1, 2, 3]))  # [2, 4, 6]

    print("double_all empty:", double_all([]))  # []

    # 3) person_info

    print("person_info:", person_info("Alice", 25))  # ("Alice", 25)

    try:

        person_info("Bob", -1)  # ValueError

    except ValueError as e:

        print("person_info error:", e)

        # 4) normalize_scores

    print("normalize_scores:", normalize_scores({"A": 50.0, "B": 100.0}))  # {"A": 0.5, "B": 1.0}

    print("normalize_scores empty:", normalize_scores({}))  # {}

    # 5) find_user_name

    users = {UserId(1): "Alice", UserId(2): "Bob"}

    print("find_user_name exist:", find_user_name(users, UserId(1)))  # "Alice"

    print("find_user_name none:", find_user_name(users, UserId(3)))  # None

    # 6) square_or_length

    print("square_or_length int:", square_or_length(10))  # 100

    print("square_or_length str:", square_or_length("10"))  # 2

    # print(square_or_length(3.14))  # 정적 검사에서 Union 불일치 경고 예상

    # 7) sort_numbers

    print("sort asc:", sort_numbers([3, 1, 2], "asc"))  # [1, 2, 3]

    print("sort desc:", sort_numbers([3, 1, 2], "desc"))  # [3, 2, 1]

    # 8) apply_op

    print("apply_op add:", apply_op(3, 4, add))  # 7

    print("apply_op lambda mul:", apply_op(3, 4, lambda x, y: x * y))  # 12

    # 9) first_or_default

    print("first_or_default:", first_or_default([10, 20], 0))  # 10

    print("first_or_default empty:", first_or_default([], 0))  # 0

    # 10) safe_div

    print("safe_div ok:", safe_div(10, 2))  # 5.0

    print("safe_div zero:", safe_div(10, 0))  # None

    # 11) compute_grade

    print("grade:", compute_grade(85))  # "B"

    try:

        compute_grade(120)  # ValueError

    except ValueError as e:

        print("grade error:", e)