from functools import wraps
from flask import make_response,g,current_app
# import requests
from mwsdk import Rightmanage,Rightmanage_inner

class PermissionError(Exception):
    pass

class Permission(object):
    def __init__(self,sysname=None,app=None,version='v1.0'):
        '''
        :param sys: 系统名称，如:maxguideweb
        :param app:
        :param auth: 认证方式，如：jwt
        :param version: 权限的版本，通过url取permission
        '''
        super(Permission, self).__init__()
        # 权限的版本
        self.version = version
        self.sys = sysname
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.sys = app.config.get('SYSTEM_NAME')

    def _get_permission(self):
        if current_app.config.get('DEVELOPMENT',False):
            return []
        _,result = Rightmanage_inner().permissions(self.sys, g.user_id,self.version)
        return result

    def check(self, subsystem3 , actions):
        '''
        检查某个模块的权限，装饰器
        :param subsystem3: 权限名称，比如：vehicle,employee 等
        :param actions: 是list，内容为 ['insert','edit','delete',...]
        :return: True 代表有权限，false 代表没有权限
        '''
        def decorate(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if current_app.config.get('DEVELOPMENT', False):
                    return func(*args, **kwargs)
                permissions = self._get_permission()
                permission = permissions.get(subsystem3)
                if permission is None:
                    raise Exception('the subsystem(%s) is not in %s'%(subsystem3,self.sys))
                ops = permission.get('ops')
                if not [act for act in actions if act in ops]:
                    response = make_response()
                    response.status_code = 403
                    return response
                return func(*args, **kwargs)
            return wrapper
        return decorate

    def check_permission(self,subsystem3 , action, msg=''):
        _, permissions_js = Rightmanage_inner().permissions(self.sys, g.user_id)
        permission = permissions_js.get(subsystem3)
        if permission is None:
            raise Exception('the subsystem(%s) is not exist in %s' % (subsystem3,self.sys))
        ops = permission.get('ops',[])
        if action not in ops:
            if not msg:
                msg = 'The user(%s) have no this (%s) right!' % (g.user_name, ops)
            raise PermissionError(msg)
        return True



