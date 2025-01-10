from vj4 import db
from vj4 import error
from vj4.util import argmethod
import datetime


async def checkin(name: str, version: str, concurrency: int):
    coll = db.coll("judge")
    expire_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    await coll.find_one_and_update(
        {"_id": name},
        {
            "$set": {
                "expire_at": expire_at,
                "version": version,
                "concurrency": concurrency,
            }
        },
        upsert=True,
    )

def get_all():
    coll = db.coll("judge")
    return coll.find()


@argmethod.wrap
async def ensure_indexes():
    coll = db.coll("judge")
    await coll.create_index("expire_at", expireAfterSeconds=0)


if __name__ == "__main__":
    argmethod.invoke_by_args()
