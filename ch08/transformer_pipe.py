# transformer_pipe.py
from transformers import pipeline

print("1. 허깅페이스에서 AI 모델을 다운로드/로드 중입니다... (최초 1회만 시간 소요)")
# [설명] zero-shot-classification 파이프라인을 생성하고, 한국어를 지원하는 가벼운 다국어 모델을 불러옵니다.
pipe = pipeline(
    "zero-shot-classification",
    model="MoritzLaurer/multilingual-MiniLMv2-L6-mnli-xnli"
)

# ---------------------------------------------------------
# [문 1] 제로샷의 마법! 우리가 분류하고 싶은 카테고리를 미리 정의합니다.
# 기존에 없던 새로운 카테고리(예: 건강, 여가 등)를 마음대로 적어보세요.
# ---------------------------------------------------------
CATEGORIES = [
    # 빈칸 채우기 (문자열 리스트 형태)
    "개인", "공부", "쇼핑", "업무", "운동", "건강", "여가", "문화"
]

def predict_category(content: str) -> dict:
    # 파이프라인에 텍스트와 카테고리를 통째로 던지면 끝! (fit 과정이 없음)
    result = pipe(content, CATEGORIES)

    # 파이프라인 결과에서 가장 점수가 높은 1등 카테고리 추출
    top_label = result["labels"][0]

    # ---------------------------------------------------------
    # [문 2] 파이프라인 결과는 'labels' 리스트와 'scores' 리스트로 나뉘어 나옵니다.
    # zip 함수를 사용하여 두 리스트를 묶어 딕셔너리(dict) 형태로 만드세요.
    # ---------------------------------------------------------
    score_map = dict(zip(
        # 빈칸 채우기
        result['labels'], result['scores']
    ))

    return {
        "predicted_category": top_label,
        "score_map": score_map
    }

# --- Main 실행 테스트 ---
if __name__ == "__main__":
    test_texts = [
        "새로 나온 런닝화 사이즈 270 주문하기",
        "비타민 C랑 오메가3 챙겨 먹기",
        "자격증 시험 기출문제 3회독 풀기"
    ]

    print("\n========= 🤖 현대 AI 제로샷 예측 결과 =========")
    for text in test_texts:
        result = predict_category(text)
        print(f"📝 입력 할 일 : {text}")
        print(f"🏷️  예측 분류 : [{result['predicted_category']}]")

        # 소수점 2자리까지만 백분율로 출력되도록 보기 좋게 변환
        formatted_scores = {k: f"{v*100:.1f}%" for k, v in result['score_map'].items()}
        print(f"📊 상세 확률 : {formatted_scores}")
        print("-" * 45)

### [추가 토의 질문]
# 내가 작성한 'CATEGORIES' 목록에 포함되지 않은 엉뚱한 문장(예: "우주선 타고 화성 가기")을 넣으면 모델은 어떤 결과를 출력할까요?
# 이처럼 제로샷 모델이 가지는 논리적 한계(주어진 카테고리 안에서만 무조건 답을 찾아야 함)를 서비스에서 어떻게 방어할 수 있을지 생각해 봅시다.