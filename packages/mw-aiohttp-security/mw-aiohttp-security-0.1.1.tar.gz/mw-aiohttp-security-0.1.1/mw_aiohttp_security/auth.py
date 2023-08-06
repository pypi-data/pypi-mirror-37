from aiohttp_session import get_session
from aiohttp_security.abc import AbstractAuthorizationPolicy
from aiohttp_security.abc import AbstractIdentityPolicy
from functools import namedtuple
from mwsdk import AIORightmanage_inner

User = namedtuple('User', ['uid', 'uname', 'systemuser','manageuser','manageuserid'])

class MWSessionIdentityPolicy(AbstractIdentityPolicy):
    '''
    提供session认证
    '''
    def __init__(self):
        super().__init__()

    async def identify(self, request):
        session = await get_session(request)
        # "uid": "1999", "uname": "super", "systemuser": true, "manageuser": false, "manageuserid": null}
        current_user = User(uid=session.get('uid'),
                            uname=session.get('uname'),
                            systemuser=session.get('systemuser', False),
                            manageuser=session.get('manageuser', False),
                            manageuserid=session.get('manageuserid'))
        request['current_user'] = current_user
        return session.get('uid')

    async def remember(self, request, response, identity, **kwargs):
        # 不提供登入
        pass

    async def forget(self, request, response):
        # 不提供登出
        pass

class MWAuthorizationPolicy(AbstractAuthorizationPolicy):
    def __init__(self):
        super().__init__()
        self.systemname = None

    async def authorized_userid(self, identity):
        # identiy 为 user.uid
        return identity

    async def permits(self, identity, permission, context=None):
        '''
        调用权限服务，检测权限
        :param identity: user_id
        :param permission: subsystem，如：vehicle,fleet。。。
        :param context: ops，权限的操作，必须是list
        :return:
        '''
        if identity is None:
            return False
        assert context ,'context can not be null'
        assert self.systemname,'please assign systemname'
        rm = AIORightmanage_inner()
        _,permissions = await rm.permissions(self.systemname,identity)
        permission_rm = permissions.get(permission)
        if permission_rm is None:
            raise Exception('the permission(%s) is not exist in the system(%s)' % (permission,self.systemname))
        ops = permission_rm.get('ops',[])
        return context in ops

