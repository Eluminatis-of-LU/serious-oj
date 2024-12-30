from vj4.service import bus
from vj4.model import user
import logging

_logger = logging.getLogger(__name__)

async def _on_global_announcement(data):
    value = data.get('value')
    _logger.info("Global announcement: %s", value)
    async for udoc in user.get_multi(fields={'_id': 1}):
        bus.publish_throttle('push_received-' + str(udoc['_id']), {
            'type': 'window-alert',
            'message': value['message']
        }, udoc['_id'])

def init():
    bus.subscribe(_on_global_announcement, ["worker_global_announcement"])