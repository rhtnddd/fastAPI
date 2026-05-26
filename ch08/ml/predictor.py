# Step 3. AI 두뇌 준비하기 (ml/predictor.py)
# 서버가 켜질 때 모델을 장전하고, 예측 요청이 오면 응답하는 함수입니다.
# ml/predictor.py
from transformers import pipeline

print("🤖 AI 제로샷 분류 모델 로딩 중... (최초 1회만 시간 소요)")
classifier = pipeline("zero-shot-classification", model="typeform/distilbert-base-uncased-mnli")

CATEGORIES = ["기쁨", "슬픔", "분노", "평온", "기대"]

def predict_category(text: str) -> dict:
    """사용자의 할 일 텍스트를 기반으로 카테고리를 예측합니다."""
    result = classifier(text, CATEGORIES)
    top_label = result["labels"][0]
    score_map = dict(zip(result["labels"], result["scores"]))
    return {
        "predicted_category": top_label,
        "scores": score_map
    }


