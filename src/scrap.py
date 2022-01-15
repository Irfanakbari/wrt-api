from asyncio.windows_events import NULL
import json
from urllib import request
from bs4 import BeautifulSoup as bs
from flask import request as req
import requests
from cachetools import cached, TTLCache
from src.success import error_connection

cache = TTLCache(maxsize=100, ttl=300)
cache2 = TTLCache(maxsize=100, ttl=10000)
cache3 = TTLCache(maxsize=100, ttl=900)
cache4 = TTLCache(maxsize=100, ttl=400)
cache5 = TTLCache(maxsize=100, ttl=900)


@cached(cache)
def get_homepage():
    url = "https://wrt.my.id/"
    r = requests.get(url)
    soup = bs(r.text, "html.parser")
    if r.status_code == 200:
        populer = []
        project = []
        rilis = []
        upcoming = []

        # GET POPULER
        for data in soup.find("div", class_="hothome").find_all("div", class_="bs"):
            tmp = {
                "title": data.find("div", class_="tt").text,
                "link": data.find("a").get("href"),
                "img": data.find("img").get("src"),
                "last_chapter": data.find("div", class_="epxs").text,
                "skor": data.find("div", class_="numscore").text
            }
            populer.append(tmp)

        # GET PROJECT
        for data in soup.find("div", class_="postbody").find_all("div", class_="bixbox")[0].find_all("div", class_="bs"):
            tmp = {
                "title": data.find("a").text,
                "link": data.find("a").get("href"),
                "img": data.find("img").get("src"),
                "last_chapter": data.find("ul", class_="chfiv").find("li").find("a").text.replace("Ch. ", "Chapter"),
                "last_update": data.find("ul", class_="chfiv").find("li").find("span").text
            }
            project.append(tmp)

        # GET RILIS
        for data in soup.find("div", class_="postbody").find_all("div", class_="bixbox")[1].find_all("div", class_="utao"):
            tmp = {
                "title": data.find("div", class_="luf").find("a").find("h4").text,
                "link": data.find("div", class_="luf").find("a").get("href"),
                "img": data.find("img").get("src"),
                "last_chapter": data.find("ul", class_="Manga").find("li").find("a").text.replace("Ch. ", "Chapter"),
                "last_update": data.find("ul", class_="Manga").find("li").find("span").text
            }
            rilis.append(tmp)

        # GET UPCOMING
        for data in soup.find("div", class_="postbody").find_all("div", class_="bixbox")[2].find_all("div", class_="bs"):
            tmp = {
                "title": data.find("div", class_="tt").text,
                "link": data.find("a").get("href"),
                "img": data.find("img").get("src"),
            }
            upcoming.append(tmp)

        return json.dumps({
            "code": 200,
            "status": "success",
            "data": {
                "populer": populer,
                "project": project,
                "rilis": rilis,
                "upcoming": upcoming
            }
        }, indent=5)
    else:
        return error_connection()


@cached(cache2)
def get_genre():
    url = "https://wrt.my.id/"
    r = requests.get(url)
    soup = bs(r.text, "html.parser")
    if r.status_code == 200:
        genre = []
        for data in soup.find("ul", class_="genre").find_all("li"):
            tmp = {
                "genre": data.find("a").text,
                "link": data.find("a").get("href")
            }
            genre.append(tmp)
        return json.dumps({
            "code": 200,
            "status": "success",
            "data": genre
        }, indent=5)
    else:
        return error_connection()


def get_project():
    if req.args.get("page") is not None:
        url = "https://wrt.my.id/project-wrt/page/" + req.args.get("page")
        r = requests.get(url)
        soup = bs(r.text, "html.parser")
        if r.status_code == 200:
            project = []
            for data in soup.find_all("div", class_="bs"):
                tmp = {
                    "title": data.find("div", class_="tt").text,
                    "link": data.find("a").get("href"),
                    "cover": data.find("img").get("src"),
                    "last_chapter": data.find("div", class_="epxs").text,
                    "last_update": data.find("div", class_="epxdate").text,
                }
                project.append(tmp)
            return json.dumps({
                "code": 200,
                "status": "success",
                "total_page": soup.find("div", class_="pagination").find_all("a")[-1].text,
                "current_page": req.args.get("page"),
                "data": project
            }, indent=5)
        else:
            return error_connection()
    else:
        return json.dumps({
            "code": 400,
            "status": "failed",
            "message": "Page parameter is required"
        }, indent=5)


@cached(cache4)
def get_allproject():
    url = "https://wrt.my.id/project-wrt/"
    r = requests.get(url)
    project = []
    soup = bs(r.text, "html.parser")
    total_page = int(
        soup.find("div", class_="pagination").find_all("a")[-2].text)
    for i in range(1, (total_page+1)):
        url = "https://wrt.my.id/project-wrt/page/" + str(i)
        r = requests.get(url)
        soup = bs(r.text, "html.parser")
        if r.status_code == 200:
            for data in soup.find_all("div", class_="bs"):
                project.append({
                    "title": data.find("div", class_="tt").text,
                    "link": data.find("a").get("href"),
                    "cover": data.find("img").get("src"),
                    "last_chapter": data.find("div", class_="epxs").text,
                    "last_update": data.find("div", class_="epxdate").text,
                }
                )

        else:
            return error_connection()
    return json.dumps({
        "code": 200,
        "status": "success",
        "page_length": total_page,
        "data": project
    }, indent=8)


@cached(cache5)
def get_manga_list():
    url = "https://wrt.my.id/manga/list-mode/"
    r = requests.get(url)
    soup = bs(r.text, "html.parser")
    if r.status_code == 200:
        manga = []
        for data in soup.find_all("div", class_="blix"):
            abjd_tmp = data.find("span").find("a").text
            tmp2 = []
            for data2 in data.find_all("li"):
                tmp = {
                    "title": data2.find("a").text,
                    "link": data2.find("a").get("href"),
                }
                tmp2.append(tmp)
            manga.append({
                "abjad": abjd_tmp,
                "manga": tmp2
            })
        return json.dumps({
            "code": 200,
            "status": "success",
            "data": manga
        }, indent=5)


def get_detail_manga():
    if req.args.get("link") is not None:
        url = req.args.get("link")
        r = requests.get(url)
        soup = bs(r.text, "html.parser")
        if r.status_code == 200:
            detail = []
            tmp = []
            tmp2 = []
            tmp3 = []
            for data in soup.find("table", class_="infotable").find_all("tr"):
                tmp.append(data.find_all("td")[1].text)
            for data2 in soup.find("div", class_="seriestugenre").find_all("a"):
                tmp2.append(data2.text)
            for data3 in soup.find("div", class_="eplister").find_all("li"):
                tmp3.append({
                    "chapter": data3.find("div", class_="eph-num").find("a").find("span").text,
                    "link": data3.find("div", class_="eph-num").find("a").get("href"),
                    "update": data3.find("div", class_="eph-num").find("a").find("span", class_="chapterdate").text
                })
                alt = soup.find("div", class_="seriestualt").get_text()

            detail.append({
                "post_id": soup.find("article").get("id"),
                "title": soup.find("h1", class_="entry-title").text,
                "alternative": alt,
                "cover": soup.find("div", class_="seriestucontl").find("img").get("src"),
                "rating": soup.find("div", class_="rating-prc").find("div", class_="num").text,
                "sinopsis": soup.find("div", class_="seriestuhead").find("p").text,
                "info": tmp,
                "genre": tmp2,
                "list_chapter": tmp3
            })
            return json.dumps({
                "code": 200,
                "status": "success",
                "data": detail
            }, indent=5)
        else:
            return error_connection()
    else:
        return json.dumps({
            "code": 400,
            "status": "failed",
            "message": "Link parameter is required"
        }, indent=5)
