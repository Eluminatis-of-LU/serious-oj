from vj4 import db
from vj4 import error
from vj4.util import argmethod
import datetime


async def checkin(doc):
    coll = db.coll("judge")
    expire_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
    doc["expire_at"] = expire_at
    await coll.insert_one(doc)


@argmethod.wrap
async def ensure_indexes():
    coll = db.coll("judge")
    await coll.create_index("expire_at", expireAfterSeconds=0)


if __name__ == "__main__":
    argmethod.invoke_by_args()
