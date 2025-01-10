from vj4 import db
from vj4 import error
from vj4.util import argmethod
import datetime

async def insert_judge(doc):
  coll = db.coll('judge')
  doc['created_at'] = datetime.datetime.utcnow()
  await coll.insert_one(doc)

@argmethod.wrap
async def ensure_indexes():
  coll = db.coll('judge')
  await coll.create_index([('created_at', 1)], expireAfterSeconds=60)


if __name__ == '__main__':
  argmethod.invoke_by_args()