import importlib


class Sources:
    initialized = False

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        # initialize sources only one time
        if self.initialized:
            return False

        for source in app.config.get('API_MODULES'):
            path = f'app.sources.{source}'
            source = importlib.import_module(path)
            source.init()

        self.initialized = True


sources = Sources()
