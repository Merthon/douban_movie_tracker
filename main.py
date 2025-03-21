from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from database import save_movie, get_movie_by_name, get_all_movies, save_user, get_user, save_search_history, get_user_history
from scraper import scrape_douban_movie
from auth import verify_password, get_password_hash, create_access_token, decode_token
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

class UserRequest(BaseModel):
    username: str
    password: str

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

class HistoryResponse(BaseModel):
    movie: MovieResponse
    searched_at: str
@app.post("/register")
async def register(user: UserRequest):
    if get_user(user.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    password_hash = get_password_hash(user.password)
    save_user(user.username, password_hash)
    return {"message": "User registered successfully"}

@app.post("/login")
async def login(user: UserRequest):
    db_user = get_user(user.username)
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

async def get_current_user(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    username = decode_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return username

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
    movies = get_all_movies()
    if not movies:
        raise HTTPException(status_code=404, detail="No movies found")
    return movies

@app.get("/history/", response_model=list[HistoryResponse])
async def get_history(username: str = Depends(get_current_user)):
    history = get_user_history(username)
    if not history:
        raise HTTPException(status_code=404, detail="No search history found")
    return history