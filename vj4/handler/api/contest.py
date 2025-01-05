from vj4 import app
from vj4.model import builtin
from vj4.model import document
from vj4.handler import base
from vj4.model.adaptor import contest
from vj4.util import pagination


@app.api_route("/contest", "contest_main")
class ContestMainHandler(base.Handler):
    CONTESTS_PER_PAGE = 20

    @base.require_perm(builtin.PERM_VIEW_CONTEST)
    @base.get_argument
    @base.sanitize
    async def get(self, page: int = 1):
        query = {}
        query["hidden"] = {"$ne": True}
        if self.has_perm(builtin.PERM_EDIT_CONTEST):
            del query["hidden"]
        tdocs = contest.get_multi(
            self.domain_id,
            document.TYPE_CONTEST,
            fields={
                "_id": 1,
                "begin_at": 1,
                "end_at": 1,
                "hidden": 1,
                "title": 1,
                "rule": 1,
                "attend": 1,
            },
            **query,
        )
        tdocs, tpcount, count = await pagination.paginate(
            tdocs, page, self.CONTESTS_PER_PAGE
        )
        self.json(
            {
                "page": page,
                "page_size": self.CONTESTS_PER_PAGE,
                "page_count": tpcount,
                "count": count,
                "contests": tdocs,
            }
        )
