from .fcm import FCM, FCMMessage

__all__ = ('SanicFCM', 'FCM', 'FCMMessage')

__version__ = '0.0.1'


class SanicFCM:
    def __init__(self, app=None):
        self.app = app
        self.fcm = None
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.fcm = FCM(app.config.FCM_API_KEY)
        return self
