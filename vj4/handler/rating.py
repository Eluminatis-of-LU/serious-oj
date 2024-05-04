from vj4 import app
from vj4.model import builtin
from vj4.model import domain
from vj4.model import user
from vj4.model import rating as rating_model
from vj4.job import rating as rating_job
from vj4.util import pagination
from vj4.handler import base
from bson import objectid

@app.route('/rating/purge', 'rating_purge_all')
class RatingPurgeHandler(base.Handler):
  
  @base.require_perm(builtin.PERM_PROCESS_RATING)
  @base.get_argument
  @base.sanitize
  async def get(self):
    await rating_model.purge_all_ratings(domain_id=self.domain_id)
    self.redirect(self.reverse_url('domain_main'))

@app.route('/rating/clear', 'rating_clear_all')
class RatingClearHandler(base.Handler):
  
  @base.require_perm(builtin.PERM_PROCESS_RATING)
  @base.get_argument
  @base.sanitize
  async def get(self):
    await rating_model.clear_all_ratings(domain_id=self.domain_id)
    self.redirect(self.reverse_url('domain_main'))

@app.route('/rating/{tid:\w{24}}/add', 'rating_add')
class RatingAddHandler(base.Handler):
  
  @base.require_perm(builtin.PERM_PROCESS_RATING)
  @base.get_argument
  @base.route_argument
  @base.sanitize
  async def get(self, *, tid: objectid.ObjectId):
    await rating_job.add_contest_to_rating(domain_id=self.domain_id, tid=tid)
    self.redirect(self.reverse_url('contest_detail', tid=tid))

@app.route('/rating/{tid:\w{24}}/delete', 'rating_delete')
class RatingDeleteHandler(base.Handler):
  
  @base.require_perm(builtin.PERM_PROCESS_RATING)
  @base.get_argument
  @base.route_argument
  @base.sanitize
  async def get(self, *, tid: objectid.ObjectId):
    await rating_model.delete_rating(domain_id=self.domain_id, contest_id=tid)
    self.redirect(self.reverse_url('contest_detail', tid=tid))

@app.route('/rating/process', 'rating_process')
class RatingProcessHandler(base.Handler):
  
  @base.require_perm(builtin.PERM_PROCESS_RATING)
  @base.get_argument
  @base.sanitize
  async def get(self):
    await rating_model.clear_all_ratings(domain_id=self.domain_id)
    await rating_job.process_all_contest_ratings(domain_id=self.domain_id)
    self.redirect(self.reverse_url('domain_main'))