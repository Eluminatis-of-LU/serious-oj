import asyncio
import datetime
from bson import objectid

from vj4 import db
from vj4 import error
from vj4.model import builtin
from vj4.model import document
from vj4.util import argmethod
from vj4.util import validator


@argmethod.wrap
async def add(domain_id: str, parent_doc_type: int, parent_doc_id: document.convert_doc_id,
              owner_uid: int, title: str, content: str, is_public: bool=True,
              ip: str=None):
  """Add a clarification question."""
  validator.check_title(title)
  validator.check_content(content)
  return await document.add(domain_id, content, owner_uid,
                           document.TYPE_CLARIFICATION_QUESTION,
                           title=title,
                           is_public=is_public,
                           is_announcement=False,
                           answered=False,
                           answer_content=None,
                           answer_uid=None,
                           ip=ip,
                           parent_doc_type=parent_doc_type,
                           parent_doc_id=parent_doc_id,
                           update_at=datetime.datetime.utcnow())


@argmethod.wrap
async def get(domain_id: str, cqid: document.convert_doc_id):
  """Get a clarification question by ID."""
  return await document.get(domain_id, document.TYPE_CLARIFICATION_QUESTION, cqid)


@argmethod.wrap
async def edit(domain_id: str, cqid: document.convert_doc_id, **kwargs):
  """Edit a clarification question."""
  if 'title' in kwargs:
    validator.check_title(kwargs['title'])
  if 'content' in kwargs:
    validator.check_content(kwargs['content'])
  if 'answer_content' in kwargs and kwargs['answer_content']:
    validator.check_content(kwargs['answer_content'])
  kwargs['update_at'] = datetime.datetime.utcnow()
  return await document.set(domain_id, document.TYPE_CLARIFICATION_QUESTION, cqid, **kwargs)


@argmethod.wrap
async def answer(domain_id: str, cqid: document.convert_doc_id, answer_uid: int,
                 answer_content: str):
  """Answer a clarification question."""
  validator.check_content(answer_content)
  return await edit(domain_id, cqid,
                   answered=True,
                   answer_content=answer_content,
                   answer_uid=answer_uid)


@argmethod.wrap
async def set_visibility(domain_id: str, cqid: document.convert_doc_id, is_public: bool):
  """Set visibility of a clarification question (public or private)."""
  return await edit(domain_id, cqid, is_public=is_public)


@argmethod.wrap
async def set_announcement(domain_id: str, cqid: document.convert_doc_id, is_announcement: bool):
  """Set whether a clarification question is an announcement."""
  return await edit(domain_id, cqid, is_announcement=is_announcement)


@argmethod.wrap
async def delete(domain_id: str, cqid: document.convert_doc_id):
  """Delete a clarification question."""
  return await document.delete(domain_id, document.TYPE_CLARIFICATION_QUESTION, cqid)


@argmethod.wrap
def get_multi(domain_id: str, *, fields=None, **kwargs):
  """Get multiple clarification questions."""
  return document.get_multi(domain_id=domain_id,
                           doc_type=document.TYPE_CLARIFICATION_QUESTION,
                           fields=fields,
                           **kwargs) \
                 .sort([('is_announcement', -1),
                        ('update_at', -1),
                        ('doc_id', -1)])


@argmethod.wrap
async def count(domain_id: str, **kwargs):
  """Count clarification questions."""
  # Use count_documents instead of cursor.count() which is deprecated
  coll = db.coll('document')
  return await coll.count_documents({'domain_id': domain_id,
                                     'doc_type': document.TYPE_CLARIFICATION_QUESTION,
                                     **kwargs})


if __name__ == '__main__':
  argmethod.invoke_by_args()
