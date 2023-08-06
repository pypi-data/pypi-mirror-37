# -*- coding: utf-8 -*-


class FlipGive(object):

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        "Init app with flipgive blueprint and signals"
        import fulfil_shop_flipgive.views
        app.register_blueprint(fulfil_shop_flipgive.views.blueprint)

        from fulfil_shop_flipgive.signals import register_signals
        register_signals(app)
