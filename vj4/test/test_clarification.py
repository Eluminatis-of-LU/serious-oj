import unittest
from bson import objectid

from vj4 import error
from vj4.model import document
from vj4.model.adaptor import clarification
from vj4.test import base

DOMAIN_ID_DUMMY = 'dummy'
CONTEST_ID = objectid.ObjectId()
OWNER_UID = 22
TITLE = 'Question about problem A'
CONTENT = 'Can you clarify the input format?'
ANSWER_CONTENT = 'The input format is specified in the problem statement.'


class ClarificationTest(base.DatabaseTestCase):
  @base.wrap_coro
  async def test_add_get(self):
    # Add a clarification question
    cqid = await clarification.add(
        DOMAIN_ID_DUMMY,
        document.TYPE_CONTEST,
        CONTEST_ID,
        OWNER_UID,
        TITLE,
        CONTENT,
        is_public=True
    )
    
    # Get the clarification
    cqdoc = await clarification.get(DOMAIN_ID_DUMMY, cqid)
    
    # Verify all fields
    self.assertIsNotNone(cqdoc)
    self.assertEqual(cqdoc['doc_id'], cqid)
    self.assertEqual(cqdoc['domain_id'], DOMAIN_ID_DUMMY)
    self.assertEqual(cqdoc['parent_doc_type'], document.TYPE_CONTEST)
    self.assertEqual(cqdoc['parent_doc_id'], CONTEST_ID)
    self.assertEqual(cqdoc['owner_uid'], OWNER_UID)
    self.assertEqual(cqdoc['title'], TITLE)
    self.assertEqual(cqdoc['content'], CONTENT)
    self.assertEqual(cqdoc['is_public'], True)
    self.assertEqual(cqdoc['is_announcement'], False)
    self.assertEqual(cqdoc['answered'], False)
    self.assertIsNone(cqdoc['answer_content'])
    self.assertIsNone(cqdoc['answer_uid'])

  @base.wrap_coro
  async def test_add_private(self):
    # Add a private clarification question
    cqid = await clarification.add(
        DOMAIN_ID_DUMMY,
        document.TYPE_CONTEST,
        CONTEST_ID,
        OWNER_UID,
        TITLE,
        CONTENT,
        is_public=False
    )
    
    # Get the clarification
    cqdoc = await clarification.get(DOMAIN_ID_DUMMY, cqid)
    
    # Verify it's private
    self.assertFalse(cqdoc['is_public'])

  @base.wrap_coro
  async def test_answer(self):
    # Add a clarification question
    cqid = await clarification.add(
        DOMAIN_ID_DUMMY,
        document.TYPE_CONTEST,
        CONTEST_ID,
        OWNER_UID,
        TITLE,
        CONTENT,
        is_public=True
    )
    
    # Answer the question
    answer_uid = 100
    await clarification.answer(DOMAIN_ID_DUMMY, cqid, answer_uid, ANSWER_CONTENT)
    
    # Get the clarification
    cqdoc = await clarification.get(DOMAIN_ID_DUMMY, cqid)
    
    # Verify answer fields
    self.assertTrue(cqdoc['answered'])
    self.assertEqual(cqdoc['answer_content'], ANSWER_CONTENT)
    self.assertEqual(cqdoc['answer_uid'], answer_uid)

  @base.wrap_coro
  async def test_set_visibility(self):
    # Add a public clarification question
    cqid = await clarification.add(
        DOMAIN_ID_DUMMY,
        document.TYPE_CONTEST,
        CONTEST_ID,
        OWNER_UID,
        TITLE,
        CONTENT,
        is_public=True
    )
    
    # Make it private
    await clarification.set_visibility(DOMAIN_ID_DUMMY, cqid, False)
    cqdoc = await clarification.get(DOMAIN_ID_DUMMY, cqid)
    self.assertFalse(cqdoc['is_public'])
    
    # Make it public again
    await clarification.set_visibility(DOMAIN_ID_DUMMY, cqid, True)
    cqdoc = await clarification.get(DOMAIN_ID_DUMMY, cqid)
    self.assertTrue(cqdoc['is_public'])

  @base.wrap_coro
  async def test_set_announcement(self):
    # Add a clarification question
    cqid = await clarification.add(
        DOMAIN_ID_DUMMY,
        document.TYPE_CONTEST,
        CONTEST_ID,
        OWNER_UID,
        TITLE,
        CONTENT,
        is_public=True
    )
    
    # Mark as announcement
    await clarification.set_announcement(DOMAIN_ID_DUMMY, cqid, True)
    cqdoc = await clarification.get(DOMAIN_ID_DUMMY, cqid)
    self.assertTrue(cqdoc['is_announcement'])
    
    # Unmark announcement
    await clarification.set_announcement(DOMAIN_ID_DUMMY, cqid, False)
    cqdoc = await clarification.get(DOMAIN_ID_DUMMY, cqid)
    self.assertFalse(cqdoc['is_announcement'])

  @base.wrap_coro
  async def test_edit(self):
    # Add a clarification question
    cqid = await clarification.add(
        DOMAIN_ID_DUMMY,
        document.TYPE_CONTEST,
        CONTEST_ID,
        OWNER_UID,
        TITLE,
        CONTENT,
        is_public=True
    )
    
    # Edit the question
    new_title = 'Updated title'
    new_content = 'Updated content'
    await clarification.edit(DOMAIN_ID_DUMMY, cqid, title=new_title, content=new_content)
    
    cqdoc = await clarification.get(DOMAIN_ID_DUMMY, cqid)
    self.assertEqual(cqdoc['title'], new_title)
    self.assertEqual(cqdoc['content'], new_content)

  @base.wrap_coro
  async def test_delete(self):
    # Add a clarification question
    cqid = await clarification.add(
        DOMAIN_ID_DUMMY,
        document.TYPE_CONTEST,
        CONTEST_ID,
        OWNER_UID,
        TITLE,
        CONTENT,
        is_public=True
    )
    
    # Delete it
    await clarification.delete(DOMAIN_ID_DUMMY, cqid)
    
    # Verify it's gone
    cqdoc = await clarification.get(DOMAIN_ID_DUMMY, cqid)
    self.assertIsNone(cqdoc)

  @base.wrap_coro
  async def test_get_multi(self):
    contest_id_1 = objectid.ObjectId()
    contest_id_2 = objectid.ObjectId()
    
    # Add multiple clarifications for different contests
    cqid1 = await clarification.add(
        DOMAIN_ID_DUMMY, document.TYPE_CONTEST, contest_id_1,
        OWNER_UID, 'Question 1', 'Content 1', is_public=True
    )
    cqid2 = await clarification.add(
        DOMAIN_ID_DUMMY, document.TYPE_CONTEST, contest_id_1,
        OWNER_UID, 'Question 2', 'Content 2', is_public=False
    )
    cqid3 = await clarification.add(
        DOMAIN_ID_DUMMY, document.TYPE_CONTEST, contest_id_2,
        OWNER_UID, 'Question 3', 'Content 3', is_public=True
    )
    
    # Get all clarifications for contest_id_1
    cqdocs = await clarification.get_multi(
        DOMAIN_ID_DUMMY,
        parent_doc_type=document.TYPE_CONTEST,
        parent_doc_id=contest_id_1
    ).to_list(None)
    
    self.assertEqual(len(cqdocs), 2)
    
    # Get only public clarifications for contest_id_1
    cqdocs_public = await clarification.get_multi(
        DOMAIN_ID_DUMMY,
        parent_doc_type=document.TYPE_CONTEST,
        parent_doc_id=contest_id_1,
        is_public=True
    ).to_list(None)
    
    self.assertEqual(len(cqdocs_public), 1)
    self.assertEqual(cqdocs_public[0]['title'], 'Question 1')

  @base.wrap_coro
  async def test_count(self):
    contest_id = objectid.ObjectId()
    
    # Initially no clarifications
    count = await clarification.count(
        DOMAIN_ID_DUMMY,
        parent_doc_type=document.TYPE_CONTEST,
        parent_doc_id=contest_id
    )
    self.assertEqual(count, 0)
    
    # Add some clarifications
    await clarification.add(
        DOMAIN_ID_DUMMY, document.TYPE_CONTEST, contest_id,
        OWNER_UID, 'Question 1', 'Content 1', is_public=True
    )
    await clarification.add(
        DOMAIN_ID_DUMMY, document.TYPE_CONTEST, contest_id,
        OWNER_UID, 'Question 2', 'Content 2', is_public=True
    )
    
    # Count should be 2
    count = await clarification.count(
        DOMAIN_ID_DUMMY,
        parent_doc_type=document.TYPE_CONTEST,
        parent_doc_id=contest_id
    )
    self.assertEqual(count, 2)

  @base.wrap_coro
  async def test_announcement_sorting(self):
    contest_id = objectid.ObjectId()
    
    # Add clarifications with one as announcement
    cqid1 = await clarification.add(
        DOMAIN_ID_DUMMY, document.TYPE_CONTEST, contest_id,
        OWNER_UID, 'Regular Question', 'Content', is_public=True
    )
    cqid2 = await clarification.add(
        DOMAIN_ID_DUMMY, document.TYPE_CONTEST, contest_id,
        OWNER_UID, 'Important Announcement', 'Important content', is_public=True
    )
    
    # Mark second one as announcement
    await clarification.set_announcement(DOMAIN_ID_DUMMY, cqid2, True)
    
    # Get all clarifications - announcements should come first
    cqdocs = await clarification.get_multi(
        DOMAIN_ID_DUMMY,
        parent_doc_type=document.TYPE_CONTEST,
        parent_doc_id=contest_id
    ).to_list(None)
    
    self.assertEqual(len(cqdocs), 2)
    self.assertTrue(cqdocs[0]['is_announcement'])
    self.assertEqual(cqdocs[0]['title'], 'Important Announcement')


if __name__ == '__main__':
  unittest.main()
