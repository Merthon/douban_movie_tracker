from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import save_movie, get_movie_by_name, get_all_movies
from scraper import scrape_douban_movie
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 跨域支持
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 请求和响应模型
class MovieRequest(BaseModel):
    name: str

class MovieResponse(BaseModel):
    title: str
    url: str
    rating: str
    director: str
    actors: list[str]
    comments: list[str]
    scraped_at: str

# 添加电影（爬取或从数据库取）
@app.post("/movies/", response_model=MovieResponse)
async def create_movie(movie: MovieRequest):
    # 先查数据库
    existing_movie = get_movie_by_name(movie.name)
    if existing_movie:
        return existing_movie
    
    # 没找到就爬
    data = scrape_douban_movie(movie.name)
    if not data:
        raise HTTPException(status_code=404, detail="Movie not found on Douban")
    
    save_movie(data)
    return data

# 获取所有电影
@app.get("/movies/", response_model=list[MovieResponse])
async def get_movies():
    return get_all_movies()