import src.error as not_found


class Routes:
    @staticmethod
    def run(app):

        @app.route('/')
        def index():
            return not_found.error(404, 'Not found')
