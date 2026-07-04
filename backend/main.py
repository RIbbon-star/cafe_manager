import sys, os
sys.path.insert(0, os.path.dirname(__file__))
# backend/ 폴더를 경로에 추가 — collectors, pipeline 모듈 인식용

from collectors.step1_naver_collector import search_blog
from collectors.step2_youtube_collector import search_youtube, get_transcript
from pipeline.step3_extractor import extract_recipe, Recipe
from pipeline.step4_synthesizer import synthesize_recipes
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "카페 메뉴 API"}

@app.get("/recipe")
def get_recipe(query: str):
    # 1. 블로그 + 유튜브 검색
    blog_results = search_blog(query, display=3)
    youtube_results = search_youtube(query, max_results=3)

    # 2. 각 소스에서 레시피 추출
    recipes = []
    for item in blog_results:
        recipe = extract_recipe(item["description"])
        if recipe:
            recipes.append(recipe)

    for item in youtube_results:
        video_id = item["id"]["videoId"]
        text = get_transcript(video_id)
        if text:
            recipe = extract_recipe(text)
            if recipe:
                recipes.append(recipe)

    # 3. 합성
    result = synthesize_recipes(recipes)
    return result