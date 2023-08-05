====
Wechat user
====

Wechat-user is a app for wehcat user authencation

Quick start
-----------

1 Add 'wechat-user' to your INSTALLED_APPS settings like this::

    INSTALLED_APPS = [
        ...
        'wechat-user',
    ]

2 Include the wechat-user URLconf in your project urls.py like this::

        path('wx/', include('wechat-user.urls'))

3 Run `python manage.py migrate` to create the wechat-user models
