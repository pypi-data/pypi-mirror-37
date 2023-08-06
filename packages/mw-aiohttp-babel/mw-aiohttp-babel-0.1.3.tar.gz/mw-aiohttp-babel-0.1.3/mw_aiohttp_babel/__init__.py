##################
#封装Babel 类，类似 flask_babel
##################
from .middlewares import gettext,gettext as _
from .middlewares import laze_gettext
from .middlewares import babel_middleware
from .locale import load_gettext_translations,set_default_locale

class Babel():
    def __init__(self,directory='./app/translations',domain='messages',default_locale='zh_TW'):
        load_gettext_translations(directory,domain)
        set_default_locale(default_locale)

    def init_app(self,app):
        app.middlewares.append(babel_middleware)
