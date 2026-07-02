import anthropic
import instructor
import os
from pydantic import BaseModel
from dotenv import load_dotenv

class Recipe(BaseModel):
    menu_name: str
    ingredients: list[str]
    steps: list[str]

load_dotenv()

client = instructor.from_anthropic(anthropic.Anthropic())

def extract_recipe(text: str) -> Recipe:
# 블로그/자막 텍스트 받고 -> LLM한테 레시피 추출 요청 -> Recipe 객체로 반환
    return client.messages.create(
        model="claude-haiku-4-5",
        # 구조화 추출은 단순 작업 — 가장 저렴한 모델로 충분
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"다음 텍스트에서 카페 음료 레시피를 추출해줘:\n\n{text}"
            }
        ],
        response_model=Recipe,
        # Instructor 핵심 — LLM 출력을 Recipe 객체로 강제 변환
    )

if __name__ == "__main__":
    sample = "아인슈페너 만들기. 에스프레소 2샷, 우유 150ml, 생크림 50ml 준비. 1. 에스프레소를 추출한다. 2. 생크림을 올린다."
    
    recipe = extract_recipe("Let’s make a simple cafe latte at home without a whisk. Pour 1 cup (180ml) of milk into a pot and heat until just before boiling. Pour 1 cup of water into the pot and boil it. Do not boil the milk. Turn off the heat when a lot of steam rises and it is just about to boil. When the water boils, warm the cup with the steam. I prepared a 300ml cup. It's hot, so place a cup next to the pot. This will help you stay warm longer. Pour 2 bags (24 grams) of mixed coffee into the warmed cup. Add 3 tablespo")
    print(recipe.menu_name)
    print(recipe.ingredients)
    print(recipe.steps)