import src.success as sukses
import src.scrap as scrap


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
            return scrap.get_detail_manga()
