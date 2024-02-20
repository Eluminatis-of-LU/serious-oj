import datetime

from bson import objectid
from pymongo import errors
from pymongo import ReturnDocument

from typing import List, Tuple, Dict
from vj4 import db
from vj4 import error
from vj4.util import argmethod

@argmethod.wrap
async def count(**kwargs):
  coll = db.coll('rating')
  return await coll.find({**kwargs}).count()

@argmethod.wrap
async def ensure_indexes():
  coll = db.coll('rating')


if __name__ == '__main__':
  argmethod.invoke_by_args()