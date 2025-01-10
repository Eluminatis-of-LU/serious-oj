from vj4 import db
from vj4 import error
from vj4.util import argmethod
import datetime


async def checkin(doc):
    coll = db.coll("judge")
    expire_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
    doc["expire_at"] = expire_at
    await coll.find_one_and_update(
        {"_id": doc['name']}, {"$set": {"expire_at": expire_at}}, upsert=True
    )


@argmethod.wrap
async def ensure_indexes():
    coll = db.coll("judge")
    await coll.create_index("expire_at", expireAfterSeconds=0)


if __name__ == "__main__":
    argmethod.invoke_by_args()
