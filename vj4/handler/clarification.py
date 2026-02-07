import asyncio
from bson import objectid

from vj4 import app
from vj4 import error
from vj4.model import builtin
from vj4.model import document
from vj4.model import user
from vj4.model import domain
from vj4.model.adaptor import clarification
from vj4.model.adaptor import contest
from vj4.handler import base


@app.route('/contest/{tid}/clarify', 'clarification_create')
class ClarificationCreateHandler(base.Handler):
  @base.require_priv(builtin.PRIV_USER_PROFILE)
  @base.require_perm(builtin.PERM_CREATE_CLARIFICATION)
  @base.require_csrf_token
  @base.route_argument
  @base.post_argument
  @base.sanitize
  async def post(self, *, tid: objectid.ObjectId, title: str, content: str,
                 is_public: bool=True):
    tdoc = await contest.get(self.domain_id, document.TYPE_CONTEST, tid)
    if not tdoc:
      raise error.ContestNotFoundError(self.domain_id, tid)
    cqid = await clarification.add(self.domain_id,
                                   document.TYPE_CONTEST,
                                   tdoc['doc_id'],
                                   self.user['_id'],
                                   title,
                                   content,
                                   is_public,
                                   self.remote_ip)
    self.json_or_redirect(self.reverse_url('contest_detail', tid=tdoc['doc_id']))


@app.route('/clarify/{cqid}/answer', 'clarification_answer')
class ClarificationAnswerHandler(base.Handler):
  @base.require_priv(builtin.PRIV_USER_PROFILE)
  @base.require_perm(builtin.PERM_ANSWER_CLARIFICATION)
  @base.require_csrf_token
  @base.route_argument
  @base.post_argument
  @base.sanitize
  async def post(self, *, cqid: document.convert_doc_id, answer_content: str):
    cqdoc = await clarification.get(self.domain_id, cqid)
    if not cqdoc:
      raise error.DocumentNotFoundError(self.domain_id, document.TYPE_CLARIFICATION_QUESTION, cqid)
    await clarification.answer(self.domain_id, cqid, self.user['_id'], answer_content)
    # Redirect back to the parent contest
    if cqdoc.get('parent_doc_type') == document.TYPE_CONTEST:
      self.json_or_redirect(self.reverse_url('contest_detail', tid=cqdoc['parent_doc_id']))
    else:
      self.json_or_redirect(self.url)


@app.route('/clarify/{cqid}/toggle-visibility', 'clarification_toggle_visibility')
class ClarificationToggleVisibilityHandler(base.Handler):
  @base.require_priv(builtin.PRIV_USER_PROFILE)
  @base.require_csrf_token
  @base.route_argument
  @base.post_argument
  @base.sanitize
  async def post(self, *, cqid: document.convert_doc_id, is_public: bool):
    cqdoc = await clarification.get(self.domain_id, cqid)
    if not cqdoc:
      raise error.DocumentNotFoundError(self.domain_id, document.TYPE_CLARIFICATION_QUESTION, cqid)
    # Check permissions
    if cqdoc['owner_uid'] != self.user['_id']:
      self.check_perm(builtin.PERM_EDIT_CLARIFICATION)
    else:
      self.check_perm(builtin.PERM_EDIT_CLARIFICATION_SELF)
    await clarification.set_visibility(self.domain_id, cqid, is_public)
    # Redirect back to the parent contest
    if cqdoc.get('parent_doc_type') == document.TYPE_CONTEST:
      self.json_or_redirect(self.reverse_url('contest_detail', tid=cqdoc['parent_doc_id']))
    else:
      self.json_or_redirect(self.url)


@app.route('/clarify/{cqid}/toggle-announcement', 'clarification_toggle_announcement')
class ClarificationToggleAnnouncementHandler(base.Handler):
  @base.require_priv(builtin.PRIV_USER_PROFILE)
  @base.require_perm(builtin.PERM_ANSWER_CLARIFICATION)
  @base.require_csrf_token
  @base.route_argument
  @base.post_argument
  @base.sanitize
  async def post(self, *, cqid: document.convert_doc_id, is_announcement: bool):
    cqdoc = await clarification.get(self.domain_id, cqid)
    if not cqdoc:
      raise error.DocumentNotFoundError(self.domain_id, document.TYPE_CLARIFICATION_QUESTION, cqid)
    await clarification.set_announcement(self.domain_id, cqid, is_announcement)
    # Redirect back to the parent contest
    if cqdoc.get('parent_doc_type') == document.TYPE_CONTEST:
      self.json_or_redirect(self.reverse_url('contest_detail', tid=cqdoc['parent_doc_id']))
    else:
      self.json_or_redirect(self.url)


@app.route('/clarify/{cqid}/edit', 'clarification_edit')
class ClarificationEditHandler(base.Handler):
  @base.require_priv(builtin.PRIV_USER_PROFILE)
  @base.require_csrf_token
  @base.route_argument
  @base.post_argument
  @base.sanitize
  async def post(self, *, cqid: document.convert_doc_id, title: str, content: str):
    cqdoc = await clarification.get(self.domain_id, cqid)
    if not cqdoc:
      raise error.DocumentNotFoundError(self.domain_id, document.TYPE_CLARIFICATION_QUESTION, cqid)
    # Check permissions
    if cqdoc['owner_uid'] != self.user['_id']:
      self.check_perm(builtin.PERM_EDIT_CLARIFICATION)
    else:
      self.check_perm(builtin.PERM_EDIT_CLARIFICATION_SELF)
    await clarification.edit(self.domain_id, cqid, title=title, content=content)
    # Redirect back to the parent contest
    if cqdoc.get('parent_doc_type') == document.TYPE_CONTEST:
      self.json_or_redirect(self.reverse_url('contest_detail', tid=cqdoc['parent_doc_id']))
    else:
      self.json_or_redirect(self.url)


@app.route('/clarify/{cqid}/delete', 'clarification_delete')
class ClarificationDeleteHandler(base.Handler):
  @base.require_priv(builtin.PRIV_USER_PROFILE)
  @base.require_csrf_token
  @base.route_argument
  @base.sanitize
  async def post(self, *, cqid: document.convert_doc_id):
    cqdoc = await clarification.get(self.domain_id, cqid)
    if not cqdoc:
      raise error.DocumentNotFoundError(self.domain_id, document.TYPE_CLARIFICATION_QUESTION, cqid)
    # Check permissions
    if cqdoc['owner_uid'] != self.user['_id']:
      self.check_perm(builtin.PERM_DELETE_CLARIFICATION)
    else:
      self.check_perm(builtin.PERM_DELETE_CLARIFICATION_SELF)
    await clarification.delete(self.domain_id, cqid)
    # Redirect back to the parent contest
    if cqdoc.get('parent_doc_type') == document.TYPE_CONTEST:
      self.json_or_redirect(self.reverse_url('contest_detail', tid=cqdoc['parent_doc_id']))
    else:
      self.json_or_redirect(self.url)
