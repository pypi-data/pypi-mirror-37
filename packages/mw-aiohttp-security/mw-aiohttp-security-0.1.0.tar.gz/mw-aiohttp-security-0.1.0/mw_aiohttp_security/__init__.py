from .auth import MWAuthorizationPolicy,MWSessionIdentityPolicy
from aiohttp_session import setup as setup_session
from aiohttp import web
from mw_aiohttp_session.redis_storage import RedisStorage
from aiohttp_security import setup as setup_security
from aiohttp_security.api import check_authorized,check_permission,AUTZ_KEY
from functools import wraps

class Auth():
    def init_app(self,app,redis_pool):
        assert app is not None
        if not isinstance(app, web.Application):
            msg = ("app(%s) must be aiohttp.web.Application"%app)
            raise RuntimeError(msg)
        setup_session(app, RedisStorage(redis_pool))
        setup_security(app, MWSessionIdentityPolicy(),MWAuthorizationPolicy())

    def valid_login(self,fn):
        """Decorator that restrict access only for authorized users.
        兼容maxwin团队 flask的auth方法
        User is considered authorized if authorized_userid
        returns some value.
        """
        @wraps(fn)
        async def wrapped(*args, **kwargs):
            request = args[-1]
            if not isinstance(request, web.BaseRequest):
                msg = ("Incorrect decorator usage. "
                       "Expecting `def handler(request)` "
                       "or `def handler(self, request)`.")
                raise RuntimeError(msg)
            await check_authorized(request)
            return await fn(*args, **kwargs)
        return wrapped

class Permission():
    def __init__(self,systemname):
        '''
        :param systemname: 权限系统的名称,如：maxguideweb
        '''
        self.systemname = systemname
        self.authorization_policy = None

    def init_app(self,app):
        assert app
        if not isinstance(app, web.Application):
            msg = ("app(%s) must be aiohttp.web.Application"%app)
            raise RuntimeError(msg)
        self.authorization_policy = app[AUTZ_KEY]
        assert self.authorization_policy ,'Please auth.init_app(app) first'
        self.authorization_policy.systemname = self.systemname

    def check(self, subsystem , action):
        '''
        检查某个模块的权限
        :param subsystem: 模块名称,比如：
        :param action: 是str，内容为 'insert','edit','delete',...
        :return: True 代表有权限，false 代表没有权限
        '''
        def wrapper(fn):
            @wraps(fn)
            async def wrapped(*args, **kwargs):
                request = args[-1]
                if not isinstance(request, web.BaseRequest):
                    msg = ("Incorrect decorator usage. "
                           "Expecting `def handler(request)` "
                           "or `def handler(self, request)`.")
                    raise RuntimeError(msg)
                await check_permission(request, subsystem, action)
                return await fn(*args, **kwargs)
            return wrapped
        assert isinstance(action, str),'action(%s) must be str'%action
        return wrapper

    async def check_permission(self,user_id, subsystem3 , action):
        '''
        检查某权限项是否有权限
        :param user_id: 用户id
        :param subsystem3: 如：vehicle，fleet。。。
        :param action: insert ,view 。。。
        :return:
        '''
        assert self.authorization_policy, 'Please init_app(app) first!'
        allowed = await self.authorization_policy.permits( user_id, subsystem3,action)
        if not allowed:
            raise web.HTTPForbidden()

    async def has_permission(self,user_id, subsystem3 , action):
        '''
                检查某权限项是否有权限
                :param user_id: 用户id
                :param subsystem3: 如：vehicle，fleet。。。
                :param action: insert ,view 。。。
                :return:
                '''
        assert self.authorization_policy, 'Please init_app(app) first!'
        return await self.authorization_policy.permits(user_id, subsystem3, action)


