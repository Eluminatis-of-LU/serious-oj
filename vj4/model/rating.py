import datetime

from bson import objectid
from pymongo import errors
from pymongo import ReturnDocument

from typing import List, Tuple, Dict
from vj4 import db
from vj4 import error
from vj4.util import argmethod


async def add(
    domain_id: str, contest_id: str, contest_title: str, attend_at: datetime.datetime
):
    coll = db.coll("rating")
    obj_id = contest_id
    rating_doc = {
        "_id": contest_id,
        "domain_id": domain_id,
        "attend_at": attend_at,
        "contest_title": contest_title,
    }
    inserted_doc = await coll.find_one_and_update(
        filter={"_id": obj_id},
        update={"$set": rating_doc},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )


async def add_rating_changes(domain_id: str, rating_changes: List[Dict]):
    bulk_rating_changes = db.coll("rating_changes").initialize_unordered_bulk_op()
    bulk_domain_users = db.coll("domain.user").initialize_unordered_bulk_op()
    for rating_change in rating_changes:
        bulk_rating_changes.insert(rating_change)
        bulk_domain_users.find(
            {"domain_id": domain_id, "uid": rating_change["uid"]}
        ).update({"$set": {"rating": rating_change["new_rating"]}})
    await bulk_rating_changes.execute()
    await bulk_domain_users.execute()


async def get_latest_rating_changes(domain_id: str, uids: List[int]):
    coll = db.coll("domain.user")
    return await coll.find({"domain_id": domain_id, "uid": {"$in": uids}}).to_list()


async def delete_rating(domain_id: str, contest_id: str):
    coll = db.coll("rating")
    await coll.delete_one({"_id": contest_id, "domain_id": domain_id})


@argmethod.wrap
async def clear_all_ratings(domain_id: str):
    coll = db.coll("rating_changes")
    await coll.delete_many({"domain_id": domain_id})
    coll = db.coll("domain.user")
    await coll.update_many({"domain_id": domain_id}, {"$unset": {"rating": ""}})


@argmethod.wrap
async def purge_all_ratings(domain_id: str):
    coll = db.coll("rating")
    await coll.delete_many({"domain_id": domain_id})
    coll = db.coll("rating_changes")
    await coll.delete_many({"domain_id": domain_id})
    coll = db.coll("domain.user")
    await coll.update_many({"domain_id": domain_id}, {"$unset": {"rating": ""}})


@argmethod.wrap
async def get_user_rating_changes(domain_id: str, uid: int):
    coll = db.coll("rating_changes")
    return await coll.find({"domain_id": domain_id, "uid": uid}).to_list()


@argmethod.wrap
async def get_user_rating(domain_id: str, uid: int):
    coll = db.coll("domain.user")
    return await coll.find_one({"domain_id": domain_id, "uid": uid}, {"rating": 1})


@argmethod.wrap
async def list(**kwargs):
    coll = db.coll("rating")
    return await coll.find({**kwargs}).to_list()


@argmethod.wrap
async def count(**kwargs):
    coll = db.coll("rating")
    return await coll.find({**kwargs}).count()


async def get_sorted_by_attend_at(domain_id: str):
    coll = db.coll("rating")
    return await coll.find({"domain_id": domain_id}).sort("attend_at", 1).to_list()


@argmethod.wrap
async def ensure_indexes():
    coll = db.coll("rating")
    await coll.create_index([("domain_id", 1), ("attend_at", 1)])
    await coll.create_index([("domain_id", 1), ("contest_id", 1)])
    coll = db.coll("rating_changes")
    await coll.create_index([("rating_id", 1), ("uid", 1)], unique=True)
    await coll.create_index([("domain_id", 1), ("uid", 1)])
    await coll.create_index([("rating_id", 1), ("rank", 1)])
    coll = db.coll("domain.user")
    await coll.create_index([("domain_id", 1), ("uid", 1), ("rating", 1)])


if __name__ == "__main__":
    argmethod.invoke_by_args()
