import src.success as sukses
import src.scrap as scrap
from flask import request as req


class Routes:
    @staticmethod
    def run(app):

        @app.route('/')
        def index():
            return sukses.success()

        @app.route('/home')
        def home():
            return scrap.get_homepage()

        @app.route('/genre')
        def genre():
            return scrap.get_genre()

        @app.route('/project/all')
        def project():
            return scrap.get_allproject()

        @app.route('/project')
        def project_page():
            return scrap.get_project()

        @app.route('/mangalist')
        def mangalist():
            return scrap.get_manga_list()

        @app.route('/manga')
        def manga():
            return scrap.get_detail_manga(req.args.get("link"))

        @app.route('/search')
        def search():
            return scrap.search_komik()

        @app.route('/read')
        def read():
            return scrap.get_reader_page(req.args.get('link'))
