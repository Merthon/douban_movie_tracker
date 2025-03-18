import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "Referer": "https://www.douban.com"  # 加个 Referer，模拟正常访问
}

def scrape_douban_movie(movie_name):
    # 设置无头浏览器
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    
    search_url = f"https://movie.douban.com/subject_search?search_text={movie_name}"
    print(f"Searching: {search_url}")
    
    # 加载页面
    driver.get(search_url)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "item-root"))
        )
    except:
        print("Timeout waiting for search results.")
        driver.quit()
        return None
    
    print(f"Page Title: {driver.title}")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    movie_link = soup.select_one(".item-root a[href^='https://movie.douban.com/subject/']")
    if not movie_link:
        print("No movie link found.")
        driver.quit()
        return None
    
    movie_url = movie_link["href"]
    print(f"Detail URL: {movie_url}")
    driver.quit()
    
    # 爬详情页
    time.sleep(2)
    detail_response = requests.get(movie_url, headers=HEADERS)
    print(f"Detail Status Code: {detail_response.status_code}")
    if detail_response.status_code != 200:
        print(f"Detail Response: {detail_response.text[:500]}")
        return None
    
    detail_soup = BeautifulSoup(detail_response.text, "html.parser")
    
    title = detail_soup.select_one("h1 span").text.strip()
    rating = detail_soup.select_one(".rating_num").text.strip() or "N/A"
    director = detail_soup.select_one(".attrs a").text.strip() if detail_soup.select_one(".attrs a") else "Unknown"
    # 修复演员选择器
    actors_section = detail_soup.select_one("#info > span:nth-child(5) > span.attrs")
    actors = [a.text.strip() for a in actors_section.select("a")][:3] if actors_section else ["Unknown"]
    comments = [c.text.strip() for c in detail_soup.select(".comment-item .comment p span.short")[:5]] or ["No comments"]
    
    print(f"Scraped Title: {title}")
    print(f"Scraped Actors: {actors}")
    return {
        "title": title,
        "url": movie_url,
        "rating": rating,
        "director": director,
        "actors": actors,
        "comments": comments,
        "scraped_at": time.ctime()
    }

if __name__ == "__main__":
    data = scrape_douban_movie("肖申克的救赎")
    print(f"Final Result: {data}")