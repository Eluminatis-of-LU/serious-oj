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
from vj4.service import bus


def is_moderator_or_admin(handler, tdoc):
  """Check if user is contest moderator or has admin permission."""
  return (contest.is_contest_moderator(tdoc, handler.user['_id']) or
          handler.has_perm(builtin.PERM_EDIT_CONTEST))


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
  @base.require_csrf_token
  @base.route_argument
  @base.post_argument
  @base.sanitize
  async def post(self, *, cqid: document.convert_doc_id, answer_content: str):
    cqdoc = await clarification.get(self.domain_id, cqid)
    if not cqdoc:
      raise error.DocumentNotFoundError(self.domain_id, document.TYPE_CLARIFICATION_QUESTION, cqid)
    
    # Get contest document to check moderator status
    if cqdoc.get('parent_doc_type') == document.TYPE_CONTEST:
      tdoc = await contest.get(self.domain_id, document.TYPE_CONTEST, cqdoc['parent_doc_id'])
      # Only contest moderators or admins can answer
      if not is_moderator_or_admin(self, tdoc):
        raise error.PermissionError(builtin.PERM_ANSWER_CLARIFICATION)
    else:
      # Fallback to permission check for non-contest clarifications
      self.check_perm(builtin.PERM_ANSWER_CLARIFICATION)
    
    await clarification.answer(self.domain_id, cqid, self.user['_id'], answer_content)
    
    # Send push notification to the question asker
    if cqdoc['owner_uid'] != self.user['_id']:
      notification_data = {
        'type': 'clarification_answered',
        'title': 'Clarification Answered',
        'message': f"Your clarification question '{cqdoc['title']}' has been answered.",
        'url': self.reverse_url('contest_detail', tid=cqdoc['parent_doc_id']) if cqdoc.get('parent_doc_type') == document.TYPE_CONTEST else None
      }
      try:
        await bus.publish(f'push_received-{cqdoc["owner_uid"]}', notification_data)
      except Exception:
        pass  # Don't fail if notification fails
    
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
    
    # Get contest document to check moderator status
    if cqdoc.get('parent_doc_type') == document.TYPE_CONTEST:
      tdoc = await contest.get(self.domain_id, document.TYPE_CONTEST, cqdoc['parent_doc_id'])
      # Only contest moderators or admins can mark as private
      if not is_public:  # Making it private
        if not is_moderator_or_admin(self, tdoc):
          raise error.PermissionError(builtin.PERM_EDIT_CLARIFICATION)
      # Anyone can make their own question public, moderators can change any
      elif cqdoc['owner_uid'] != self.user['_id'] and not is_moderator_or_admin(self, tdoc):
        raise error.PermissionError(builtin.PERM_EDIT_CLARIFICATION)
    else:
      # Check permissions for non-contest clarifications
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
  @base.require_csrf_token
  @base.route_argument
  @base.post_argument
  @base.sanitize
  async def post(self, *, cqid: document.convert_doc_id, is_announcement: bool):
    cqdoc = await clarification.get(self.domain_id, cqid)
    if not cqdoc:
      raise error.DocumentNotFoundError(self.domain_id, document.TYPE_CLARIFICATION_QUESTION, cqid)
    
    # Get contest document to check moderator status
    if cqdoc.get('parent_doc_type') == document.TYPE_CONTEST:
      tdoc = await contest.get(self.domain_id, document.TYPE_CONTEST, cqdoc['parent_doc_id'])
      # Only contest moderators or admins can mark as announcement
      if not is_moderator_or_admin(self, tdoc):
        raise error.PermissionError(builtin.PERM_ANSWER_CLARIFICATION)
      
      # If marking as announcement, send notifications to all contest attendees
      if is_announcement:
        # Get all contest attendees
        try:
          tsdocs = await contest.get_multi_status(
              document.TYPE_CONTEST,
              domain_id=self.domain_id,
              doc_id=tdoc['doc_id'],
              fields={'uid': 1}
          ).to_list()
          
          # Send push notification to each attendee (except the sender)
          notification_data = {
            'type': 'clarification_announcement',
            'title': 'Contest Announcement',
            'message': f"Announcement: {cqdoc['title']}",
            'url': self.reverse_url('contest_detail', tid=tdoc['doc_id'])
          }
          for tsdoc in tsdocs:
            if tsdoc['uid'] != self.user['_id']:
              try:
                await bus.publish(f'push_received-{tsdoc["uid"]}', notification_data)
              except Exception:
                pass  # Don't fail if individual notification fails
        except Exception:
          pass  # Don't fail if notification system fails
    else:
      # Fallback to permission check for non-contest clarifications
      self.check_perm(builtin.PERM_ANSWER_CLARIFICATION)
    
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
    
    # Get contest document to check moderator status
    if cqdoc.get('parent_doc_type') == document.TYPE_CONTEST:
      tdoc = await contest.get(self.domain_id, document.TYPE_CONTEST, cqdoc['parent_doc_id'])
      # Only contest moderators or admins can delete
      if not is_moderator_or_admin(self, tdoc):
        raise error.PermissionError(builtin.PERM_DELETE_CLARIFICATION)
    else:
      # Check permissions for non-contest clarifications
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
