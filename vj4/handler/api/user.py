from vj4 import app
from vj4 import error
from vj4.model import builtin
from vj4.model import system
from vj4.model import user
from vj4.handler import base
from vj4.util import validator


@app.api_route(r'/user/{uid:-?\d+}', 'user_detail_api')
class UserDetailApiHandler(base.Handler):
    @base.require_perm(builtin.PERM_EDIT_USER)
    @base.route_argument
    @base.sanitize
    async def get(self, *, uid: int):
        udoc = await user.get_by_uid(uid, user.PROJECTION_PUBLIC)
        if not udoc:
            raise error.UserNotFoundError(uid)
        self.json(udoc)

    @base.require_perm(builtin.PERM_EDIT_USER)
    @base.route_argument
    @base.post_argument
    @base.sanitize
    async def post(self, *, uid: int, mail: str = ''):
        udoc = await user.get_by_uid(uid)
        if not udoc:
            raise error.UserNotFoundError(uid)
        if mail:
            validator.check_mail(mail)
            await user.set_mail(uid, mail)
        self.json(None)


@app.api_route('/user', 'user_create_api')
class UserCreateApiHandler(base.Handler):
    @base.require_perm(builtin.PERM_EDIT_USER)
    @base.post_argument
    @base.sanitize
    async def post(self, *, uname: str, password: str, mail: str):
        validator.check_uname(uname)
        validator.check_password(password)
        validator.check_mail(mail)
        if await user.get_by_uname(uname):
            raise error.UserAlreadyExistError(uname)
        if await user.get_by_mail(mail):
            raise error.UserAlreadyExistError(mail)
        uid = await system.inc_user_counter()
        await user.add(uid, uname, password, mail, self.remote_ip)
        self.json({'uid': uid})


@app.api_route(r'/user/{uid:-?\d+}/password', 'user_password_api')
class UserPasswordApiHandler(base.Handler):
    @base.require_perm(builtin.PERM_EDIT_USER)
    @base.route_argument
    @base.post_argument
    @base.sanitize
    async def post(self, *, uid: int, password: str):
        udoc = await user.get_by_uid(uid)
        if not udoc:
            raise error.UserNotFoundError(uid)
        validator.check_password(password)
        await user.set_password(uid, password)
        self.json(None)
