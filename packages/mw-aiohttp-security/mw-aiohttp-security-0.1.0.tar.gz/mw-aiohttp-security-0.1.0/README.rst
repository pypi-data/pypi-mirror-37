`rst file editor <http://rst.ninjs.org>`_

mw-aiohttp-security
===================
maxwin 团队 aiohttp 框架下的 认证和确权


代码样例
------------------

> .app/__init__.py 生成app，初始化 auth和permission 类

.. code-block:: python

    from mw_aiohttp_security import Auth,Permission
    import asyncio
    import aioredis
    from aiohttp import web

    # 认证类
    auth = Auth()
    # 权限类
    p = Permission('maxguideweb')

    def make_app():
        async def make_redis_pool():
            redis_address = ('192.168.101.70', '6380')
            return await aioredis.create_redis_pool(redis_address, timeout=1)

        async def dispose_redis_pool(app):
            redis_pool.close()
            await redis_pool.wait_closed()

        loop = asyncio.get_event_loop()
        app = web.Application()

        redis_pool = loop.run_until_complete(make_redis_pool())

        auth.init_app(app,redis_pool)
        p.init_app(app)
        app.on_cleanup.append(dispose_redis_pool)
        # add router
        from .router import add_router
        add_router(app)
        return app

> ./app/handler.py ，检查认证：@auth.valid_login，检查有无权限： @p.check('fleet','delete')

.. code-block:: python

    from . import auth,p
    import time
    from aiohttp import web
    from aiohttp_session import get_session

    # 检查是否授权
    @auth.valid_login
    async def handler(request):
        user = request['current_user']
        # 没有权限raise 403
        p.check_permission(user.uid, 'fleet', 'auth')
        text = 'Last visited: {}'.format(time.time())
        return web.Response(text=text)

    # 检查是否有删除 fleet的权限
    @p.check('fleet','delete')
    async def say_hello(request):
        # 获取session，session中有包含user信息
        session = await get_session(request)
        # 获取当前用户 信息
        user = request['current_user']
        # 动态的检查权限
        if not p.has_permission(user.uid,'fleet','auth'):
            return web.Response(text='没有设定授权车队的权限')
        return web.Response(text='hello')

> ./app/router.py add router

.. code-block:: python

    from .handler import handler,say_hello

    def add_router(app):
        app.router.add_get('/', handler)
        app.router.add_get('/hello',say_hello)
    ```

    > .main.py ，run app
    ```python
    from aiohttp import web
    from app import make_app

    web.run_app(make_app(),port=8899)
