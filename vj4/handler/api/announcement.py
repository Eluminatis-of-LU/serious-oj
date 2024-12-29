import datetime
from vj4 import app
from vj4.model import builtin
from vj4.handler import base
from vj4.service import bus

@app.api_route('/announcement', 'announcement')
class AnnouncementHandler(base.Handler):

    @base.require_priv(builtin.PRIV_USER_PROFILE | builtin.PRIV_MAKE_ANNOUNCEMENT)
    @base.sanitize
    @base.post_argument
    @base.limit_rate("global_announcement", 3600, 10)
    async def post(self, message: str):
        await bus.publish('worker_global_announcement', {
            'message': message,
            'made_by': self.user['_id'],
            'made_at': datetime.datetime.utcnow(),
            'made_by_name': self.user['uname']
        })
        self.json(None)