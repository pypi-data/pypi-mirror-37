`rst file editor <http://rst.ninjs.org>`_
mw_aiohttp_babel
===================
修改aiohttp_babel源码，使它能适应 maxwin团队的开发框架

aiohttp_babel adds i18n and l10n support to aiohttp.

变更：
--------
1，增加类似flask_babel的Babel类
2，_() 直接调用 babel.support.Translations.translation,原来的_()改为了lazy_gettext()

Babel使用样例：
------------------

.. code-block:: python

    import aiohttp_jinja2
    from mw_aiohttp.web import Application
    from mw_aiohttp_babel import Babel,_

    babel = Babel(directory='/path/to/locales', domain='messages',default_locale='en_US')

    # you can use your own locale detection method, if necessary.
    # aiohttp_babel checks cookie parameter `locale` or `Accept-Language`
    # header by default.
    # def detector(request):
    #     if request.url.host == 'es.example.com':
    #         return 'es'
    #     elif request.url.host == 'zh.example.com':
    #         return 'zh'
    #     else:
    #         return 'en'
    # set_locale_detector(detector)

    jinja_loader = jinja2.FileSystemLoader('./templates')
    app = Application()
    babel.init_app(app)
    aiohttp_jinja2.setup(app, loader=jinja_loader)
    jinja_env = aiohttp_jinja2.get_env(app)
    jinja_env.globals['_'] = _

保留aiohttp_babel的样例：
----------------------------

.. code-block:: python

    import aiohttp_jinja2
    from mw_aiohttp.web import Application
    from mw_aiohttp_babel.locale import (load_gettext_translations,
                                      set_default_locale,
                                      set_locale_detector)
    from mw_aiohttp_babel.middlewares import babel_middleware, lazy_gettext as _


    set_default_locale('en_GB')  # set default locale, if necessary
    # load compiled locales
    load_gettext_translations('/path/to/locales', 'domain')

    # you can use your own locale detection method, if necessary.
    # aiohttp_babel checks cookie parameter `locale` or `Accept-Language`
    # header by default.
    def detector(request):
        if request.url.host == 'es.example.com':
            return 'es'
        elif request.url.host == 'zh.example.com':
            return 'zh'
        else:
            return 'en'
    set_locale_detector(detector)

    jinja_loader = jinja2.FileSystemLoader('./templates')
    app = Application(middlewares=[babel_middleware])

    aiohttp_jinja2.setup(app, loader=jinja_loader)
    jinja_env = aiohttp_jinja2.get_env(app)
    jinja_env.globals['_'] = _



创建多语言文件 :
--------------------

1. 创建pot模板

   ``$ pybabel extract -F babel.cfg -o messages.pot app``

2. 创建多语言的po文件

   > 简体中文

   ``$ pybabel init -i messages.pot -d app/translations -l zh_CN``

   > 繁体中文

   ``$ pybabel init -i messages.pot -d app/translations -l zh_TW``

   > 英文

   ``$ pybabel init -i messages.pot -d app/translations -l en``

3. 更新多语言的po文件

   ``$ pybabel update -i messages.pot -d app/translations``

4. 产生mo文件

   ``$ pybabel compile -d app/translations``

How to extract & compile locales:
----------------------------------

http://babel.pocoo.org/en/latest/messages.html

http://babel.pocoo.org/en/latest/cmdline.html


Code from:
-----------

tornado-babel: https://github.com/openlabs/tornado-babel

django-babel: https://github.com/python-babel/django-babel


