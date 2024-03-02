import datetime
import math

from bson import objectid
from pymongo import errors
from pymongo import ReturnDocument

from typing import List, Tuple, Dict
from vj4 import db
from vj4 import error
from vj4.model import document
from vj4.model import rating as rating_model
from vj4.model.adaptor import contest
from vj4.util import argmethod

class Contestant:
    uid: int
    rank: int
    rating: int  # previous rating

    seed: float
    need_rating: int
    delta: int

    def __init__(self, uid, rank, previous_rating):
        self.uid = uid
        self.rank = rank
        self.rating = previous_rating

        self.seed = 0.0
        self.need_rating = 0
        self.delta = 0


def get_seed(contestants, rating, seed_cache):
    if rating in seed_cache:
        return seed_cache[rating]

    extra = Contestant(None, 0, rating)
    result = 1
    for other in contestants:
        result += get_elo_win_probability(other.rating, extra.rating)
    seed_cache[rating] = result
    return result


def get_rating_to_rank(contestants, rank, seed_cache):
    left = 1
    right = 8000
    while right - left > 1:
        mid = (left + right) // 2
        if get_seed(contestants, mid, seed_cache) < rank:
            right = mid
        else:
            left = mid
    return left


def get_elo_win_probability(ra, rb):
    return 1.0 / (1.0 + math.pow(10, (rb - ra) / 400.0))

def sort_by_rating_desc(contestants):
    contestants.sort(key=lambda x: x.rating, reverse=True)

def process(contestants):
    if not contestants:
        return
    
    # Caches the calculated seed for a given rating
    seed_cache = {}

    for contestant in contestants:
        rating = contestant.rating
        contestant.seed = get_seed(contestants, rating, seed_cache) - 0.5
        mid_rank = math.sqrt(contestant.rank * contestant.seed)
        contestant.need_rating = get_rating_to_rank(
            contestants, mid_rank, seed_cache
        )
        contestant.delta = (contestant.need_rating - rating) // 2

    sort_by_rating_desc(contestants)

    # Total sum should not be more than zero
    def total_sum_not_more_than_zero():
        sum = 0
        for c in contestants:
            sum += c.delta
        inc = -sum // len(contestants) - 1
        for c in contestants:
            c.delta += inc

    total_sum_not_more_than_zero()

    # Sum of top-4*sqrt should be adjusted to zero
    def adjust_sum():
        sum = 0
        calc = int(4 * round(math.sqrt(len(contestants))))
        zero_sum_count = min(calc, len(contestants))
        for i in range(zero_sum_count):
            sum += contestants[i].delta
        inc = min(0, max(-sum // zero_sum_count, -10))
        for c in contestants:
            c.delta += inc

    adjust_sum()


def calculate_rating_changes(contestants: List[Contestant]) -> Dict[int, int]:
    # List will be modified by process function (passed by reference)
    process(contestants)
    
    rating_changes = {}
    for c in contestants:
        rating_changes[c.uid] = c.delta
    return rating_changes

@argmethod.wrap
async def process_contest_rating(domain_id: str, tid: objectid.ObjectId):
    tdoc, rows, udict = await contest.get_scoreboard_details(domain_id, document.TYPE_CONTEST, tid, True, False)
    previous_rating = {}
    
    previous_rating_changes = await rating_model.get_latest_rating_changes(domain_id, [u for u in udict])
       
    for u in previous_rating_changes:
        previous_rating[u['uid']] = u['rating'] if 'rating' in u else 400
    contestants: List[Contestant] = []
    
    print('previous_rating:', previous_rating)
    
    for row in rows[1:]:
        uid = row[1]['raw']['_id']
        rank = row[0]['value']
        prev_rating = previous_rating[uid]
        c = Contestant(uid, rank, prev_rating)
        contestants.append(c)
        
    rating_delta = calculate_rating_changes(contestants)
    rating_changes = []
    for uid in rating_delta:
        print(uid, '->', rating_delta[uid])
        rating_changes.append({'uid': uid, 'new_rating': previous_rating[uid] + rating_delta[uid], 'delta': rating_delta[uid], 'previous_rating': previous_rating[uid]})
        
    await rating_model.add(domain_id, tid, tdoc['title'], rating_changes, tdoc['begin_at'], datetime.datetime.utcnow())

    return rating_changes

if __name__ == '__main__':
  argmethod.invoke_by_args()
