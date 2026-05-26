# Step 1. 에러 처리 계층 만들기 (error.py)
# 데이터가 없거나 중복될 때 사용할 깔끔한 에러 객체를 만듭니다.
# error.py
class Missing(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

class Duplicate(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg