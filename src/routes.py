from os import link
import src.success as sukses
import src.scrap as scrap
from flask import request as req


class Routes:
    @staticmethod
    def run(app):

        @app.route('/')
        def index():
            return sukses.success()

        @app.route('/api/home')
        def home():
            return scrap.get_homepage()

        @app.route('/api/genre')
        def genre():
            return scrap.get_genre()

        @app.route('/api/project')
        def project():
            return scrap.get_allproject()

        @app.route('/project/<page>')
        def project_page(page):
            return scrap.get_project(page)

        @app.route('/api/mangalist')
        def mangalist():
            return scrap.get_manga_list()

        @app.route('/api/detail/<slug>')
        def manga(slug):
            return scrap.get_detail_manga(slug)

        @app.route('/api/search/<keyword>/<page>')
        def search(keyword, page):
            return scrap.search_komik(keyword, page)

        @app.route('/api/read/<slug>')
        def read(slug):
            return scrap.get_reader_page(slug)
