import anthropic
import instructor
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# __file__ 기준으로 한 단계 위(backend/)를 경로에 추가 — pipeline.step3_extractor 임포트를 가능하게 함
from dotenv import load_dotenv
from pipeline.step3_extractor import Recipe
# Step 3에서 정의한 Recipe 스키마 재사용 — 입력도 출력도 같은 형태

load_dotenv()

client = instructor.from_anthropic(anthropic.Anthropic())
# Instructor가 Anthropic 클라이언트를 감싸서 response_model 파라미터를 쓸 수 있게 해줌

def synthesize_recipes(recipes: list[Recipe]) -> Recipe:
    if not recipes:
        raise ValueError("레시피가 없습니다")
    # 빈 리스트가 들어오면 LLM 호출 전에 즉시 실패 — 원인 불명 에러 방지

    recipes_text = ""
    for i, recipe in enumerate(recipes, start=1):
        recipes_text += f"[소스 {i}]\n"
        recipes_text += f"메뉴명: {recipe.menu_name}\n"
        recipes_text += f"재료: {', '.join(recipe.ingredients)}\n"
        recipes_text += f"방법: {' / '.join(recipe.steps)}\n\n"
    # Recipe 객체들을 텍스트로 변환 — LLM은 객체를 못 받으니까

    return client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""아래 여러 소스의 레시피를 비교해서 하나로 합쳐줘.
- 재료: 가장 공통적으로 등장하는 것 위주로
- 방법: 가장 상세한 버전 기준으로
- 메뉴명: 가장 일반적인 이름으로

{recipes_text}"""
            }
        ],
        # 프롬프트에 기준을 명시할수록 LLM 출력 품질이 올라감 — "합쳐줘"만 하면 기준 없이 임의로 선택함
        response_model=Recipe,
        # Instructor 핵심 — LLM 출력을 Recipe 객체로 강제 변환, 실패 시 자동 재시도
    )

if __name__ == "__main__":
    recipe1 = Recipe(
        menu_name="아인슈페너",
        ingredients=["에스프레소 2샷", "생크림 50ml"],
        steps=["에스프레소 추출", "생크림 올리기"]
    )
    recipe2 = Recipe(
        menu_name="아인슈페너",
        ingredients=["에스프레소 2샷", "우유100ml"],
        steps=["에스프레소 추출", "라떼아트 하기"]
    )
    result = synthesize_recipes([recipe1, recipe2])
    print(result.menu_name)
    print(result.ingredients)
    print(result.steps)