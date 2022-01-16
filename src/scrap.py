import json
from bs4 import BeautifulSoup as bs
from flask import request as req
from flask import make_response as res
import requests
from cachetools import cached, TTLCache
from src.success import error_connection

cache = TTLCache(maxsize=100, ttl=400)
cache2 = TTLCache(maxsize=100, ttl=10000)
cache3 = TTLCache(maxsize=100, ttl=900)
cache4 = TTLCache(maxsize=100, ttl=400)
cache5 = TTLCache(maxsize=100, ttl=900)
cache6 = TTLCache(maxsize=100, ttl=1000)
cachedetail = TTLCache(maxsize=100, ttl=1-00)


@cached(cache)
def get_homepage():
    url = "https://wrt.my.id/"
    r = requests.get(url)
    soup = bs(r.text, "html.parser")
    if r.status_code == 200:
        populer = []
        project = []
        rilis = []

        # GET POPULER
        for data in soup.find("div", class_="hothome").find_all("div", class_="bs"):
            tmp = {
                "title": data.find("div", class_="tt").text.replace("\n", "").replace("\t", ""),
                "slug": data.find("a").get("href").split("https://wrt.my.id/manga")[1].split("/")[1].replace("/", ""),
                "link": data.find("a").get("href"),
                "hot": data.find("span", class_="hotx") is not None,
                "img": data.find("img").get("src"),
                "last_chapter": data.find("div", class_="epxs").text,
                "skor": data.find("div", class_="numscore").text
            }
            populer.append(tmp)

        # GET PROJECT
        for data in soup.find("div", class_="postbody").find_all("div", class_="bixbox")[0].find_all("div", class_="bs"):
            tmp = {
                "title": data.find("div", class_="tt").find("a").text.replace("\n", "").replace("\t", ""),
                "slug": data.find("a").get("href").split("https://wrt.my.id/manga")[1].split("/")[1].replace("/", ""),
                "link": data.find("a").get("href"),
                "hot": data.find("span", class_="hotx") is not None,
                "img": data.find("img").get("src"),
                "last_chapter": data.find("ul", class_="chfiv").find("li").find("a").text.replace("Ch. ", "Chapter"),
                "last_update": data.find("ul", class_="chfiv").find("li").find("span").text
            }
            project.append(tmp)

        # GET RILIS
        for data in soup.find("div", class_="postbody").find_all("div", class_="bixbox")[1].find_all("div", class_="utao"):
            tmp = {
                "title": data.find("div", class_="luf").find("a").find("h4").text.replace("\n", "").replace("\t", ""),
                "slug": data.find("div", class_="luf").find("a").get("href").split("https://wrt.my.id/manga")[1].split("/")[1].replace("/", ""),
                "link": data.find("div", class_="luf").find("a").get("href"),
                "hot": data.find("span", class_="hot") is not None,
                "img": data.find("img").get("src"),
                "last_chapter": data.find("ul", class_="Manga").find("li").find("a").text.replace("Ch. ", "Chapter"),
                "last_update": data.find("ul", class_="Manga").find("li").find("span").text
            }
            rilis.append(tmp)

        ress = res(json.dumps({
            "code": 200,
            "status": "success",
            "data": {
                "populer": populer,
                "project": project,
                "rilis": rilis,
            }
        }, indent=4))
        ress.headers["Access-Control-Allow-Origin"] = "*"
        ress.headers["Content-Type"] = "application/json"
        return ress
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
        ress = res(
            json.dumps({
                "code": 200,
                "status": "success",
                "data": genre
            }, indent=4)
        )
        ress.headers["Access-Control-Allow-Origin"] = "*"
        ress.headers["Content-Type"] = "application/json"
        return ress
    else:
        return error_connection()


def get_project(page):
    if page is not 0:
        url = "https://wrt.my.id/project-wrt/page/" + str(page)
        r = requests.get(url)
        soup = bs(r.text, "html.parser")
        if r.status_code == 200:
            project = []
            for data in soup.find_all("div", class_="bs"):
                tmp = {
                    "title": data.find("div", class_="tt").text,
                    "slug": data.find("a").get("href").split("https://wrt.my.id/manga")[1].split("/")[1].replace("/", ""),
                    "link": data.find("a").get("href"),
                    "hot": data.find("span", class_="hotx") is not None,
                    "cover": data.find("img").get("src"),
                    "last_chapter": data.find("div", class_="epxs").text,
                    "last_update": data.find("div", class_="epxdate").text,
                }
                project.append(tmp)
            ress = res(
                json.dumps({
                    "code": 200,
                    "status": "success",
                    "total_page": soup.find("div", class_="pagination").find_all("a")[-1].text,
                    "current_page": req.args.get("page"),
                    "data": project
                }, indent=4)
            )
            ress.headers["Access-Control-Allow-Origin"] = "*"
            ress.headers["Content-Type"] = "application/json"
            return ress
        else:
            return error_connection()
    else:
        return json.dumps({
            "code": 400,
            "status": "failed",
            "message": "Page parameter is required"
        }, indent=4)


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
                    "slug": data.find("a").get("href").split("https://wrt.my.id/manga")[1].split("/")[1].replace("/", ""),
                    "link": data.find("a").get("href"),
                    "hot": data.find("span", class_="hotx") is not None,
                    "cover": data.find("img").get("src"),
                    "last_chapter": data.find("div", class_="epxs").text,
                    "last_update": data.find("div", class_="epxdate").text,
                }
                )

        else:
            return error_connection()
    ress = res(json.dumps({
        "code": 200,
        "status": "success",
        "page_length": total_page,
        "data": project
    }, indent=8))

    ress.headers["Access-Control-Allow-Origin"] = "*"
    ress.headers["Content-Type"] = "application/json"
    return ress


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
        ress = res(json.dumps({
            "code": 200,
            "status": "success",
            "data": manga
        }, indent=4))
        ress.headers["Access-Control-Allow-Origin"] = "*"
        ress.headers["Content-Type"] = "application/json"
        return ress


@cached(cachedetail)
def get_detail_manga(slug):
    if slug is not None:
        url = 'https://wrt.my.id/manga/' + slug
        r = requests.get(url)
        key = ["Status", "Type", "Rilis", "Author", "Artist",
               "Serialization", "Uploader", "Posted On", "Last Update", "Viewers"]
        soup = bs(r.text, "html.parser")
        if r.status_code == 200:
            detail = []
            tmp = []
            rekomendasi = []
            tmp2 = []
            tmp3 = []
            for index, data in enumerate(soup.find("table", class_="infotable").find_all("tr")):
                tmp.append({
                    key[index]: data.find_all(
                        "td")[1].text.replace("\n", "")
                })
            for data2 in soup.find("div", class_="seriestugenre").find_all("a"):
                tmp2.append(data2.text)
            for data3 in soup.find("div", class_="listupd").find_all("div", class_="bs"):
                rekomendasi.append({
                    "title": data3.find("div", class_="tt").text.replace("\n", "").replace("\t", ""),
                    "link": data3.find("a").get("href"),
                    "cover": data3.find("img").get("src"),
                    "last_chapter": data3.find("div", class_="epxs").text,
                    "skor": data3.find("div", class_="numscore").text,
                })
            for data3 in soup.find("div", class_="eplister").find_all("li"):
                tmp3.append({
                    "chapter": data3.find("div", class_="eph-num").find("a").find("span").text,
                    "slug": data3.find("div", class_="eph-num").find("a").get("href").split("https://wrt.my.id")[1].split("/")[1].replace("/", ""),
                    "link": data3.find("div", class_="eph-num").find("a").get("href"),
                    "update": data3.find("div", class_="eph-num").find("a").find("span", class_="chapterdate").text
                })
                alt = soup.find(
                    "div", class_="seriestualt").get_text().replace("\n", "")

            detail.append({
                "post_id": soup.find("article").get("id"),
                "title": soup.find("h1", class_="entry-title").text,
                "alternative": alt,
                "cover": soup.find("div", class_="seriestucontl").find("img").get("src"),
                "rating": soup.find("div", class_="rating-prc").find("div", class_="num").text,
                "adult": soup.find("div", class_="alr") is not None,
                "sinopsis": soup.find("div", class_="seriestuhead").find("p").text,
                "info": tmp,
                "genre": tmp2,
                "list_chapter": tmp3,
                "rekomendasi": rekomendasi
            })
            ress = res(json.dumps({
                "code": 200,
                "status": "success",
                "data": detail
            }, indent=4))
            ress.headers["Access-Control-Allow-Origin"] = "*"
            ress.headers["Content-Type"] = "application/json"
            return ress
        else:
            return error_connection()
    else:
        return res(json.dumps({
            "code": 400,
            "status": "failed",
            "message": "Link parameter is required"
        }, indent=4))


def search_komik(keyword, page):
    url = "https://wrt.my.id/?s=" + keyword
    project = []
    if keyword is not None and page is not None:
        r = requests.get(url)
        soup = bs(r.text, "html.parser")
        if soup.find("div", class_="pagination") is None:
            pageLength = int(
                soup.find("div", class_="pagination").find_all("a")[-2].text)
        else:
            pageLength = 1
        url = "https://wrt.my.id/page/" + \
            page + "?s=" + keyword
        r = requests.get(url)
        soup = bs(r.text, "html.parser")
        if r.status_code == 200:
            for data in soup.find_all("div", class_="bs"):
                project.append({
                    "title": data.find("div", class_="tt").text.replace("\n", "").replace("\t", ""),
                    "slug": data.find("a").get("href").split("https://wrt.my.id/manga")[1].split("/")[1].replace("/", ""),
                    "link": data.find("a").get("href"),
                    "hot": data.find("span", class_="hotx") is not None,
                    "cover": data.find("img").get("src"),
                    "last_chapter": data.find("div", class_="epxs").text,
                    "skor": data.find("div", class_="numscore").text,
                }
                )
        else:
            return error_connection()
        ress = res(json.dumps({
            "code": 200,
            "status": "success",
            "page_length": pageLength,
            "data": project
        }, indent=4))
        ress.headers["Access-Control-Allow-Origin"] = "*"
        ress.headers["Content-Type"] = "application/json"
        return ress
    else:
        return res(json.dumps({
            "code": 400,
            "status": "failed",
            "message": "Keyword parameter is required"
        }, indent=4))


@cached(cache6)
def get_reader_page(slug):
    if slug is not None:
        url = "https://wrt.my.id/" + slug
        r = requests.get(url)
        soup = bs(r.text, "html.parser")
        if r.status_code == 200:
            link = []
            linkmin = []
            linkmedium = []
            for data in soup.find("div", id="readerarea").find_all("img"):
                link.append(data.get("src"))
            for data2 in link:
                if data2.find("cdn3.wrt.my.id") != -1:
                    linkmedium.append(data2 + "?quality=50")
                    linkmin.append(data2 + "?quality=25")
                if data2.find("images2.imgbox.com") != -1:
                    linkmedium.append(data2.replace(
                        "images2.imgbox.com", "cdn4.wrt.my.id") + "?quality=50")
                    linkmin.append(data2.replace(
                        "images2.imgbox.com", "cdn4.wrt.my.id") + "?quality=25")
                if data2.find("i.ibb.co") != -1:
                    linkmedium.append(data2.replace(
                        "i.ibb.co", "cdn5.wrt.my.id") + "?quality=50")
                    linkmin.append(data2.replace(
                        "i.ibb.co", "cdn5.wrt.my.id") + "?quality=25")
            ress = res(json.dumps({
                "code": 200,
                "status": "success",
                "data-high": link,
                "data-med": linkmedium,
                "data-min": linkmin
            }, indent=4))
            ress.headers["Access-Control-Allow-Origin"] = "*"
            ress.headers["Content-Type"] = "application/json"
            return ress
        else:
            return error_connection()
    else:
        return res(json.dumps({
            "code": 400,
            "status": "failed",
            "message": "Link parameter is required"
        }, indent=4))
