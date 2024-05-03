from vj4 import app
from vj4.model import builtin
from vj4.model import domain
from vj4.model import user
from vj4.model import rating as rating_model
from vj4.job import rating as rating_job
from vj4.util import pagination
from vj4.handler import base

@app.route('/rating/clearall', 'rating_clear_all')
class RatingClearHandler(base.Handler):
  
  @base.require_perm(builtin.PERM_PROCESS_RATING)
  @base.get_argument
  @base.sanitize
  async def get(self):
    await rating_model.clear_all_ratings(domain_id=self.domain_id)
    self.redirect(self.referer_or_main)

@app.route('/rating/{tid}', 'rating_calculate')
class RatingCalculationHandler(base.Handler):
  
  @base.require_perm(builtin.PERM_PROCESS_RATING)
  @base.get_argument
  @base.route_argument
  @base.sanitize
  async def get(self, *, tid: objectid.ObjectId):
    rating_changes = await rating_job.process_contest_rating(domain_id=self.domain_id, tid=tid)
    self.redirect(self.referer_or_main)

@app.route('/rating/rollback', 'rating_rollback_last')
class RatingRollbackHandler(base.Handler):
  
  @base.require_perm(builtin.PERM_PROCESS_RATING)
  @base.get_argument
  @base.sanitize
  async def get(self):  
    self.redirect(self.referer_or_main)